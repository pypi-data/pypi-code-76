from typing import Optional

from src.Skills import Skills


class Job:

    def __init__(self, title, skills: Optional[str]):
        self.title = title
        self.skills = Skills(skills_list=skills)


