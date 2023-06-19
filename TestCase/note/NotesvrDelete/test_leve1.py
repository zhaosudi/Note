import unittest

from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.add_Usernote import AddNotes
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesvrDeletelevel1(unittest.TestCase):
    envConfig = ReadYaml().env_yaml("config.yml")#类属性变量用小驼峰
    host = envConfig["host"]
    sid = envConfig["sid"]
    userid = envConfig["userid"]
    path = "/v3/notesvr/delete"
    url = host + path
    apiDataBase = {"noteId": str(int(time.time() * 1000))}

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """删除便签主流程"""

        info_log("添加便签")
        num = 3
        noteIds=AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用户A删除便签主流程")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.apiDataBase)

        self.assertEqual(200, res.status_code)
        expect_res = {"responseTime": int}
        ResCheck().res_check(expect_res, res.json())

    def testCase_01(self):
        """删除便签noteId必填项缺失"""
        info_log("删除便签noteId必填项缺失")
        self.api_data_base.pop("noteId")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.apiDataBase)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())
