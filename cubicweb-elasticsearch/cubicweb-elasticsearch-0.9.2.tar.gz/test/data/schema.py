from yams.buildobjs import EntityType, String, Int, SubjectRelation, RelationDefinition


class Person(EntityType):
    name = String(fulltextindexed=True)
    age = Int()
