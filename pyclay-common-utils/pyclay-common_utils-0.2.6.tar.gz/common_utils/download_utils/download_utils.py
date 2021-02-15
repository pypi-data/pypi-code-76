import requests
import tarfile, zipfile
from tqdm import tqdm
import math

def download_file(url: str, output_path: str):
    r = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(r.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0 
    with open(output_path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='MB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")  

def tar_extractall(tarfile_path: str, dst_path: str):
    tar = tarfile.open(tarfile_path)
    tar.extractall(dst_path)
    tar.close()

def zip_extractall(zipfile_path: str, dst_path: str):
	zip_ref = zipfile.ZipFile(zipfile_path, 'r')
	zip_ref.extractall(dst_path)
	zip_ref.close()
