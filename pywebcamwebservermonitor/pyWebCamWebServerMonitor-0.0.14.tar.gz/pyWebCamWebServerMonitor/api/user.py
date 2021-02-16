from pyWebCamWebServerMonitor import auth, db
from flask import current_app, Blueprint, render_template, jsonify, g, request
from pyWebCamWebServerMonitor.models.user import User

user = Blueprint('user', __name__, url_prefix='/api/user')



def reset_admin_password():
   user = User.query.filter_by(username='admin').first()
   user.hash_password('admin')
   db.session.commit()
   print("Admin Password was reset to: admin")


@user.route('is-password-admin')
def is_pass_admin():
    user = User.query.filter_by(username='admin').first()
    return  jsonify(error=False, isPassAdmin=user.is_pass_admin())
   

@user.route('change/password', methods=['POST'])
@auth.login_required
def _change_password():
   password = request.json.get('password')
   if password is None:
      return  jsonify(error=True, msg='No password submited')
   if ' ' in password:
      return  jsonify(error=True, msg='Password should not contain a space')
   user = User.query.filter_by(username='admin').first()
   user.hash_password(password)
   db.session.commit()
   return  jsonify(error=False, msg='Password was set to {}'.format(password))



         