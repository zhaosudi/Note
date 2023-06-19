import unittest
import time
from copy import deepcopy
from common.resCheck import ResCheck
from common.read_yml import ReadYaml
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from parameterized import parameterized
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrWebGetnotesgroupevel3(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    print(env_config)
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    path = "/v3/notesvr/web/getnotes/group"
    url = host + path
    api_data_base = {"groupId": str(int(time.time() * 1000)),
                     "startIndex": 0,
                     "rows": 1}

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    @parameterized.expand(("startIndex", "rows"))
    def testCase_02(self, key):
        """查看分组下便签rows必填项缺失"""
        info_log("用户A查看分组下便签必填项rows缺失")
        data = deepcopy(self.api_data_base)
        data.pop(key)
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())
