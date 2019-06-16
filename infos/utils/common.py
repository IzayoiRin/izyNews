import logging
from infos import constants as ct
from infos.models import DatabaseError


class Paginate(object):

    def __init__(self, slide_window=ct.HOME_PAGE_MAX_NEWS, error_echo=False):
        self.slide = slide_window
        self.error_echo = error_echo
        self.query_sql = None
        self.query_set = None

    def alchemyQuery_init(self, alchemy_query_sql):
        self.query_sql = alchemy_query_sql
        return self

    def query(self, page=1):
        if self.query_sql is None:
            raise DatabaseError("No query sql, use 'alchemyQuery_init()' first")
        try:
            self.query_set = self.query_sql.paginate(page, self.slide, self.error_echo)
        except Exception as e:
            logging.error(e)
            raise DatabaseError("Bad Database Connection")
        return self

    @property
    def arrayobj(self):
        if self.query_set is None:
            return
        return self.query_set.items

    @property
    def current(self):
        if self.query_set is None:
            return
        return self.query_set.page

    @property
    def total(self):
        if self.query_set is None:
            return
        return self.query_set.pages
