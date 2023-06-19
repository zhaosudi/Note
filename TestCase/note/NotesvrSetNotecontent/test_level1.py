import unittest
from common.read_yml import ReadYaml
from common.resCheck import ResCheck
from common.logs_create import info_log, log_class_methods, error_log
from business_common.request_demo import RequestsDemo
import time
from parameterized import parameterized
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrSetNotecontentlevel1(unittest.TestCase):
    env_config = ReadYaml.env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    set_notecontent_path = "/v3/notesvr/set/notecontent"
    set_noteinfo_path = "/v3/notesvr/set/noteinfo"
    url1 = host + set_noteinfo_path
    url2 = host + set_notecontent_path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """上传/更新便签信息主体"""
        noteId = str(int(time.time() * 1000))
        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用户A上传/更新便签信息主体主流程")
        res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

        """上传/更新便签内容主流程"""
        info_log("用户A上传/更新便签内容主流程")
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        self.assertEqual(200, res1.status_code)
        ResCheck().res_check(expected_res1, res1.json())
        info_log(f"{res1.json()}")

    @parameterized.expand(("noteId", "title", "summary", "body", "localContentVersion", "BodyType"))
    def testCase01(self, key):
        """上传/更新便签内容_必填项缺失"""
        noteId = str(int(time.time() * 1000))
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("上传/更新便签内容_必填noteId项缺失")
        data2.pop(key)
        res = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res = {"errorCode": int, "errorMsg": str}
        self.assertEqual(500, res.status_code, msg="参数不合法！")
        self.assertEqual(-7, res.json()["errorCode"])
        ResCheck().res_check(expected_res, res.json())
