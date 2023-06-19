import unittest
from common.read_yml import ReadYaml
from common.logs_create import log_class_methods, info_log
from business_common.request_demo import RequestsDemo
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from common.resCheck import ResCheck


@log_class_methods
class NotesvrGetNotebodylevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    userid = env_config["userid"]
    sid = env_config["sid"]
    path = "/v3/notesvr/get/notebody"
    url = host + path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """获取便签内容主流程"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("用戶A获取便签内容")
        data = {"noteIds": noteIds}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepect_res, res.json())
        ResCheck().res_check(exepect_res_son, res.json()["noteBodies"][0])
        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(res.json()["noteBodies"]))
        self.assertIn(res.json()["noteBodies"][0]["noteId"], noteIds)

    def testCase_01(self):
        """获取便签内容必填項缺失"""
        info_log("用戶A获取便签内容必填項缺失")
        data = {}
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(exepect_res, res.json())
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
