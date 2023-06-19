import time
import unittest
from common.read_yml import ReadYaml
from common.logs_create import log_class_methods, info_log
from business_common.request_demo import RequestsDemo
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from common.resCheck import ResCheck


@log_class_methods
class NotesvrGetNotebodylevel2(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    userid = env_config["userid"]
    sid = env_config["sid"]
    path ="/v3/notesvr/get/notebody"
    url = host + path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_01(self):
        """获取便签内容_返回多个便签内容数据"""
        info_log("添加便签")
        num = 5
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用戶A获取便签内容_返回多个便签内容数据")
        data = {"noteIds": noteIds}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][4])
        self.assertEqual(200, res.status_code)
        self.assertEqual(5, len(res.json()["noteBodies"]))
        self.assertIn(res.json()["noteBodies"][0]["noteId"], noteIds)

    def testCase_02(self):
        """获取便签内容_返回1个便签内容数据"""
        info_log("添加便签")
        num = 1
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用戶A获取便签内容_返回1个便签内容数据")
        data = {"noteIds": noteIds}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][0])
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json()["noteBodies"]))
        self.assertIn(res.json()["noteBodies"][0]["noteId"], noteIds)

    def testCase_03(self):
        """获取便签内容_返回0个便签内容数据"""
        info_log("用戶A获取便签内容_返回0个便签内容数据")
        data = {"noteIds": []}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(exepect_res, res.json())
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])

    def testCase_04(self):
        """获取便签内容_valid：1有效"""
        info_log("添加便签")
        num = 1
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用戶A获取便签内容_返回1个便签内容数据")
        data = {"noteIds": noteIds}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][0])
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json()["noteBodies"]))
        self.assertIn(res.json()["noteBodies"][0]["noteId"], noteIds)
        self.assertEqual(res.json()["noteBodies"][0]["valid"], 1)

    def testCase_05(self):
        """获取便签内容_valid：0，回收站"""
        info_log("添加便签")
        num = 1
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("删除便签")
        dele_data = {"noteId": noteIds[0]}
        res1 = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=dele_data)
        self.assertEqual(200, res1.status_code)
        expect_res1 = {"responseTime": int}
        ResCheck().res_check(expect_res1, res1.json())

        info_log("用戶A获取便签内容_返回1个便签内容数据")
        data = {"noteIds": noteIds}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][0])
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json()["noteBodies"]))
        self.assertIn(res.json()["noteBodies"][0]["noteId"], noteIds)
        self.assertEqual(res.json()["noteBodies"][0]["valid"], 0)

    def testCase_06(self):
        """获取便签内容_valid：2，从回收站删除"""
        data = {"noteIds": str(int(time.time()))}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][0])
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json()["noteBodies"]))
        self.assertEqual(res.json()["noteBodies"][0]["valid"], 2)

