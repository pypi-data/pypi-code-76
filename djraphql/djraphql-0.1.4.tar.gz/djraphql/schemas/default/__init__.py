from ..abstract_type_builder import AbstractSchema
from .types.queries.by_pk import ByPkQuery
from .types.queries.aggregate import AggregateQuery
from .types.queries.many import ManyQuery
from .types.mutations.delete import DeleteMutation
from .types.mutations.insert import InsertMutation
from .types.mutations.update import UpdateMutation
from .types.shared.where_clause import WhereClause
from .types.shared.order_clause import OrderClause
from .types.shared.where_predicate import WherePredicate
from .types.shared.basic import BasicType
from .types.shared.enum import EnumType
from .types.shared.pk_input import PkInputType
from .types.shared.aggregate_result import AggregateResultType
from .types.shared.aggregate_basic import AggregateBasicType
from .types.shared.aggregate_group_by import AggregateGroupByType
from .types.shared.insert_input_type import InsertInputType
from .types.shared.update_input_type import UpdateInputType
from .types.shared.list_update_input_type import ListUpdateInputType
from .types.shared.nested_item_update_input_type import (
    NestedItemUpdateInputType,
)
from .types.shared.nested_item_insert_input_type import (
    NestedItemInsertInputType,
)
from .types.shared.tag_to_pk import TagToPkType
from .resolvers.insert import InsertMutationResolverType
from .resolvers.update import UpdateMutationResolverType
from .resolvers.delete import DeleteMutationResolverType
from .mappings import Types


class DefaultSchema(AbstractSchema):

    DEFAULT_QUERIES = (ByPkQuery, ManyQuery, AggregateQuery)
    DEFAULT_MUTATIONS = (InsertMutation, UpdateMutation, DeleteMutation)

    def get_node_name_for_model(self, model_class):
        return model_class.__name__

    def get_builder_mapping(self):
        return {
            Types.AGGREGATE_RESULT_TYPE: AggregateResultType,
            Types.AGGREGATE_BASIC_TYPE: AggregateBasicType,
            Types.AGGREGATE_GROUP_BY_TYPE: AggregateGroupByType,
            Types.AGGREGATE_QUERY_TYPE: AggregateQuery,
            Types.BASIC_TYPE: BasicType,
            Types.BY_PK_QUERY_TYPE: ByPkQuery,
            Types.DELETE_MUTATION_RESOLVER: DeleteMutationResolverType,
            Types.DELETE_MUTATION_TYPE: DeleteMutation,
            Types.ENUM_TYPE: EnumType,
            Types.INSERT_INPUT_TYPE: InsertInputType,
            Types.INSERT_MUTATION_RESOLVER: InsertMutationResolverType,
            Types.INSERT_MUTATION_TYPE: InsertMutation,
            Types.LIST_UPDATE_INPUT_TYPE: ListUpdateInputType,
            Types.MANY_QUERY_TYPE: ManyQuery,
            Types.NESTED_ITEM_UPDATE_TYPE: NestedItemUpdateInputType,
            Types.NESTED_ITEM_INSERT_TYPE: NestedItemInsertInputType,
            Types.ORDER_CLAUSE_TYPE: OrderClause,
            Types.PK_INPUT_TYPE: PkInputType,
            Types.TAG_TO_PK_TYPE: TagToPkType,
            Types.UPDATE_INPUT_TYPE: UpdateInputType,
            Types.UPDATE_MUTATION_TYPE: UpdateMutation,
            Types.UPDATE_MUTATION_RESOLVER: UpdateMutationResolverType,
            Types.WHERE_CLAUSE_TYPE: WhereClause,
            Types.WHERE_PREDICATE_INPUT_TYPE: WherePredicate,
        }
