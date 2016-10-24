from sqlalchemy import Column
from appmon.extensions import db


class HitCount(db.Model):

    __tablename__ = 'hit_count'

    id = Column(db.Integer, primary_key=True)
    endpoint = Column(db.String(), nullable=False, unique=True)
    hit_count = Column(db.Integer)