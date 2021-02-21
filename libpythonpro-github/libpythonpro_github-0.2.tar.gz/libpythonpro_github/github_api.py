import requests


def buscar_avatar(usuario: str) -> str:
    """
    Busca avatar no GitHub

    Args: usuario (str): usuário no github
    Return: str com o link do avatar
    """

    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == "__main__":
    usuario = input("Digite o nome do usuário: ")
    print(buscar_avatar(usuario))
