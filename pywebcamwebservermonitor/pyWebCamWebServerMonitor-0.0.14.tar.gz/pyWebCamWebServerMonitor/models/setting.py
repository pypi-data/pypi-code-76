from pyWebCamWebServerMonitor import db

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(255), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Setting %r>' % self.name
