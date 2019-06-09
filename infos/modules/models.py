from Activation import db
import datetime


class Users(db.Model):

    id =  db.Column(db.Integer, primary_key=True, nullable=False)
    nick_name = db.Column(db.String(20), nullable=False)
    pwd = db.Column(db.String(12), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    gender = db.Column(db.BOOLEAN, nullable=False, default=1)
    avatar_url = db.Column(db.String(40))
    signature = db.Column(db.String(100))
    create_date = db.Column(db.DATE, default=datetime.datetime.now())
    last_login = db.Column(db.DATE)
    is_admin = db.Column(db.BOOLEAN, default=0)
    is_delete = db.Column(db.BOOLEAN, default=0)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.nick_name)


class News(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(20), nullable=False)
    poster_url = db.Column(db.String(40))
    content = db.Column(db.String(255))
    create_date = db.Column(db.DATE, default=datetime.datetime.now())
    digest = db.Column()
    hot = db.Column(db.Integer)
    status = db.Column()
    is_delete = db.Column(db.BOOLEAN, default=0)
    category_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.title)


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.id, self.name)


class Fans(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    star_id = db.Column(db.Integer, nullable=False)
    fan_id = db.Column(db.Integer, nullable=False)
    is_delete = db.Column(db.BOOLEAN, default=0)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.star_id, self.fan_id)


class Collection(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    news_id = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DATE, default=datetime.datetime.now())
    is_delete = db.Column(db.BOOLEAN, default=0)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.news_id)


class Comments(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    news_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255))
    create_date = db.Column(db.DATE, default=datetime.datetime.now())
    likes = db.Column(db.Integer)
    is_delete = db.Column(db.BOOLEAN, default=0)
    parent_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.news_id)


class Agreements(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__tablename__, self.user_id, self.comment_id)


if __name__ == '__main__':
    db.create_all()
