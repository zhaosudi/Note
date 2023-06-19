import unittest
from logging import info
import requests
from common.read_yml import ReadYaml
from common.logs_create import log_class_methods, info_log
from business_common.request_demo import RequestsDemo
import time
from common.resCheck import ResCheck
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from parameterized import parameterized
from business_common.add_Usernoteremind import AddNotesremind


@log_class_methods
class NotesvrWebGetnotesRemindleve2(unittest.TestCase):
    evn_config = ReadYaml().env_yaml("config.yml")
    host = evn_config["host"]
    sid = evn_config["sid"]
    userid = evn_config["userid"]
    path = "/v3/notesvr/web/getnotes/remind"
    url = host + path
    remindStartTime = int(time.time() * 1000)
    remindEndTime = int(time.time() * 1000)

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_01(self):
        """查看日历下便签_remindStartTime=remindEndTime"""
        info_log("添加日历便签")
        num = 2
        noteIds = AddNotesremind().add_Usernoteremind(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户A查看日历下便签")
        data = {"remindStartTime": int(time.time() * 1000), "remindEndTime": int(time.time() * 1000), "startIndex": 0,
                "rows": 10}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(200, res.status_code, msg="处理异常")
        expected_res = {"responseTime": int, "webNotes": list}
        ResCheck().res_check(expected_res, res.json())


    def testCase_02(self):
        """查看日历下便签_remindStartTime<remindEndTime"""
        info_log("添加日历便签")
        num = 2
        noteIds = AddNotesremind().add_Usernoteremind(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户A查看日历下便签")
        data = {"remindStartTime": 1684200250000, "remindEndTime": int(time.time() * 1000), "startIndex": 0,
                "rows": 10}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(200, res.status_code, msg="处理成功")
        expected_res = {"responseTime": int, "webNotes": list}
        ResCheck().res_check(expected_res, res.json())
        expected_res_son = {"noteId": str, "createTime": int, "star": int, "remindTime": int, "remindType": int,
                            "infoVersion": int, "infoUpdateTime": int, "groupId": type(None), "title": str,
                            "summary": str,
                            "thumbnail": type(None), "contentVersion": int, "contentUpdateTime": int}
        ResCheck().res_check(expected_res_son, res.json()["webNotes"][0])
        self.assertIn(res.json()["webNotes"][0]["noteId"], noteIds)

    def testCase_03(self):
        """查看日历下便签_remindStartTime>remindEndTime"""
        info_log("添加日历便签")
        num = 2
        noteIds = AddNotesremind().add_Usernoteremind(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户A查看日历下便签")
        data = {"remindStartTime": int(time.time() * 1000), "remindEndTime":1684200250000 , "startIndex": 0,
                "rows": 10}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(412, res.status_code, msg="处理异常")
        expected_res = {"errorCode":int,"errorMsg":str}
        ResCheck().res_check(expected_res, res.json())
        self.assertEqual(-7,res.json()["errorCode"])



