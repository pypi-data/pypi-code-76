from ..utils import DictWrapper, dict_prop


class ProjectStatValue(DictWrapper):
    total: int = dict_prop()
    new: int = dict_prop()


class ProjectStat(DictWrapper):
    all: ProjectStatValue = dict_prop(wrapper=ProjectStatValue)
    pkp: ProjectStatValue = dict_prop(wrapper=ProjectStatValue)
    env_check: ProjectStatValue = dict_prop(wrapper=ProjectStatValue)
    tamper: ProjectStatValue = dict_prop(wrapper=ProjectStatValue)
    crash: ProjectStatValue = dict_prop(wrapper=ProjectStatValue)


class Project(DictWrapper):
    id: int = dict_prop()
    name: str = dict_prop()
    demo: bool = dict_prop()
    stat: ProjectStat = dict_prop(wrapper=ProjectStat)
