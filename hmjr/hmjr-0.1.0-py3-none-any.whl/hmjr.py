from python_graphql_client import GraphqlClient

def example():
    # Instantiate the client with our endpoint.
    hmjr = GraphqlClient(endpoint="https://hmjrapi-prod.herokuapp.com/")

    query = """
        query entries {
            entries(max: 5, offset: 0) {
                header
                content
            }
        }
    """

    data = hmjr.execute(query=query)
    print(data)

