import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class AdvertsImages(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'adverts_images'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    advert_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('adverts.images_id'))
    advert = orm.relationship('Advert')
