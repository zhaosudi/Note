import unittest
from common.read_yml import ReadYaml
from common.resCheck import ResCheck
from common.logs_create import info_log, log_class_methods, error_log
from business_common.request_demo import RequestsDemo
import time
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrSetNotecontentlevel2(unittest.TestCase):
    env_config = ReadYaml.env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    set_notecontent_path = "/v3/notesvr/set/notecontent"
    set_noteinfo_path = "/v3/notesvr/set/noteinfo"
    get_notebody_path = "/v3/notesvr/get/notebody"
    url1 = host + set_noteinfo_path
    url2 = host + set_notecontent_path
    url3 = host + get_notebody_path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_01(self):
        """上传/更新便签内容_noteId为0"""
        data2 = {"noteId": str(int(time.time() * 1000)),
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用户A上传/更新便签内容主流程_noteId为0")
        data2["noteId"] = 0
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res1, res1.json())
        self.assertEqual(500, res1.status_code)
        self.assertEqual(-7, res1.json()["errorCode"])
        info_log(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{res1.json()}")

    def testCase_02(self):
        """上传/更新便签内容_noteId为1.5"""
        data2 = {"noteId": str(int(time.time() * 1000)),
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用户A上传/更新便签内容主流程_noteId为1.5")
        data2["noteId"] = 1.5
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res1, res1.json())
        self.assertEqual(500, res1.status_code)
        self.assertEqual(-7, res1.json()["errorCode"])
        info_log(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{res1.json()}")

    def testCase_03(self):
        """上传/更新便签内容_noteId为None"""
        data2 = {"noteId": str(int(time.time() * 1000)),
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用户A上传/更新便签内容主流程_noteId为None")
        data2["noteId"] = None
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res1, res1.json())
        self.assertEqual(500, res1.status_code)
        self.assertEqual(-7, res1.json()["errorCode"])
        info_log(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{res1.json()}")

    def testCase_04(self):
        """上传/更新便签内容_noteId为中文"""

        data2 = {"noteId": str(int(time.time() * 1000)),
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用户A上传/更新便签内容主流程_noteId为中文")
        data2["noteId"] = "中文"
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res1, res1.json())
        self.assertEqual(500, res1.status_code)
        self.assertEqual(-7, res1.json()["errorCode"])
        info_log(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{res1.json()}")
