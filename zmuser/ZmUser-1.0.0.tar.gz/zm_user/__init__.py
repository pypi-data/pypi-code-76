from zm_user.conf import Config


class ZmUser(object):
    def __init__(self, db):
        self.db = db
        Config.zm_user_db = db
        from zm_user.models.base import Base
        from zm_user.views.bb import bb_bp
        self.bb_bp = bb_bp

        # 声明 用户 Model
        from zm_user.models.user import User
        self.User = User

        # 声明 角色 Model
        from zm_user.models.role import Role
        self.Role = Role

        # 声明 权限 Model
        from zm_user.models.role import Role
        self.Role = Role
