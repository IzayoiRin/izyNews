import logging

from flask import json, abort
from infos.models import Users, News, Category
from infos.modules import response_code as rc
from infos import constants as ct
from infos.utils.common import Paginate


class IndexLogical(object):
    def __init__(self):
        self.request = None
        self.response = None

    def login_state(self):
        uid = self.request
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

    def main_categroy(self):
        context = {"categories": self._category_con()}
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

    def main_news(self):
        user_fields = ("id", "avatar_url", "name")
        news_fields = ("id", "poster_url", "title", "digest", "source", "create_date")
        cid, page, slide = self.request.get("cid", 1), self.request.get("page", 1),\
                           self.request.get("per_page", ct.HOME_PAGE_MAX_NEWS)
        try:
            cid, page, slide =int(cid), int(page), int(slide)
        except Exception as e:
            logging.error(e)
            return json.jsonify(errno=rc.RET.PARAMERR, errmsg="Error Params")
        filters = list()
        (filters.append(News.category_id == cid)) if cid != 1 else filters
        news, total = self._news_con(page, slide, *filters,
                       user_fields=user_fields, news_fields=news_fields)
        self.response = json.jsonify(errno=rc.RET.OK, data=news, total=total)


    @staticmethod
    def _news_con(page, slide, *filters, user_fields=("id", "name"), news_fields=("id", "title")):
        """
        quert news order by c.create_date
        :param filters: news query condition as SQL WHERE
        :param user_fields: select fields of queried user objects to dict
        :param news_fields: select fields of queried news objects to dict
        :return: arrayDictionary
        """
        filters = [News.is_delete == 0] + list(filters)
        # all_news : queried news object [obj, .....]
        p = Paginate(slide)
        try:
            q = p.alchemyQuery_init(
                News.query.order_by(News.create_date.desc()).filter(*filters)
            ).query(page)
            all_news = q.arrayobj
        except Exception as e:
            logging.error(e)
            return abort(500)
        # pack to arrayDictionary
        news = list()
        for temp_news in all_news:
            # temp_news.user(): user_obj,  user.packDict(): {id: xx, name: xxx, ...}
            temp_user = temp_news.user(Users.is_delete == 0)
            user = temp_user.packDict(*user_fields) if temp_user else ''
            # temp_news.packDict: {id: xx, title: xxx, ...}
            temp = temp_news.packDict(*news_fields)
            # {id: xx, title: xxx, ..., user: {id: xx, name: xxx, ...} or None}
            temp["user"] = user
            news.append(temp)
        return news, q.total  # [{id: xx, title: xx, user: {id: xx, ..} or None}, ......]
