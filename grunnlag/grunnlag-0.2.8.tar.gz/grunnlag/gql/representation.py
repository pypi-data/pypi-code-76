from bergen.query import DelayedGQL


GET_REPRESENTATION = DelayedGQL("""
query Representation($id: ID!){
  representation(id: $id){
    id
    name
    tags
    image
    variety
    store
    unique
    sample {
      id
    }
  
  }
}
""")

CREATE_REPRESENTATION = DelayedGQL("""
mutation Representation($sample: ID!, $name: String!, $tags: [String], $variety: RepresentationVarietyInput){
  createRepresentation(sample: $sample, name: $name, tags: $tags, variety: $variety){
    name
    id
    image
    variety
    tags
    store
    unique
  
  }
}
""")

UPDATE_REPRESENTATION = DelayedGQL("""
mutation Representation($id: ID!){
  updateRepresentation(rep: $id){
    name
    id
    image
    variety
    tags
    store
    unique
  }
}
""")


FILTER_REPRESENTATION = DelayedGQL("""
query Representation($name: String) {
  representations(name: $name) {
    id
    name
    image
    store
    variety
    tags
    unique
    sample {
      id
    }
  }
}
""")