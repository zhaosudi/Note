import unittest
from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrSetnoteInfolevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    userid = env_config["userid"]
    sid = env_config["sid"]
    path = "/v3/notesvr/set/noteinfo"
    url = host + path
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

    def testCase_major(self):
        """上传/更新便签信息主体主流程"""
        info_log("用户A上传/更新便签信息主体主流程")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

    def testCase01(self):
        """上传/更新便签信息主体_noteId必填项缺失"""
        info_log("上传/更新便签信息主体_noteId必填项为空")
        self.api_data_base.pop("noteId")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        expected_res = {"errorCode": int, "errorMsg": str}
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        ResCheck().res_check(expected_res, res.json())
