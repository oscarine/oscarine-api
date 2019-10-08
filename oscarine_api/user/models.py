# -*- coding: utf-8 -*-
"""User models."""

from oscarine_api.database import (
    Column,
    Model,
    SurrogatePK,
    db
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from datetime import datetime


class User(SurrogatePK, Model):
    """A user of the app."""

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(64), index=True, unique=True)
    email = Column(db.String(120), index=True, unique=True)
    password_hash = Column(db.String(128))
    bio = Column(db.String(140))
    last_seen = Column(db.DateTime, default=datetime.utcnow)
    first_name = Column(db.String(25))
    last_name = Column(db.String(25))
    phone_number = Column(db.String(15))
    avatar_image = Column(db.String(120))
    city = Column(db.String(30))
    state = Column(db.String(30))
    role = Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen,
            'bio': self.bio,
            'avatar_image': self.avatar_image,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'city': self.city,
            'state': self.state,
            'role': self.role,
            '_links': {
                'self': url_for('user.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'bio', 'phone_number',
                      'first_name', 'last_name', 'city',
                      'state', 'role']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def __repr__(self):
        return '<User {}>'.format(self.username)
