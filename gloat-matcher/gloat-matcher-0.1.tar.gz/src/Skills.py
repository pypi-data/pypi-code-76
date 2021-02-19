class Skill:

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Skills:
    def __init__(self, skills_list: [str]):
        self.__skills = list(map(lambda x: Skill(x), skills_list))

    def __str__(self):
        res = ""
        for skill in self.__skills:
            res += f'   - {skill}\n'
        return res

    def get_list(self):
        return list(map(lambda x: x.name.lower(), self.__skills))
