from typing import Optional

from src.Skills import Skills


class Candidate:
    def __init__(self, name: str, title: str, skills: Optional[str]):
        self.skills = Skills(skills_list=skills)
        self.name = name
        self.title = title

    def __str__(self):
        return f'------------------\nCandidate\n------------------\nName: {self.name}\nTitle: {self.title}\nSkills:' \
               f'\n{self.skills}'
