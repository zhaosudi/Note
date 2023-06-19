import unittest
import time
from copy import deepcopy

from common.resCheck import ResCheck
from common.read_yml import ReadYaml
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernotegroup import AddNotesgroup
from business_common.delete_notegroup import DeleteNotegroup


@log_class_methods
class NotesvrSetNotegrouplevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    print(env_config)
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    getnotes_group_path = "/v3/notesvr/web/getnotes/group"
    url = host + getnotes_group_path


    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")

    def testCase_major(self):
        """查看分组下便签"""
        groupId = str(int(time.time() * 1000))
        data = {"groupId": groupId,
                "startIndex": 0,
                "rows": 1}

        info_log("用户A新增分组便签")
        res_group=AddNotesgroup().add_Usernotegroup(userid=self.userid,sid=self.sid,num=3,groupId=groupId)
        info_log(f"{res_group}")
        info_log("获取用户A的首页便签")
        startindex = 0
        rows = 10
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        url = self.host + path
        res_user = RequestsDemo().get(url, self.userid, self.sid)
        info_log(f"{res_user.json()}")
        info_log("查看用户A分组下便签")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(200, res.status_code, msg="处理成功")
        expected_res = {"responseTime": int, "webNotes": list}
        ResCheck().res_check(expected_res, res.json())
        expected_res_son = {"noteId": str, "createTime": int, "star": int, "remindTime": int, "remindType": int,
                            "infoVersion": int, "infoUpdateTime": int, "groupId": type(None), "title": str,
                            "summary": str,
                            "thumbnail": type(None), "contentVersion": int, "contentUpdateTime": int}
        ResCheck().res_check(expected_res_son, res.json()["webNotes"][0])

    def testCase_01(self):
        """查看分组下便签groupId必填项缺失"""
        info_log("用户A新增分组必填项groupId缺失")
        data = {"groupId": "",
                "startIndex": 0,
                "rows": 1}
        data.pop("groupId")
        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=self.data)
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def tearDown(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")