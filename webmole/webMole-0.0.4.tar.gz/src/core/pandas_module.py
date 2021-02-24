import os
import pandas as pd
from core.helper import get_Directory

DEFAULT_FILE_PATH = get_Directory()
print(DEFAULT_FILE_PATH)


# This method load all data inside a Excel (.xlsx) file into a dataFrame
# Argumenst:
#   work_File : The File where it is stored
#   path : path where the file is stored
# noinspection PyBroadException
def load_Data_toDataframe(work_File, path=DEFAULT_FILE_PATH):
    location = os.path.join(DEFAULT_FILE_PATH, work_File)

    df_excel = pd.read_excel(location, index_col=0)  # load all data into a dataframe
    print(f"\n----------> '{work_File}' LOADED")
    return df_excel


# This method loads all data inside a Excel (.xlsx) file from a specific category (Exemple: Link,Name,Store...)
# Argumenst:
#   work_File : The File where it is stored
#   path : path where the file is stored
#   name_of_category: name of what to return

def load_Data_toList(name_of_category, work_File, path=DEFAULT_FILE_PATH, ):
    location = os.path.join(DEFAULT_FILE_PATH, work_File)

    df_excel = load_Data_toDataframe(work_File)
    print(f"\n----------> '{work_File}' LOADED")

    categoryValues_list = df_excel[name_of_category].tolist()

    print(categoryValues_list)

    return categoryValues_list


# This method stores all data inside a Excel (.xlsx) file
# Argumenst:
#   data_dict : The dictonary containing the data to add
#   work_File : The File where it is stored
#   path : path where the file is stored

def write_Data_PD(data_dict, work_File, path=DEFAULT_FILE_PATH):
    location = os.path.join(DEFAULT_FILE_PATH, work_File)

    try:
        print("Entrei no try do write data")
        df_excel = pd.read_excel(location, index_col=0)  # load all data into a dataframe
        print(f"\n----------> '{work_File}' LOADED")

        df_excel2 = pd.DataFrame(data_dict, index=[0])  # load new data into a 2nd dataframe
        df_excel.append(df_excel2, ignore_index=True).to_excel(
            location)  # append the 2 together and save it to the work_File

        print(f"\n----------> Created Stored Data at the File '{work_File}'!")

    except:
        print("Entrei no Except do write data")
        df_excel = pd.DataFrame(data_dict, index=[0])
        df_excel.to_excel(location)
        print(f"\n----------> '{work_File}' does not exist... Created a File and Stored Data at {location}...")

# write_Data_PD(dados2, "teste.xlsx")
# listest = load_Data_toList('Preco', 'teste.xlsx')
