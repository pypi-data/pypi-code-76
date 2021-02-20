from flask import Blueprint

from zm_user.models.role import Role
from zm_user.models.user import User
bb_bp = Blueprint('bb_bp', __name__)


@bb_bp.route('/init_user', methods=['get'])
def init_user():
    role = Role._q(Role.level == 0)
    if not role:
        role = Role()
        role.name = "超级管理员"
        role.level = 0
        role.to_save()
    user = User._q(User.role_id == role.id)
    if not user:
        user = User()
        user.role_id = role.id
        user.name = "超级管理员"
        user.to_save()
    print(user.role)
    return "success"
