from src.core.database import db
from src.core.people.member_rider import Member

class Horse(db.Model):
    """Modelo para los caballos de la institución"""
    __tablename__ = 'horses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    race = db.Column(db.String(32), nullable=False)
    coat = db.Column(db.String(32), nullable=False)
    donation = db.Column(db.Boolean, nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    assigned_location = db.Column(db.String(64), nullable=False)
    assigned_members = db.relationship('Member', secondary='horse_members', backref='horses')
    activities = db.relationship('Activity', secondary='horse_activities', backref='horses')
    documents = db.relationship('HorseDocument', backref='horse', lazy=True)


    def __repr__(self):
        return f'Horse {self.id} - {self.name}'
    
    def __str__(self):
        return f'{self.name}'


horse_members = db.Table('horse_members', 
    db.Column('horse_id', db.Integer, db.ForeignKey('horses.id'), primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True)
)

horse_activities = db.Table('horse_activities',
    db.Column('horse_id', db.Integer, db.ForeignKey('horses.id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True)
)