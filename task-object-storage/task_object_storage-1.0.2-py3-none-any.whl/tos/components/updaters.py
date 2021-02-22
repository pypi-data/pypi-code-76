from bson.binary import Binary

from tos.utils import accept_string_object_ids


class TaskUpdaters:

    @accept_string_object_ids
    def increment_retry_count(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        # TODO: move to setters
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"retry_count": 1},
             "$currentDate": {"updatedAt": {"$type": "date"}}}
        )

    @accept_string_object_ids
    def increment_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        # TODO: move to setters
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"stage": 1},
             "$currentDate": {"updatedAt": {"$type": "date"}}}
        )

    @accept_string_object_ids
    def decrement_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        # TODO: move to setters
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"stage": -1},
             "$currentDate": {"updatedAt": {"$type": "date"}}}
        )

    @accept_string_object_ids
    def add_binary_data_to_payload(self, object_id, filepath, data_title):
        """
        Put an encoded binary string to database.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param filepath: file path to the file to encode
        :type filepath: str
        :param data_title: name of the binary data to store.
        :type data_title: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`

        :ivar bin_data: bson.Binary encoded binary data
        """
        bin_data = self._encode_binary_data(filepath)
        return self.add_key_value_pair_to_payload(object_id, data_title, bin_data)

    def _encode_binary_data(self, filepath):
        """
        Encode a file to a binary string presentation.

        :param filepath: file path to the file to encode
        :type filepath: str

        :returns: encoded file
        :rtype: bson.Binary
        """
        with open(filepath, "rb") as f:
            encoded = Binary(f.read())
        return encoded

    @accept_string_object_ids
    def update_payload(self, object_id, update):
        """
        Update task object payload with new data.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param update: key value pair(s) to add to payload
        :type update: dict

        :raises TypeError: when ``update`` is not a dict.
        :returns: List of results of the update action
        :rtype: List of :class: `pymongo.results.UpdateResult`
        """
        if not isinstance(update, dict):
            raise TypeError("Argument update should be a dict")

        results = []
        for key, value in update.items():
            results.append(
                self.add_key_value_pair_to_payload(object_id, key, value)
            )
        return results

    @accept_string_object_ids
    def add_key_value_pair_to_payload(self, object_id, key, value):
        """
        Add single key value pair to payload.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to insert
        :type key: str
        :param value: value of the field to insert
        :type value: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._add_key_value_pair_to_field(object_id, key, value, "payload")

    @accept_string_object_ids
    def _add_key_value_pair_to_field(self, object_id, key, value, field_name):
        """
        Add single key value pair to payload.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to insert
        :type key: str
        :param value: value of the field to insert
        :type value: str
        :param field_name: name of the field where the key-value pair is inserted
        :type field_name: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        item_name = f"{field_name}.{key}"
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {item_name: value},
             "$currentDate": {"updatedAt": {"$type": "date"}}}
        )

    @accept_string_object_ids
    def push_value_to_array_field(self, object_id, value, field_name):
        """
        Push an arbitrary value to an array type field.

        Push is an upsert operation; if the array doesn't exist,
        it will be created.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param value: value of the field to insert
        :type value: str, int or dict
        :param field_name: Name of the array field, e.g. 'analytics' or
            'payload.alerts'
        :type field_name: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$push": {field_name: value},
             "$currentDate": {"updatedAt": {"$type": "date"}}}
        )

    @accept_string_object_ids
    def update_stage_exceptions(self, object_id, error_text, stage):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param error_text: Exception stacktrace or error text
        :type error_text: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.push_value_to_array_field(
            object_id,
            error_text,
            f"stages.{stage}.exceptions"
        )

    @accept_string_object_ids
    def update_stage_retry_count(self, object_id, stage):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {
                "$inc": {f"stages.{stage}.retry_count": 1},
                "$currentDate": {"updatedAt": {"$type": "date"}}
            }
        )

    def update_stage_object(self, object_id, current_stage):
        """Update stages object with new stage."""
        self.set_task_object_stage(object_id, current_stage)
        self.set_stage_start_time(object_id, current_stage)
        self.set_stage_build_number(object_id, current_stage)
        self.set_stage_executor(object_id, current_stage)

    def update_status(self, object_id, current_stage, status):
        """Update task object and its stages object with new status."""
        self.set_task_object_status(object_id, status)
        self.set_stage_status(object_id, current_stage, status)

    def update_exceptions(self, object_id, current_stage, error_text):
        """Update task object and its stages object with the new exception."""
        self.set_task_object_last_error(object_id, error_text)
        self.update_stage_exceptions(object_id, error_text, current_stage)

    def save_retry_metadata_if_retry(self, to, current_stage):
        """
        For every run, check if it's a retry.
        If it is, populate a retry object inside the stage object.
        This way we get to know when and where the job has been running
        on failures.
        """
        # TODO: combine this with update_stage, they are mostly duplicate code
        if to.get("retry_count", 0) > 0:
            self._update_retries_data(
                to["_id"],
                current_stage,
                to["retry_count"]
            )

    def _update_retries_data(self, object_id, current_stage, retry_count):
        self.set_retry_build_number(object_id, current_stage, retry_count)
        self.set_retry_executor(object_id, current_stage, retry_count)
