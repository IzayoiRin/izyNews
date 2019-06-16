import logging
from werkzeug.security import generate_password_hash, check_password_hash
from infos import DB as db
from datetime import datetime


class DatabaseError(Exception):
    pass


class BaseClass(object):
    """The Basic Class of every Model Class has 3 common columns such as id, is_delete, create_date"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_delete = db.Column(db.BOOLEAN, default=False)
    create_date = db.Column(db.DateTime, default=datetime.now)
    # 记录的更新时间
    update_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def packQuery(cls, *criterion):
        try:
            res = db.session.query(cls).filter(*criterion).all()
        except Exception as e:
            logging.error(e)
            raise DatabaseError("Bad Database Connection")
        else:
            return res

    def packDict(self, *fields):
        res = dict()
        for field in fields:
            val = getattr(self, field, None)
            if val is None:
                raise DatabaseError("No Such Field")
            if isinstance(val, datetime):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            res[field] = val
        return res


class Users(BaseClass, db.Model):

    nick_name = db.Column(db.String(20), nullable=False)
    # sha256 encoding password
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    gender = db.Column(
        db.Enum("Female", "Male"),
        nullable=False, default="Male")
    avatar_url = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    last_login = db.Column(db.DATE)
    is_admin = db.Column(db.BOOLEAN, default=0)

    @property
    def encode_pwd(self):
        raise DatabaseError("Security Attribution")

    @encode_pwd.setter
    def encode_pwd(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_pwd(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def add_raw(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise DatabaseError("No Such Field")
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise DatabaseError("Commit Failed")

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.nick_name)


class News(BaseClass, db.Model):

    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(63), nullable=False)
    poster_url = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    digest = db.Column(db.String(511), nullable=False)
    hot = db.Column(db.Integer)
    # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    status = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer)
    # 未通过原因，status = -1 的时候使用
    reason = db.Column(db.String(256))

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.title)

    def user(self, *filters):
        try:
            return self.join_users()\
                .filter(*filters)\
                .filter_by(id=self.id)\
                .first()
        except Exception as e:
            logging.error(e)
            raise DatabaseError("Bad Database Connection")

    @classmethod
    def join_users(cls, *filters):
        try:
            return db.session.query(Users, cls)\
                .select_from(cls)\
                .join(Users, Users.id == cls.user_id)\
                .filter(*filters)
        except Exception as e:
            logging.error(e)
            raise DatabaseError("Bad Database Connection")


class Category(BaseClass, db.Model):

    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.name)


class Fans(BaseClass, db.Model):

    star_id = db.Column(db.Integer, nullable=False)
    fan_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.star_id, self.fan_id)


class Collection(BaseClass, db.Model):

    user_id = db.Column(db.Integer, nullable=False)
    news_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.news_id)


class Comments(BaseClass, db.Model):

    user_id = db.Column(db.Integer, nullable=False)
    news_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255))
    likes = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.news_id)


class Agreements(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.comment_id)
