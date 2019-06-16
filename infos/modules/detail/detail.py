from flask import json
from infos.modules import response_code as rc
from infos.models import News
from infos.utils.common import BaseModules


class Detail(BaseModules):

    def main_content(self):
        nid = self.request
        news = News.packQuery(News.id == nid, News.is_delete == 0)[0]
        if not news:
            self.response = json.jsonify(errno=rc.RET.USERERR, errmsg="No Such News")
            return
        return news.packDict("id", "title", "create_date", "source", "digest", "content")
