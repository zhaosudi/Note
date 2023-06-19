import unittest
from copy import deepcopy
from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from parameterized import parameterized
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrSetnoteInfolevel3(unittest.TestCase):
    env_config = ReadYaml.env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    path = "/v3/notesvr/set/noteinfo"
    url = "http://" + host + path
    api_data_base = {"noteId": str(int(time.time() * 1000)),
                     "star": 1,
                     "remindTime": int(time.time()),
                     "remindType": "1",
                     "groupId": "groupId"}

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    @parameterized.expand(("star", "remindTime", "remindType", "groupId"))
    def testCase01(self, key):
        """上传/更新便签信息选填项校验"""
        info_log("用户上传/更新便签信息选填项")
        data = deepcopy(self.api_data_base)
        data.pop(key)
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        expect_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expect_res, res.json())
