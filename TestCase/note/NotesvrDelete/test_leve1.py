import unittest

from common.read_yml import ReadYaml
import time
from common.logs_create import info_log, log_class_methods
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.add_Usernote import AddNotes
from business_common.clean_Usernote import ClearNotes
from business_common.Get_Usernote import GetNotes

@log_class_methods
class NotesvrDeletelevel1(unittest.TestCase):
    envConfig = ReadYaml().env_yaml("config.yml")#类属性变量用小驼峰
    host = envConfig["host"]
    sid = envConfig["sid"]
    userid = envConfig["userid"]
    delete_path = "/v3/notesvr/delete"
    getnotebody_path = "/v3/notesvr/get/notebody"

    url = host + delete_path
    url1 = host + getnotebody_path


    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """删除便签主流程"""

        info_log("添加便签")
        num = 1
        noteIds=AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")
        apiDataBase = {"noteId": noteIds[0]}

        info_log("用户A删除便签主流程")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=apiDataBase)

        self.assertEqual(200, res.status_code)
        expect_res = {"responseTime": int}
        ResCheck().res_check(expect_res, res.json())

        info_log("查询便签内容")
        apiDataBase1 = {"noteIds":noteIds}
        res1 = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=apiDataBase1)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])


    def testCase_01(self):
        """删除便签noteId必填项缺失"""
        apiDataBase = {"noteId": str(int(time.time() * 1000))}
        info_log("删除便签noteId必填项缺失")
        self.apiDataBase.pop("noteId")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=apiDataBase)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expect_res, res.json())
