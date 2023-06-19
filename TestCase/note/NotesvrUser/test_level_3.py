import unittest
from common.resCheck import ResCheck
from business_common.request_demo import RequestsDemo
from common.logs_create import info_log, log_class_methods
from common.read_yml import ReadYaml
from business_common.clean_Usernote import ClearNotes


@log_class_methods
class NotesUserlevel3(unittest.TestCase):
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

    def testCase_01(self):
        """获取用户1的首页便签_startindex为中文"""
        info_log("获取用户1的首页便签__startindex为中文")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "中文")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_02(self):
        """获取用户1的首页便签_startindex为***&……"""
        info_log("获取用户1的首页便签__startindex为***&……")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "***&……")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_03(self):
        """获取用户1的首页便签_startindex为1.5"""
        info_log("获取用户1的首页便签__startindex为1.5")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "1.5")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_04(self):
        """获取用户1的首页便签_startindex为None"""
        info_log("获取用户1的首页便签__startindex为None")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "None")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_05(self):
        """获取用户1的首页便签_startindex为-1"""
        info_log("获取用户1的首页便签__startindex为-1")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "-1")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_06(self):
        """获取用户1的首页便签_rows为中文"""
        info_log("获取用户1的首页便签__rows为中文")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "中文")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_07(self):
        """获取用户1的首页便签_rows为***&……"""
        info_log("获取用户1的首页便签__rows为***&……")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "***&……")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_08(self):
        """获取用户1的首页便签_rows为1.5"""
        info_log("获取用户1的首页便签__rows为1.5")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{startindex}", "1.5")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_09(self):
        """获取用户1的首页便签_rows为None"""
        info_log("获取用户1的首页便签__rows为None")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "None")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_10(self):
        """获取用户1的首页便签_rows为-1"""
        info_log("获取用户1的首页便签__rows为-1")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{rows}", "-1")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_11(self):
        """获取用户1的首页便签_userid为中文"""
        info_log("获取用户1的首页便签__userid为中文")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "中文")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_12(self):
        """获取用户1的首页便签_userid为***&……"""
        info_log("获取用户1的首页便签__userid为***&……")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "***&……")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_13(self):
        """获取用户1的首页便签_userid为1.5"""
        info_log("获取用户1的首页便签__userid为1.5")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "1.5")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_14(self):
        """获取用户1的首页便签_userid为None"""
        info_log("获取用户1的首页便签__userid为None")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "None")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())

    def testCase_15(self):
        """获取用户1的首页便签_userid为-1"""
        info_log("获取用户1的首页便签__userid为-1")
        startindex = 0
        rows = 0
        path = f"/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes"
        path = path.replace(f"{self.userid}", "-1")
        url = "https://" + self.host + path
        res = RequestsDemo().get(url, self.userid, self.sid)
        self.assertEqual(500, res.status_code, msg="No message available")
        expected_res = {"errorCode": int, "errorMsg": str}
        ResCheck().res_check(expected_res, res.json())
