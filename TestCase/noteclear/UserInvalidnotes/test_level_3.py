import unittest
from common.resCheck import ResCheck
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from common.read_yml import ReadYaml
from parameterized import parameterized
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class UserInvalidnoteslevel3(unittest.TestCase):
    env_config = ReadYaml().env_yaml("config.yml")
    print(env_config)
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]


    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    userid_NoInt = ([{"userid": "中文", "code": 500}], [{"userid": None, "code": 500}],
                    [{"userid": list, "code": 500}])
    @parameterized.expand(userid_NoInt)
    def testCase_01(self, userid_NoInt):
        """查看回收站下便签列表userid为其他不合法值"""
        info_log("查看回收站下便签列表userid为其他不合法值")
        startindex = 0
        rows = 10
        userid=userid_NoInt["userid"]
        path = f"/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes"
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        expected_res = {"errorCode": int, "errorMsg": str}
        self.assertEqual(500, res.status_code, msg="参数不合法！")
        self.assertEqual(-7, res.json()["errorCode"])
        ResCheck().res_check(expected_res, res.json())

    def testCase_02(self):
        """查看回收站下便签列表userid为-1"""
        info_log("查看回收站下便签列表userid为其他不合法值")
        startindex = 0
        rows = 10
        userid=-1
        path = f"/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes"
        url = self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        expected_res = {"errorCode": int, "errorMsg": str}
        self.assertEqual(-412, res.status_code, msg="参数不合法！")
        self.assertEqual(-1011, res.json()["errorCode"])
        ResCheck().res_check(expected_res, res.json())
