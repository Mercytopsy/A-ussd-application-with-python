from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    phone_number = db.Column(db.String(64), unique=True, index=True, nullable=False)

    city = db.Column(db.String(64))
    
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    



class SessionLevel(db.Model):
    __tablename__ = 'session_levels'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Text(128), unique=True)
    phone_number = db.Column(db.String(25))
    level = db.Column(db.Integer, default=0)

    def promote_level(self, level=1):
        self.level = level

    def demote_level(self):
        self.level = 0


