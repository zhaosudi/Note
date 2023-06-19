import unittest

from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.add_Usernote import AddNotes
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrDeletelevel2(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    path = "/v3/notesvr/delete"
    url = host + path
    api_data_base = {"noteId": str(int(time.time() * 1000))}

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_01(self):
        """该用户存在便签删除便签"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户A删除便签")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(200, res.status_code)
        expect_res = {"responseTime": int}
        ResCheck().res_check(expect_res, res.json())

    def testCase_02(self):
        """删除该用户不存在便签便签"""
        info_log("用户A删除便签")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(200, res.status_code)
        expect_res = {"responseTime": int}
        ResCheck().res_check(expect_res, res.json())

    def testCase_03(self):
        """该用户不存在便签,删除便签"""
        info_log("用户A删除便签")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(200, res.status_code)
        expect_res = {"responseTime": int}
        ResCheck().res_check(expect_res, res.json())

    def testCase_04(self):
        """用户B删除用户A便签删除便签"""
        info_log("用户A添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户B删除用户A便签删除便签")
        userid=944475270
        res = RequestsDemo().post(url=self.url, userid=userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(412, res.status_code)
        self.assertEqual(-1011, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())
