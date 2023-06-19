import unittest
from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrDeletelevel3(unittest.TestCase):
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
        ClearNotes().clean_Usernote(self.userid, self.sid)

    def testCase_01(self):
        """删除便签noteId中文"""
        info_log("删除便签noteId中文")
        self.api_data_base["noteId"] = "中文"
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())

    def testCase_02(self):
        """删除便签noteId为None"""
        info_log("删除便签noteId为None")
        self.api_data_base["noteId"] = None
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())

    def testCase_02(self):
        """删除便签noteId为**&^%"""
        info_log("删除便签noteId为**&^%")
        self.api_data_base["noteId"] = "为**&^%"
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())

    def testCase_02(self):
        """删除便签noteId为0"""
        info_log("删除便签noteId为0")
        self.api_data_base["noteId"] = 0
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())
