from common.read_yml import ReadYaml
import unittest
from business_common.request_demo import RequestsDemo
from common.resCheck import ResCheck
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from common.logs_create import info_log, log_class_methods


@log_class_methods
class NotesvrCleanreCyclebin(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    cleanrecyc_note_path = "/v3/notesvr/cleanrecyclebin"
    url = host + cleanrecyc_note_path
    delete_notes_path = "/v3/notesvr/delete"
    url1 = host + delete_notes_path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """删除/清空回收站便签"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote1(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        for i in noteIds:
            data1 = {"noteId": i}
            info_log("用户A删除便签")
            delete_res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
            self.assertEqual(200, delete_res.status_code)
            delete_expect_res = {"responseTime": int}
            ResCheck().res_check(delete_expect_res, delete_res.json())

            info_log("删除/清空回收站便签")
            data2 = {"noteIds": noteIds}
            res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data2)
            expect_res = {"responseTime": int}
            self.assertEqual(200, res.status_code)
            ResCheck().res_check(expect_res, res.json())

    def testCase_01(self):
        """删除/清空回收站便签必填项缺失"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        for i in noteIds:
            data1 = {"noteId": i}
            info_log("用户A删除便签")
            delete_res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
            self.assertEqual(200, delete_res.status_code)
            delete_expect_res = {"responseTime": int}
            ResCheck().res_check(delete_expect_res, delete_res.json())

            info_log("删除/清空回收站便签")
            data2 = {"noteIds": noteIds}
            data2.pop("noteIds")
            res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data2)
            self.assertEqual(500, res.status_code)
            self.assertEqual(-7, res.json()["errorCode"])
            expect_res = {"errorCode": int, "errorMsg": str}
            ResCheck().res_check(expect_res, res.json())
