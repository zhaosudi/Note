import unittest
from common.resCheck import ResCheck
from common.read_yml import ReadYaml
from common.logs_create import info_log,log_class_methods
from business_common.request_demo import RequestsDemo
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernotegroup import AddNotesgroup
import time
from business_common.delete_notegroup import DeleteNotegroup

@log_class_methods
class NotesvrGetNotegrouplevel1(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    api_data_base={"excludeInvalid":"true"}
    set_nodegroup_path = "/v3/notesvr/get/notegroup"
    url = host + set_nodegroup_path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")



    def testCase_major(self):
        """"获取分组列表主流程"""
        groupId = str(int(time.time() * 1000))
        info_log("用户A新增分组便签")
        res_group = AddNotesgroup().add_Usernotegroup(userid=self.userid, sid=self.sid, num=3, groupId=groupId)
        info_log(f"{res_group}")

        info_log("获取分组列表主流程")
        res=RequestsDemo().post(url=self.url,userid=self.userid,sid=self.sid,data=self.api_data_base)
        self.assertEqual(200,res.status_code)
        expect_res={"noteGroups":list,"requestTime":int}
        ResCheck().res_check(expect_res, res.json())
        expect_res_son={"userId":str,"groupId":str,"groupName":str,"order":int,"valid":int,"updateTime":int}
        ResCheck().res_check(expect_res_son, res.json()["noteGroups"][0])

    def tearDown(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")
        info_log("清空该用户所有分组")
        res1 = DeleteNotegroup().delete_notegroup(self.userid, self.sid)
        self.assertEqual(True, res, msg="Delete Notegroup error!")



