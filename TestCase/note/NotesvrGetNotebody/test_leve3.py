import unittest
from common.read_yml import ReadYaml
from common.logs_create import log_class_methods, info_log
from business_common.request_demo import RequestsDemo
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from common.resCheck import ResCheck
from parameterized import parameterized


class NotesvrGetNotebodylevel3(unittest.TestCase):
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

    noteIds = ([{"noteIds": "中文", "code": 500}], [{"noteIds": "#$", "code": 500}], [{"noteIds": 123, "code": 500}],
               [{"noteIds": -1, "code": 500}], [{"noteIds": 0, "code": 200}], [{"noteIds": "#$", "code": 500}],
               [{"noteIds": 123, "code": 500}], [{"noteIds": -1, "code": 500}], [{"noteIds": None, "code": 500}])

    @parameterized.expand(noteIds)
    def testCase_01(self, noteIds):
        """获取便签内容必填项为其他值"""
        info_log("获取便签内容必填项为其他值失")
        data = {"noteIds": noteIds["noteIds"]}

        res = RequestsDemo().post(url=self.url, userid=self.userid, sid=self.sid, data=data)
        exepect_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(exepect_res, res.json())
        self.assertEqual(500, res.status_code)
        self.assertEqual(-7, res.json()["errorCode"])
