import re

INVALID_CHARS = re.compile(r'[^a-zA-Z_]')
REPEATS = re.compile(r'(?P<char>.+)(?P=char){2,}', re.IGNORECASE)
SIDE_DASHES = re.compile(r'^[_-]|[_-]$')


def check_nickname(nickname: str):
    # В идеале этого не должно происходить, но пусть будет
    if len(nickname) == 0:
        return ['Никнейм не может быть пустым']

    result = []

    if len(nickname) < 3 or len(nickname) > 16:
        result.append('Ник должен быть длиной от 3 до 16 символов')

    if INVALID_CHARS.search(nickname):
        result.append((
            'Ник может состоять только из английских '
            'букв или нижнего подчёркивания'
        ))

    if REPEATS.search(nickname):
        result.append((
            'Ник не должен содержать '
            'повторов из трёх и более символов'
        ))

    if re.search(SIDE_DASHES, nickname):
        result.append((
            'Ник не должен содержать подчёркиваний, '
            'дефисов и прочих украшений по краям'
        ))

    return result


def texture_path_handler(instance, filename: str) -> str:
    return f'{instance.token.uuid}/{filename}'
