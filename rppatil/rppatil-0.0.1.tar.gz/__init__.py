import json

def read_jsonl_file(path):
    """
    inputs path of file containing multiple jsons seperated by newline
    outputs list of jsons
    
    """
    list_all_jsons = []
    with open(path) as fp:
        for f in fp:
            list_all_jsons.append(json.loads(f))
        
    return list_all_jsons
    


def write_jsonl_file(out_path, list_all_jsons):
    """
    inputs : file path to write and list of all jsons
    outputs: creates a file containing multiple jsons seperated by newline
    
    """
    with open(out_path,"w") as fw: 
        for i,line in enumerate(list_all_jsons):
            fw.write(json.dumps(line , separators = (',', ':'),ensure_ascii=False ) ) 
            fw.write('\n')
    return 


def add_numbers_test(a, b):
    return a+b