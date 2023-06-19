import unittest
from common.resCheck import ResCheck
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from common.read_yml import ReadYaml
from business_common.add_Usernote import AddNotes
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesUserlevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    def testCase_major(self):
        """获取首页便签主流程"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")

        info_log("获取用户A的首页便签")
        startindex = 0
        rows = 10
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(200, res.status_code, msg="处理失败")
        expected_res = {"responseTime": int, "webNotes": list}
        ResCheck().res_check(expected_res, res.json())
        expected_res_son = {"noteId": str, "createTime": int, "star": int, "remindTime": int, "remindType": int,
                            "infoVersion": int, "infoUpdateTime": int, "groupId": type(None), "title": str,
                            "summary": str,
                            "thumbnail": type(None), "contentVersion": int, "contentUpdateTime": int}
        ResCheck().res_check(expected_res_son, res.json()["webNotes"][0])
        self.assertEqual(3, len(res.json()["webNotes"]))
        self.assertIn(res.json()["webNotes"][0]["noteId"], noteIds)

    def testCase_01(self):
        """获取用户1的首页便签_userid必填项缺失"""
        info_log("获取用户1的首页便签_必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "")
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_02(self):
        """获取用户1的首页便签_startindex必填项缺失"""
        info_log("获取用户1的首页便签_必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "")
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_03(self):
        """获取用户1的首页便签_rows必填项缺失"""
        info_log("获取用户1的首页便签_必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "")
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())
