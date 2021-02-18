import os
from easygui import diropenbox, fileopenbox, filesavebox

files = []

def selecionar_pasta_com_arquivos(extension):
    pasta = diropenbox('Escolha a pasta com os relatorios')
    return directory_explorer(pasta, extension)

def directory_explorer(dir, extension):
    for arquivo in os.listdir(dir):
        enderecos_arquivo = os.path.join(dir, arquivo)
        if os.path.isfile(enderecos_arquivo):
            if enderecos_arquivo.endswith(extension):
                files.append(enderecos_arquivo)
        else:
            directory_explorer(enderecos_arquivo, extension)
    return files

def dir_to_safe(extension, titulo='Escolha o local para salvar o arquivo'):
    dir = filesavebox(titulo)
    if dir.endswith(extension):
        return dir
    return dir + extension

def fetch_files(extension, messenger='Escolha o arquivo'):
    #return a list of files selected
    return fileopenbox(messenger, multiple=True, filetypes=extension)

def fetch_one_file(extension, messenger='Escolha o arquivo'):
    #return the file selected
    return fileopenbox(messenger, multiple=False, filetypes=extension)