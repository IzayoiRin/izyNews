import logging

from flask import json, abort
from infos.models import Users, News, Category
from infos.modules import response_code as rc
from infos import constants as ct
from infos.utils.common import Paginate


class IndexLogical(object):

    def __init__(self):
        self.requset = None
        self.response = None

    def login_state(self):
        uid = self.requset
        if not uid:
            self.response = json.jsonify(errno=rc.RET.SESSIONERR, errmsg="Session Invalid")
        user = Users.packQuery(Users.id == uid)
        select_user = user[0] if user else None
        if select_user:
            self.response = json.jsonify(errno=rc.RET.OK, name=select_user.nick_name, url=select_user.avatar_url)
            return
        self.response = json.jsonify(errno=rc.RET.USERERR, errmsg="Error User")

    def hot_rank(self, *criterion):
        filters = [News.is_delete == 0] + list(criterion)
        try:
            queries = News.query.filter(*filters).order_by(News.hot.desc()).limit(ct.CLICK_RANK_MAX_NEWS).all()
        except Exception as e:
            logging.error(e)
            self.response = json.jsonify(errno=rc.RET.DBERR, errmsg="Query failed")
            return
        tops = [query.packDict("title", "id") for query in queries]
        self.response = json.dumps(tops)

    def main_scoop(self):
        context = {"categories":self._category_con(),
                   "news": self._news_con()}
        return context

    @staticmethod
    def _category_con(*filters, cats_fields=("id", "name")):
        """
        query category
        :param filters: category query condition as SQL WHERE
        :return: arrayDictionary
        """
        filters = [Category.is_delete == 0] + list(filters)
        all_cats = Category.packQuery(*filters)
        cats = [cat.packDict(*cats_fields) for cat in all_cats]
        return cats  # [{id: xx, name: xx}, ......]

    @staticmethod
    def _news_con(*filters, user_fields=("id", "name"), news_fields=("id", "title")):
        """
        quert news order by c.create_date
        :param filters: news query condition as SQL WHERE
        :param user_fields: select fields of queried user objects to dict
        :param news_fields: select fields of queried news objects to dict
        :return: arrayDictionary
        """
        filters = [News.is_delete == 0] + list(filters)
        # all_news : queried news object [obj, .....]
        p = Paginate()
        try:
            p.alchemyQuery_init(News.query.order_by(News.create_date.desc()).filter(*filters))
            all_news = p.query().arrayobj
        except Exception as e:
            logging.error(e)
            return abort(500)
        # pack to arrayDictionary
        news = list()
        for temp_news in all_news:
            # temp_news.user(): [user_obj, ...], user.packDict(): {id: xx, name: xxx, ...}
            user = [(user.packDict("id", "avatar_url", "name") if user else None) for user in temp_news.user(Users.is_delete == 0)]
            # temp_news.packDict: {id: xx, title: xxx, ...}
            temp = temp_news.packDict("id", "poster_url", "title", "digest", "source", "create_date")
            # {id: xx, title: xxx, ..., user: {id: xx, name: xxx, ...} or None}
            temp["user"] = user
            news.append(temp)
        return news  # [{id: xx, title: xx, user: {id: xx, ..} or None}, ......]
