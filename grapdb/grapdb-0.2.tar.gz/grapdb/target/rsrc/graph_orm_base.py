import hashlib
import logging
from operator import eq
import random
import struct
from typing import List, Union, Set, Tuple, TypeVar

import jump
from sqlalchemy import (  # pylint: disable=E0401
    BigInteger,
    Column,
    FetchedValue,
    Integer,
    MetaData,
    SmallInteger,
    literal,
)
from sqlalchemy.dialects.postgresql import (  # pylint: disable=E0401
    JSONB,
)
from sqlalchemy.ext.declarative import declarative_base  # pylint: disable=E0401
from sqlalchemy.sql import (  # pylint: disable=E0401
    operators,
    visitors,
)
from sqlalchemy.sql.elements import BindParameter  # pylint: disable=E0401

from sqlalchemy_utils import CompositeType  # pylint: disable=E0401

logger = logging.getLogger("graph_orm_base")

metadata = MetaData(schema="graph")
Base = declarative_base(metadata=metadata)
Gid = CompositeType("gid", [Column("id", BigInteger), Column("vshard", SmallInteger)])
TGid = Tuple[int, int]


def random_vshard() -> int:
    return random.randint(-32768, 32767)


def entry_point_to_vshard(entry_point_val: str) -> int:
    hashed_val = hashlib.sha1(entry_point_val.encode("utf-8")).digest()
    pair_of_bytes = hashed_val[:2]
    return struct.unpack("<h", pair_of_bytes)[0]


class EntityMixin:
    def get_vshard(self) -> int:
        raise NotImplementedError


VT = TypeVar("VT", bound="VertexMixin")


class VertexMixin(EntityMixin):
    gid = Column(Gid, primary_key=True, server_default=FetchedValue())
    data = Column(JSONB, server_default=FetchedValue())

    def __repr__(self) -> str:
        return "<{}(gid={})>".format(self.__class__.__name__, self.gid)

    def get_vshard(self) -> int:
        if self.gid is None:
            shard = random_vshard()
            # The need to use a literal is a hack thanks to a patch by the
            # SQLAlchemy author. The literal informs SA that it needs to adopt
            # the PK that's returned by the insert.
            # NOTE: This value is temporary and will be replaced by a proper
            # gid tuple by the time control is returned to the caller (not of
            # this method, but the caller of the higher-level DB operation).
            self.gid = literal((None, shard))
        if isinstance(self.gid, BindParameter):
            return self.gid.value[1]
        else:
            return self.gid[1]

    def colo_with(self: VT, gid_or_ent: Union[TGid, "EntityMixin"]) -> VT:
        assert self.gid is None
        if isinstance(gid_or_ent, EntityMixin):
            vshard = gid_or_ent.get_vshard()
        else:
            assert isinstance(gid_or_ent, tuple)
            vshard = gid_or_ent[1]
        self.gid = literal((None, vshard))
        return self


class EntryPointMixin:
    def get_vshard(self) -> int:
        if self.gid is None:
            entry_point_val = getattr(self, self._entry_point)
            assert entry_point_val is not None, (
                "Entry point %r must be set." % entry_point_val
            )
            # Redundant check (already enforced by grapdb)
            assert isinstance(entry_point_val, str)
            self.gid = literal((None, entry_point_to_vshard(entry_point_val)))
        if isinstance(self.gid, BindParameter):
            return self.gid.value[1]
        else:
            return self.gid[1]


class ColoMixin:
    def get_vshard(self) -> int:
        assert self.gid is not None, "Gid must be specified with colo-ed vertex."
        return self.gid[1]


class EdgeMixin(EntityMixin):
    src = Column(Gid, primary_key=True)
    tgt = Column(Gid, primary_key=True)
    data = Column(JSONB)

    def __repr__(self) -> str:
        return "<{}(src={}, tgt={})>".format(
            self.__class__.__name__, self.src, self.tgt
        )

    def get_vshard(self) -> int:
        return self.src[1]


class CounterMixin(EntityMixin):
    src = Column(Gid, primary_key=True)
    count = Column(Integer)

    def __repr__(self) -> str:
        return "<{}(src={}, count={})>".format(
            self.__class__.__name__, self.src, self.count
        )

    def get_vshard(self) -> int:
        return self.src[1]


class ShardMapper:
    def __init__(self, num_shards: int):
        assert num_shards > 0
        self.num_shards = num_shards
        self.shards_set = frozenset({str(i) for i in range(num_shards)})

    def jump_hash(self, vshard: int) -> str:
        return str(jump.hash(vshard, self.num_shards))

    def shard_chooser(self, mapper, instance, clause=None) -> str:
        """
        Called when inserting a new object:
        - s.add(V)
        - s.add(E)
        """
        vshard = instance.get_vshard() if instance else None
        logger.debug(
            "shard_chooser mapper=%r instance=%r clause=%r vshard=%r",
            mapper,
            instance,
            clause,
            vshard,
        )
        # Returning a dummy shard is necessary for sqlalchemy to return the
        # string representation of a query (str(query)) for debugging purposes.
        return self.jump_hash(vshard) if vshard else '0'

    def id_chooser(self, query, ident: List[Tuple[int, int]]) -> Set[str]:
        """
        Called when looking up entity by relationship.
        - v.colo
        """
        logger.debug("id_chooser: query=%r ident=%r", query, ident)
        assert len(ident) == 1, (len(ident), ident)
        vshards = set()
        for gid in ident:
            vshards.add(str(gid[1]))
        return vshards

    def query_chooser(self, query) -> Set[str]:
        """
        Called when querying vertex by primary key gid:
        - v = s.query(V).filter(V.gid == (3, 1)).one()

        Called when querying multiple vertices by primary key gid:
        - v = s.query(V).filter((V.gid == (3, 1)) | (V.gid == (4, 0))).all()
        - Unfortunately, it queries all applicable shards with all gids.

        Called when querying edge by partial primary key src:
        - e = s.query(Edge).filter(Edge.src == (3, 1)).one()

        Called when querying edge by primary key (src, tgt)
        - e = s.query(Edge).filter(Edge.src == (3, 1), Edge.tgt == (4,0)).one()

        Called when querying vertex by entry point:
        - v = s.query(V).filter(V.entry_point == 'xyz').one()

        If querying by non-PK gid or entry point, we ignore and return all shards.
        """
        logger.debug("query_chooser: query=%r", query)
        ent_class = query._entities[0].expr  # pylint: disable=W0212
        if hasattr(ent_class, "class_"):
            ent_class: Union[VertexMixin, EdgeMixin] = ent_class.class_
        shards = set()
        bin_exprs = _get_query_comparisons(query)
        for column, operator, value in bin_exprs:
            if column.primary_key:
                if column.name not in {"gid", "src"}:
                    continue
                if operator == eq:
                    assert isinstance(value, tuple)
                    assert len(value) == 2
                    vshard = value[1]
                    shards.add(self.jump_hash(vshard))
                elif operator == operators.in_op:
                    assert operator == operators.in_op
                    for gid in value:
                        assert isinstance(gid, tuple)
                        assert len(gid) == 2
                        vshard = gid[1]
                        shards.add(self.jump_hash(vshard))
                else:
                    assert False, "Unsupported operator %r" % operator
            elif (
                issubclass(ent_class, EntryPointMixin)
                and column.name == ent_class._entry_point
            ):  # pylint: disable=W0212
                shards.add(self.jump_hash(entry_point_to_vshard(value)))
        if not shards:
            logger.warning("query_chooser: querying all shards.")
            shards = self.shards_set
        logger.debug("query_chooser: shards=%s", shards)
        return shards


def _get_query_comparisons(query):
    """
    Search an orm.Query object for binary expressions.

    Taken from:
    http://docs.sqlalchemy.org/en/latest/_modules/examples/sharding/attribute_shard.html

    Returns expressions which match a Column against one or more literal values
    as a list of tuples of the form (column, operator, values). `values` is a
    single value or tuple of values depending on the operator.
    """
    binds = {}
    clauses = set()
    comparisons = []

    def visit_bindparam(bind) -> None:
        # visit a bind parameter.

        # check in _params for it first
        if bind.key in query._params:  # pylint: disable=W0212
            value = query._params[bind.key]  # pylint: disable=W0212
        elif bind.callable:
            # some ORM functions (lazy loading)
            # place the bind's value as a
            # callable for deferred evaluation.
            value = bind.callable()
        else:
            # just use .value
            value = bind.value

        binds[bind] = value

    def visit_column(column) -> None:
        clauses.add(column)

    def visit_binary(binary) -> None:
        # special handling for "col IN (params)"
        if (
            binary.left in clauses
            and binary.operator == operators.in_op
            and hasattr(binary.right, "clauses")
        ):
            comparisons.append(
                (
                    binary.left,
                    binary.operator,
                    tuple(binds[bind] for bind in binary.right.clauses),
                )
            )
        elif binary.left in clauses and binary.right in binds:
            comparisons.append((binary.left, binary.operator, binds[binary.right]))

        elif binary.left in binds and binary.right in clauses:
            comparisons.append((binary.right, binary.operator, binds[binary.left]))

    # here we will traverse through the query's criterion, searching
    # for SQL constructs.  We will place simple column comparisons
    # into a list.
    if query._criterion is not None:  # pylint: disable=W0212
        visitors.traverse_depthfirst(
            query._criterion,  # pylint: disable=W0212
            {},
            {
                "bindparam": visit_bindparam,
                "binary": visit_binary,
                "column": visit_column,
            },
        )
    return comparisons
