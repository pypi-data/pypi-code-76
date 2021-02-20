import os
from test import app, db
from zm_user import ZmUser

zm = ZmUser(db)
User = zm.User
Role = zm.Role
# 定义蓝图
app.register_blueprint(zm.bb_bp, url_prefix='/bb')


@app.route("/")
def index():
    print(Role._q_all())
    print(User._q_all())
    return "index"


if __name__ == '__main__':
    print("http://0.0.0.0:9999/")
    print("http://0.0.0.0:9999/bb/init_user")
    PORT = int(os.getenv('PORT', 9999))
    app.run(port=PORT, host='0.0.0.0')
