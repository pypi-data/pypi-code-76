"""
# Input Modules
Modules that grab inputs from somewhere

## Patterns

### jq-vars
jq-vars is a dict, with the key being the var to replace `{var}` in the `vars:` job definition. The value is a JQ
expression. With this we can extract parts of a external response without multiple calls.
See: https://stedolan.github.io/jq/
Have a look in `tests/component-resources/job-*.yml` for examples. You can also test your queries using test data.
For example `cat tests/component-resources/response-open-weather-city.json | jq "\"Test: \" + .weather[0].description"`
Note: YQ also exists for YML/YAML responses if you want to call an API yourself. See: `https://pypi.org/project/yq/`
"""
