from openapi3 import OpenAPI
import yaml

# load the spec file and read the yaml
with open('/Users/balak/Downloads/aps-discovery-ts.yaml') as f:
    spec = yaml.safe_load(f)

print(spec)
print("\n\n\n\n")
print(spec["components"])
# parse the spec into python - this will raise if the spec is invalid
api = OpenAPI(spec)

# call operations and receive result models
regions = api.call_getRegions()

# authenticate using a securityScheme defined in the spec's components.securtiySchemes
api.authenticate('personalAccessToken', my_token)

# call an operation that requires authentication
linodes  = api.call_getLinodeInstances()

# call an opertaion with parameters
linode = api.call_getLinodeInstance(parameters={"linodeId": 123})

# the models returns are all of the same (generated) type
print(type(linode))                      # openapi.schemas.Linode
type(linode) == type(linodes.data[0])    # True

# call an operation with a request body
new_linode = api.call_createLinodeInstance(data={"region":"us-east","type":"g6-standard-2"})

# the returned models is still of the correct type
type(new_linode) == type(linode)     # True