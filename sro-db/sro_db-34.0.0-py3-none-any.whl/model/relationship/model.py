from sro_db.config.config import Base
from sqlalchemy import Column ,ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

association_sprint_scrum_development_table = Table('sprint_scrum_development_task', Base.metadata,
    Column('scrum_development_task_id', Integer, ForeignKey('scrum_development_task.id')),
    Column('sprint_id', Integer, ForeignKey('sprint.id'))
)

association_sprint_backlog_scrum_development_activity_table = Table('sprint_backlog_scrum_development_task', Base.metadata,
    Column('scrum_development_task_id', Integer, ForeignKey('scrum_development_task.id')),
    Column('sprint_backlog_id', Integer, ForeignKey('sprint_backlog.id'))
)

association_development_task_team_member_table = Table('team_member_scrum_development_task', Base.metadata,
    Column('scrum_development_task_id', Integer, ForeignKey('scrum_development_task.id')),
    Column('team_member_id', Integer, ForeignKey('team_member.id'))
)

association_atomic_user_story_sprint_backlog_table = Table('atomic_user_story_sprint_backlog', Base.metadata,
    Column('atomic_user_story_id', Integer, ForeignKey('atomic_user_story.id')),
    Column('sprint_backlog_id', Integer, ForeignKey('sprint_backlog.id'))
)

association_user_story_sprint_team_member_table = Table('user_story_team_member', Base.metadata,
    Column('user_story_id', Integer, ForeignKey('user_story.id')),
    Column('team_member_id', Integer, ForeignKey('team_member.id'))
)