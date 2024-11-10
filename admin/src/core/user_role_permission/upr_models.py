from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    alias = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    isActive = db.Column(db.Boolean, default=True)
    google_id = db.Column(db.String(120), unique=True, nullable=True)  #para saber si se registro con google
    confirmed = db.Column(db.Boolean, nullable=True) #campo para saber si se confirmo el registro por el administrador


    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    member = db.relationship('Member', secondary='user_member', back_populates='user', uselist=False, lazy=True)
    articles = db.relationship('Article', back_populates='author')

    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'{self.email}, {self.password}, {self.alias}, {self.isActive}, {self.roles}'
    

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'{self.name}'
    

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)
    roles= db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'{self.name}'


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)