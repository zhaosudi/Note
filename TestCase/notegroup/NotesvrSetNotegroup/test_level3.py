import unittest
import time
from copy import deepcopy

from common.resCheck import ResCheck
from common.read_yml import ReadYaml
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from business_common.delete_notegroup import DeleteNotegroup
from business_common.clean_Usernote import ClearNotes

@log_class_methods
class NotesvrSetNotegrouplevel3(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    print(env_config)
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    path = "/v3/notesvr/set/notegroup"
    url = host + path
    api_data_base = {"groupId": str(int(time.time() * 1000)),
                     "groupName": "groupName",
                     "order": 1}

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")

    def testCase_01(self):
        """新增分组groupId为空"""
        info_log("用户A新增分组必填项groupId为空")
        data = deepcopy(self.api_data_base)
        data["groupId"] = ""
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.api_data_base)
        self.assertEqual(200, res.status_code)
        expected_res = {"responseTime": int, "updateTime": int}
        ResCheck().res_check(expected_res, res.json())

    def testcase_02(self):
        """新增分组groupName为空"""
        info_log("用户A新增分组必填项groupName为空")
        path = f"/v3/notesvr/set/notegroup"
        url = self.host + path
        data = deepcopy(self.api_data_base)
        data["groupName"] = ""
        res = RequestsDemo().post(url=url, userid=self.userid, sid=self.sid, data=data)

        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testcase_03(self):
        """选填项order缺失"""
        info_log("用户A新增分组必填项order为空")
        path = f"/v3/notesvr/set/notegroup"
        url = self.host + path
        data = deepcopy(self.api_data_base)
        data["order"] = None
        res = RequestsDemo().post(url=url, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(200, res.status_code)
        expected_res = {"responseTime": int, "updateTime": int}
        ResCheck().res_check(expected_res, res.json())

    def tearDown(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")
