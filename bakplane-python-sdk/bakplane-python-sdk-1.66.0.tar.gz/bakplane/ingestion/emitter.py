import concurrent.futures
import datetime
import os
import tempfile
import typing
from abc import abstractmethod, ABC
from typing import IO

from google.protobuf.internal.encoder import _VarintBytes
from sortedcontainers import SortedSet

from bakplane.bakplane_pb2 import ErrorEntry
from bakplane.ingestion.landing_zone import LandingZoneFactory
from .models import (
    Asset,
    Entity,
    Relationship,
    IngestionSessionContext,
    Error,
    Descriptor,
)

PARTITION_NUM = os.cpu_count()
KEY_SEPARATOR = "::"


def reduce_pair(
    p1: typing.Tuple[datetime.datetime, datetime.datetime],
    p2: typing.Tuple[datetime.datetime, datetime.datetime],
):
    a, b = p1
    c, d = p2

    if a == c:
        if b < d:
            return (a, d), None
        elif b > d:
            return (a, b), None
        else:
            raise RuntimeError("Not allowed")
    elif a < c:
        if b == d:
            return (a, b), None
        elif b < d:
            if b < c:
                return (a, b), (c, d)
            elif b > c:
                return (a, d), None
            return (a, d), None
        else:
            return (a, b), None


def reduce_intervals(s: SortedSet) -> SortedSet:
    if not s:
        raise RuntimeError("Input cannot be none.")

    if len(s) == 1:
        return s

    done = SortedSet()

    last = s[0]

    for i in range(1, len(s)):
        p1 = s[i]
        i1, i2 = reduce_pair(last, p1)

        if i2 is not None:
            done.add(i1)
            done.add(i2)

            last = i2
        else:
            last = i1

    done.add(last)
    return done


class Emitter(ABC):
    @abstractmethod
    def emit_assets(self, assets: typing.List[Asset]):
        pass

    @abstractmethod
    def emit_entities(self, entities: typing.List[Entity]):
        pass

    @abstractmethod
    def emit_relationships(self, relationships: typing.List[Relationship]):
        pass

    @abstractmethod
    def emit_errors(self, errors: typing.List[Error]):
        pass


class RelationshipReduceMap:
    source_identity_uid: int
    target_identity_uid: int
    relationship_type: str
    effective_dating: SortedSet

    def __init__(self, r: Relationship):
        self.relationship_type = r.relationship_type
        self.target_identity_uid = r.target_identity_uid
        self.source_identity_uid = r.source_identity_uid
        self.effective_dating = SortedSet()

        self.append(r)

    def append(self, r: Relationship):
        if (
            r.source_identity_uid != self.source_identity_uid
            or r.target_identity_uid != self.target_identity_uid
            or r.relationship_type != self.relationship_type
        ):
            raise RuntimeError(
                "Invalid relationship identity for this reducer."
            )

        for e in r.effective_dating:
            self.effective_dating.add((e[0], e[1]))

    def reduce(self) -> Relationship:
        reduced_intervals = []

        for interval in reduce_intervals(self.effective_dating):
            start, end = interval

            reduced_intervals.append((start, end))

        return Relationship(
            relationship_type=self.relationship_type,
            source_identity_uid=self.source_identity_uid,
            target_identity_uid=self.target_identity_uid,
            effective_dating=reduced_intervals,
        )


class EntityReduceMap:
    def __init__(self, entity: Entity):
        self.identity = entity.identity
        self.values = {}

        self.append(entity)

    def append(self, entity: Entity):
        if entity.identity.uid != self.identity.uid:
            raise RuntimeError(
                f"Entity mismatch: expected entity with identity `{entity.identity.uid}`."
            )

        for d in entity.descriptors:
            self.append_descriptor(d)

    def append_descriptor(self, d: Descriptor):
        key = d.attribute + KEY_SEPARATOR + d.value

        if key not in self.values:
            self.values[key] = SortedSet()

        for dt in d.effective_dating:
            self.values[key].add((dt[0], dt[1]))

    def reduce(self) -> Entity:
        descriptors: typing.List[Descriptor] = []

        for key, v in self.values.items():
            attr, val = key.split(KEY_SEPARATOR)

            effective_dating = []

            for interval in reduce_intervals(v):
                start, end = interval

                effective_dating.append((start, end))

            descriptors.append(
                Descriptor(
                    attribute=attr,
                    value=val,
                    effective_dating=effective_dating,
                )
            )

        self.values = None
        return Entity(identity=self.identity, descriptors=descriptors)


class DefaultEmitter(Emitter):
    def __init__(
        self,
        context: IngestionSessionContext,
        asset_num_sharding=8,
        entities_num_sharding=8,
        rels_num_sharding=8,
        csv_separator: str = "|",
        null_value: str = "NULL",
    ):

        if (
            asset_num_sharding < 1
            or entities_num_sharding < 1
            or rels_num_sharding < 1
        ):
            raise RuntimeError("Invalid requested number of shards.")

        self.ctx = context
        self.fd_map: typing.Dict[str, IO] = {}

        self.entities_lz = LandingZoneFactory.build_from_uri(
            context.entities_output_location
        )

        self.assets_lz = LandingZoneFactory.build_from_uri(
            context.assets_output_location
        )

        self.relationships_lz = LandingZoneFactory.build_from_uri(
            context.relationships_output_location
        )

        self.errors_lz = LandingZoneFactory.build_from_uri(
            context.errors_output_location
        )

        self.asset_num_sharding = asset_num_sharding
        self.entities_num_sharding = entities_num_sharding
        self.rels_num_sharding = rels_num_sharding

        self.entity_map = {}
        self.rel_map = {}

        self.csv_separator = csv_separator
        self.null_value = null_value

    def __get_entities_fd(self, entity: Entity) -> IO:
        key = "entities"

        if self.entities_num_sharding > 1:
            shard = entity.identity.uid % self.entities_num_sharding
            key += f"___{shard}_of_{self.entities_num_sharding}_"

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __get_errors_fd(self, error: ErrorEntry) -> IO:
        if "errors" not in self.fd_map:
            self.fd_map["errors"] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix="errors"
            )
        return self.fd_map["errors"]

    def __get_relationships_fd(self, relationship: Relationship) -> IO:
        key = "relationships"

        if self.rels_num_sharding > 1:
            shard = relationship.source_identity_uid % self.rels_num_sharding
            key += f"___{shard}_of_{self.rels_num_sharding}_"

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __get_assets_fd(self, asset: Asset) -> IO:
        key = asset.resource_code

        if self.asset_num_sharding > 1:
            shard = asset.payload_hash % self.asset_num_sharding
            key += f"___{shard}_of_{self.asset_num_sharding}_"

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __write_entity(self, entity: Entity):
        if entity.identity.uid not in self.entity_map:
            self.entity_map[entity.identity.uid] = EntityReduceMap(entity)
        else:
            self.entity_map[entity.identity.uid].append(entity)

    def __write_error(self, error: ErrorEntry):
        f = self.__get_errors_fd(error)
        p = error.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

    def __write_relationship(self, relationship: Relationship):
        if relationship.identity not in self.rel_map:
            self.rel_map[relationship.identity] = RelationshipReduceMap(
                relationship
            )
        else:
            self.rel_map[relationship.identity].append(relationship)

    def __write_asset(self, asset: Asset):
        f = self.__get_assets_fd(asset)
        f.write(
            asset.to_csv_entry(self.ctx, self.csv_separator, self.null_value)
            + "\n"
        )

    def emit_entities(self, entities: typing.List[Entity]):
        if entities is None or len(entities) <= 0:
            raise ValueError("Entities cannot be null or empty.")

        for e in entities:
            self.__write_entity(e)

    def emit_relationships(self, relationships: typing.List[Relationship]):
        if relationships is None or len(relationships) <= 0:
            raise ValueError("Relationships cannot be null or empty.")

        for r in relationships:
            self.__write_relationship(r)

    def emit_errors(self, errors: typing.List[Error]):
        if errors is None or len(errors) <= 0:
            raise ValueError("Errors cannot be null or empty.")

        for e in errors:
            self.__write_error(e)

    def emit_assets(self, assets: typing.List[Asset]):
        if assets is None or len(assets) <= 0:
            raise ValueError("Assets cannot be null or empty.")

        for a in assets:
            self.ctx.validate_asset(a)
            self.__write_asset(a)

    def reduce_entities(self):
        for k, e in self.entity_map.items():
            entity = e.reduce()

            f = self.__get_entities_fd(entity)
            p = entity.to_proto()

            f.write(_VarintBytes(p.ByteSize()))
            f.write(p.SerializeToString())

    def reduce_relationships(self):
        for k, r in self.rel_map.items():
            relationship = r.reduce()

            f = self.__get_relationships_fd(relationship)
            p = relationship.to_proto()

            f.write(_VarintBytes(p.ByteSize()))
            f.write(p.SerializeToString())

    def close(self):
        self.reduce_entities()
        self.reduce_relationships()

        for k, v in self.fd_map.items():
            v.close()

            if k.startswith("entities"):
                self.entities_lz.upload(
                    v.name,
                    self.ctx.entities_output_location,
                    ".proto.gz",
                    prefix="entities",
                )

            elif k.startswith("relationships"):
                self.relationships_lz.upload(
                    v.name,
                    self.ctx.relationships_output_location,
                    ".proto.gz",
                    prefix="relationships",
                )

            elif k == "errors":
                self.errors_lz.upload(
                    v.name,
                    self.ctx.errors_output_location,
                    ".proto.gz",
                    prefix="errors",
                )
            else:
                asset_code = k
                if self.asset_num_sharding > 1:
                    asset_code = asset_code.split("___")[0]
                    self.assets_lz.upload(
                        v.name,
                        self.ctx.assets_output_location + asset_code + "/",
                        ".csv.gz",
                    )
