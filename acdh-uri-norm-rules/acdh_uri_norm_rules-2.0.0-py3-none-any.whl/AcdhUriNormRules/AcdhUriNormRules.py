import json
import pkg_resources
import re

def get_rules():
  """ returns a list of regex pattern mateches

  :return: a list of regex patterns to normalize Authority IDs
  :rtype: list
  
  """
  return json.loads(pkg_resources.resource_string(__name__, 'rules.json'))
    

def get_normalized_uri(uri):
  """ takes a normdata uri and returns a normlalized version
  :param uri: A normdata uri
  :param type: str
  
  :return: The normalized URI
  :rtype: str
  """
  for x in get_rules():
    uri = re.sub(x['match'], x['replace'], uri)
  return uri