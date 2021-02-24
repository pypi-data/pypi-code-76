import json

class NuvIoTItem:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        return

def to_item_array(json, name_field = "name"):
    if json == None:
        return None
    
    items = []
    ret_items = json["model"]
    for ret_item in ret_items:
        items.append(NuvIoTItem(ret_item["id"], ret_item[name_field]))
                  
    return items
        
def print_array(name, items):
    if items == None:
        print('No Data')
    
    print(name)
    print('-----------------------------------------')
    for item in items:
        print(item.id, item.name)
        
    print('-----------------------------------------')
    print()