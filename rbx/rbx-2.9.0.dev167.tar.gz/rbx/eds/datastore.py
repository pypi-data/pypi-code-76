import functools
import logging
import math
import re
import time

import arrow
from google.cloud.datastore import Client, Entity, Key
from google.cloud.exceptions import Conflict

from ..exceptions import FatalException, RetryError, TransientException

logger = logging.getLogger(__name__)

# Google API commit object limit per api call
QUERY_LIMIT = 500


def retry_target(target, deadline=None, on_error=None, sleep=None):
    """Call a function and retry if it fails.

    Paremeters:
        target(Callable):
            The function to call and retry.
        deadline (float):
            How long to keep retrying the target. The last sleep period is shortened as necessary,
            so that the last retry runs at ``deadline`` (and not considerably beyond it).
        on_error (Callable[Exception]):
            A function to call while processing a retryable exception. Any error raised by this
            function will *not* be caught.
        sleep (int):
            An integer that defines how long to speel for between retries.
    Returns:
        Any: the return value of the target function.
    Raises:
        rbx.exceptions.RetryError: If the deadline is exceeded while retrying.
        Exception: If the target raises a method that isn't retryable.
    """
    deadline = deadline or 30
    deadline_datetime = arrow.utcnow().shift(seconds=deadline).datetime
    sleep = sleep or 1
    last_exc = None

    while True:
        try:
            return target()

        # pylint: disable=broad-except
        # This function explicitly must deal with broad exceptions.
        except Exception as exc:
            if not isinstance(exc, (Conflict, TransientException)):
                raise
            last_exc = exc
            if on_error is not None:
                on_error(exc)

        now = arrow.utcnow().datetime

        if deadline_datetime <= now:
            raise RetryError(
                f'Deadline of {deadline:.1f}s exceeded while calling {target}',
                last_exc
            ) from last_exc

        logger.debug(f'Retrying due to {last_exc}, sleeping {sleep:.1f}s ...')
        time.sleep(sleep)


def retry(func, *args, **kwargs):
    deadline = kwargs.pop('deadline', None)
    on_error = kwargs.pop('on_error', None)
    sleep = kwargs.pop('sleep', None)
    target = functools.partial(func, *args, **kwargs)
    return retry_target(target, deadline=deadline, on_error=on_error, sleep=sleep)


class Datastore:
    client = Client()

    def __init__(self, schema=None):
        self.schema = schema

    @property
    def root(self):
        """The root Key for singletons."""
        return self.key('MDM', 'mdm')

    def _get_schema_for_kind(self, kind):
        """Locate and retrieve the schema for the given Kind.

        Raise an FatalException Exception if not found.
        """
        match = [schema for schema in self.schema.values() if schema.name == kind]
        if match:
            return match[0]

        raise FatalException('No schema defined <Kind: {}>'.format(kind))

    def ancestor(self, kind, payload=None, **kwargs):
        """Retrieve an Entity's ancestor.

        Return an Entity.

        The ancestor lookup is extracted from either the payload, or the keyword arguments.

        The lookup field is determined from the schema. When the lookup field is defined in between
        curly brackets, it indicates a field lookup. Otherwise the value is taken as is.
        """
        assert type(self.schema) is dict, 'Schema must be defined for ancestor lookups.'
        schema = self._get_schema_for_kind(kind)

        if not schema.ancestor:
            raise FatalException('No ancestor defined <Schema: {}>'.format(schema))

        return self.fetch_entity(kind=schema.ancestor['kind'],
                                 name=schema.ancestor['lookup'],
                                 stack=payload or kwargs)

    def clone_entity(self, entity):
        """Clone an Entity.

        The clone will be created with an ancestor even when the original wasn't.
        When an ancestor cannot be found, the entity is created without one.

        Note that the clone isn't stored, nor is the original deleted.

        The clone Entity is returned.
        """
        assert type(entity) is Entity

        try:
            parent = self.ancestor(entity.kind, payload=entity)
            key = self.client.key(entity.kind, parent=parent.key)
        except FatalException:
            key = self.client.key(entity.kind)
        except TransientException as e:
            logger.error(f' >> {e} << ')
            return

        clone = Entity(key=key)
        clone.update(entity)

        return clone

    def delete_all_entities_by_kind(self, kind):
        """Delete all Datastore entities by kind."""
        logger.info(f'Deleting "{kind}" from Datastore ')
        query = self.query(kind=kind)
        query.keys_only()

        while True:
            # We can't remove more than QUERY_LIMIT in 1 API call
            keys = tuple(entity.key for entity in query.fetch(
                limit=QUERY_LIMIT))
            if not keys:
                break

            self.client.delete_multi(keys)

    def fetch_checkpoint(self, name):
        """Fetch the Checkpoint entity for the given name."""
        return self.fetch_singleton('Checkpoint', name=name)

    def fetch_entity(self, kind, name, stack=None, key_only=False):
        """Retrieve the Entity or Key from the given kind and name pattern.

        Return an Entity if 'key_only' is False (the default), or a Key
        otherwise.

        When key_only is set as True, only the Key is returned.

        The name pattern may be:

          - '{field_names}': the curly brackets indicate we should attempt to
            find the name value from the stack dictionary.
            The field_names value is a coma-separated list.
            i.e.:
            >>> name = '{field_1,field_2}'
            >>> lookup_value_1 = stack[field_1]
            >>> lookup_value_2 = stack[field_2]

          - 'name': when a single string is provided, it is used as the
            ID/Name of the Key.

        When constructing an Entity/Key via lookup (using the curly brackets
        pattern), we attempt to fetch the Key from Datastore.
        This operation is always expected to find a match, therefore it will
        only return the matching Entity/Key on success.

        It will raise a TransientException on failure.
        """
        results = re.search(r'\{(.*)\}', name)
        if results:
            # The lookup is field-based. The lookup values should be extracted
            # from the stack.
            lookup_fields = results.group(1).split(',')

            if stack is None:
                raise FatalException(
                    'Cannot find a Key via lookup without a stack [ '
                    '<kind: {}>, <name: {}>, <stack: {}>'
                    ' ]'.format(kind, name, stack))

            try:
                lookup_values = [stack[field] for field in lookup_fields]
            except KeyError:
                raise FatalException(
                    'Could not find the lookup fields in the stack [ '
                    '<kind: {}>, <name: {}>, <stack: {}>'
                    ' ]'.format(kind, name, stack))

            query = self.query(kind=kind)
            if key_only:
                query.keys_only()

            for attribute, value in zip(lookup_fields, lookup_values):
                query.add_filter(attribute, '=', value)
            try:
                entity = list(query.fetch())[0]
            except IndexError:
                raise TransientException(
                    'Failed to find the Key [ '
                    '<kind: {}>, <name: {}>, <stack: {}>'
                    ' ]'.format(kind, name, stack))

        else:
            # No lookup required, use the name as the ID/Name.
            entity = Entity(key=self.client.key(kind, name))

        return entity.key if key_only else entity

    def fetch_key(self, *args, **kwargs):
        """A proxy to fetch_entity with the key_only flag set to True."""
        kwargs['key_only'] = True
        return self.fetch_entity(*args, **kwargs)

    def fetch_singleton(self, kind, name, parent=None):
        """Fetch an Entity for the given kind and name.

        When no match is found, return a new Entity.
        Note that this method does not save that new Entity.
        """
        if parent is None:
            parent = self.root

        key = Key(kind, name, parent=parent)

        query = self.query(kind=kind, ancestor=parent)
        query.key_filter(key=key)
        results = list(query.fetch())

        if results:
            return results[0]

        return Entity(key=key)

    def get_day_key(self, date_str):
        """Expects a date string in the form of 'YYYY-MM-DD HH:mm'."""
        try:
            return int(date_str.split(' ')[0].replace('-', ''))
        except ValueError:
            logger.exception('Unable to resolve day_key.')
            return None

    def get_surrogate_key(self, kind, name, entity_id):
        """Get an Entity's surrogate key given its Kind, name, and ID.

        The ID may be a combined ID, in which case it is expected to be a dict instance, keyed by
        the combined IDs.

        Returns None when no match is found.
        """
        key_field = '{}_key'.format(name)

        if isinstance(entity_id, dict):
            id_field = ','.join(f'{field}' for field in entity_id.keys())
            id_field = f'{{{id_field}}}'
            stack = entity_id

        else:
            id_field = f'{{{name}_id}}'
            stack = {f'{name}_id': int(entity_id)}

        try:
            entity = self.fetch_entity(kind, id_field, stack=stack)
            return entity[key_field]
        except TransientException:
            logger.error('Entity <{}: {}> not found in Datastore.'.format(kind, entity_id))

        return None

    def get_time_key(self, date_str):
        """Expects a date string in the form of 'YYYY-MM-DD HH:mm'."""
        try:
            return 10000 + int(date_str.split(' ')[1].replace(':', ''))
        except ValueError:
            logger.exception('Unable to resolve time_key.')
            return None

    def key(self, *args, **kwargs):
        """Proxy to Datastore Client.key()."""
        return self.client.key(*args, **kwargs)

    def make_entity(self, kind, fields=None):
        """Create a orphan DS Entity for the given Kind and fields."""
        key = self.client.key(kind)
        entity = Entity(key)
        if fields:
            entity.update(fields)

        return entity

    def override_entities(self, kind, payload):
        """Given a payload of Entity data, replace all existing Entities for the given Kind."""
        self.delete_all_entities_by_kind(kind)

        entities = [self.make_entity(kind, item) for item in payload]

        self.save(entities)

    def query(self, *args, **kwargs):
        """Proxy to Datastore Client.query()."""
        return self.client.query(*args, **kwargs)

    def relatives(self, kind, payload=None, **kwargs):
        """Retrieve an Entity's relatives.

        The relative lookups are extracted from either the payload, or the keyword arguments.
        The lookup field is determined from the schema.
        """
        assert type(self.schema) is dict, 'Schema must be defined for relatives lookups.'
        schema = self._get_schema_for_kind(kind)

        if type(schema.relatives) not in (list, tuple):
            raise FatalException('No relatives defined <Schema: {}>'.format(schema))

        return [self.fetch_entity(kind=relative['kind'],
                                  name=relative['lookup'],
                                  stack=payload or kwargs)
                for relative in schema.relatives]

    def save(self, entities):
        """Save entities to Datastore.

        Entities are added by batches of QUERY_LIMIT.
        A single Entity instance can be provided, in which case it is saved in
        one single transaction (hence the Conflict check).
        """
        if isinstance(entities, Entity):
            logger.info('Saving 1 record to Datastore.')
            retry(self.client.put, entities)
        else:
            logger.info(f'Saving {len(entities)} records to Datastore.')
            saved = 0
            for i in range(0, len(entities), QUERY_LIMIT):
                batch = entities[i:i + QUERY_LIMIT]
                retry(self.client.put_multi, batch)
                saved += len(batch)
                logger.debug(f'Saved {saved} of {len(entities)}'
                             f' ({math.floor(100 * saved / len(entities)):d}%).')

    def save_checkpoint(self, checkpoint, timestamp):
        """Set the timestamp for the given Checkpoint Entity.

        The timestamp must be an RFC 3339 timestamp.
        """
        assert type(checkpoint) is Entity

        if checkpoint is not None:
            checkpoint['timestamp'] = timestamp
            self.save(checkpoint)
