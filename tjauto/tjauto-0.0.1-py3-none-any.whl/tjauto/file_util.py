import os

def read_dir_and_handle(start_path, need_handle, handler):
    entries = os.listdir(start_path)
    for entry in entries:
        dir_path = os.path.join(start_path,entry)
        if os.path.isdir(dir_path) and need_handle(dir_path):
            handler(dir_path)

def read_dict_and_handle_recursive(start_path, dir_name, file_need_handle, file_handler):
    # print("here start" + start_path)
    entries = os.listdir(start_path)
    for entry in entries:
        if os.path.isdir(os.path.join(start_path,entry)):
            # print("here dir")
            read_dict_file(os.path.join(start_path,entry), entry,file_need_handle, file_handler)   
        elif os.path.isfile(os.path.join(start_path,entry)) and need_handle(entry):
            file_handler(os.path.join(start_path,entry), entry, dir_name)    


def get_all_sub_dir(path):
    entries = os.listdir(path)
    return list(filter(lambda x: os.path.isdir(os.path.join(path,x)), entries))
 
