from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    alias = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    isActive = db.Column(db.Boolean, default=True)

    roles = db.relationship('Role', secondary='user_roles', back_populates='users') # OK

    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.email}, {self.password}, {self.alias}, {self.isActive}, {self.roles}'
    

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates='roles') # OK
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles') # OK2
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.name}'
    

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=True)
    roles= db.relationship('Role', secondary='role_permissions', back_populates='permissions') # OK2
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.name}'


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    
    created_at = db.Column(db.DateTime,default= datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)
