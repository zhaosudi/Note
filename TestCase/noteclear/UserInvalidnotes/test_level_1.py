import unittest
from common.resCheck import ResCheck
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from common.read_yml import ReadYaml
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
import time


@log_class_methods
class UserInvalidnoteslevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    print(env_config)
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]

    path1 = "/v3/notesvr/delete"
    url1 = host + path1

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")


    def testCase_major(self):
        """添加便签"""
        info_log("添加便签")
        num = 3
        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")
        """删除便签"""

        info_log("用户A删除便签主流程")
        for i in noteIds:
            data1 = {"noteId": i}
            delete_res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)

            self.assertEqual(200, delete_res.status_code)
            delete_expect_res = {"responseTime": int}
            ResCheck().res_check(delete_expect_res, delete_res.json())
        """查看回收站下便签列表主流程"""
        info_log("查看回收站下便签列表")

        startindex = 0
        rows = 10
        path = f"/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes"
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(200, res.status_code, msg="处理成功")
        expected_res = {"responseTime": int, "webNotes": list}
        ResCheck().res_check(expected_res, res.json())
        expected_res_son = {"noteId": str, "createTime": int, "star": int, "remindTime": int, "remindType": int,
                            "infoVersion": int, "infoUpdateTime": int, "groupId": type(None), "title": str,
                            "summary": str,
                            "thumbnail": type(None), "contentVersion": int, "contentUpdateTime": int}
        ResCheck().res_check(expected_res_son, res.json()["webNotes"][0])

    def testCase_01(self):
        """查看回收站下便签列表_userid必填项缺失"""
        info_log("查看回收站下便签列表_userid必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_02(self):
        """查看回收站下便签列表_startindex必填项缺失"""
        info_log("查看回收站下便签列表_startindex必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_03(self):
        """查看回收站下便签列表_rows必填项缺失"""
        info_log("查看回收站下便签列表_rows必填项缺失")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(404, res.status_code, msg="No message available")
        expected_res = {"timestamp": str, "status": int, "error": str, "message": str, "path": str}
        ResCheck().res_check(expected_res, res.json())
