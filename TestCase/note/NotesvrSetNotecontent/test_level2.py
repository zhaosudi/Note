import unittest
from common.read_yml import ReadYaml
from common.resCheck import ResCheck
from common.logs_create import info_log, log_class_methods, error_log
from business_common.request_demo import RequestsDemo
import time
from parameterized import parameterized
from business_common.clean_Usernote import ClearNotes
from business_common.add_Usernote import AddNotes
from business_common.Get_Usernote import GetNotes


@log_class_methods
class NotesvrSetNotecontentlevel2(unittest.TestCase):
    env_config = ReadYaml.env_yaml("config.yml")
    host = env_config["host"]
    sid = env_config["sid"]
    userid = env_config["userid"]
    set_notecontent_path = "/v3/notesvr/set/notecontent"
    set_noteinfo_path = "/v3/notesvr/set/noteinfo"
    get_notebody_path = "/v3/notesvr/get/notebody"
    url1 = host + set_noteinfo_path
    url2 = host + set_notecontent_path
    url3 = host + get_notebody_path

    def setUp(self) -> None:
        """清空该用户所有便签"""
        info_log("清空该用户所有便签")
        res = ClearNotes().clean_Usernote(self.userid, self.sid)
        self.assertEqual(True, res, msg="clear notes error!")

    BodyType_num = ([{"BodyType": 0, "code": 200}], [{"BodyType": 1, "code": 200}])

    @parameterized.expand(BodyType_num)
    def testCase01(self, BodyType_num):
        """上传/更新便签主体不同枚举值_BodyType"""
        noteId = str(int(time.time() * 1000))
        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("上传/更新便签主体")
        res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

        info_log("用户A上传/更新便签信息BodyType枚举值")
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        self.assertEqual(200, res1.status_code)
        ResCheck().res_check(expected_res1, res1.json())
        info_log(f"{res1.json()}")

    def testCase02(self):
        """已存在 noteId，更新便签主体内容"""
        info_log("添加便签")
        num = 1
        """添加便签方法中的data{"noteId": noteId,
                             "title": "text",
                             "summary": "text",
                             "body": "text",
                             "localContentVersion": 1,
                             "BodyType": 0}")"""

        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")
        noteId = noteIds[0]

        data = {"noteIds": noteIds}
        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用戶A获取便签内容")

        info_log("上传/更新便签主体")
        res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

        info_log("上传/更新便签内容")
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        self.assertEqual(200, res1.status_code)
        ResCheck().res_check(expected_res1, res1.json())

        info_log("用戶A获取便签内容")
        get_notebody_res = RequestsDemo().post(url=self.url3, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual("abc", get_notebody_res.json()["noteBodies"][0]["title"])
        info_log(f"{get_notebody_res.json()}")

    def testCase03(self):
        """不存在 noteId，上传便签主体内容"""
        noteId = str(int(time.time() * 1000))

        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        data = {"noteIds":[noteId]}

        info_log("上传/更新便签主体")
        res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

        info_log("上传便签内容")
        res1 = RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res1 = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        self.assertEqual(200, res1.status_code)
        ResCheck().res_check(expected_res1, res1.json())

        info_log("用戶A获取便签内容")
        get_notebody_res = RequestsDemo().post(url=self.url3, userid=self.userid, sid=self.sid, data=data)

        exepectget_notebody_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepectget_notebody_res, get_notebody_res.json())
        ResCheck().res_check(exepect_res_son, get_notebody_res.json()["noteBodies"][0])
        self.assertEqual(200, get_notebody_res.status_code)
        """查询便签列表"""
        noteIds = GetNotes().Get_Usernote(self.userid, self.sid)
        expected_noteIds = [noteId]
        self.assertEqual(expected_noteIds, noteIds)
        info_log(f"便签列表{noteIds}")

    def testCase04(self):
        """先上传便签内容，再上传便签主体"""
        noteId = str(int(time.time() * 1000))

        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        data = {"noteIds":[noteId]}
        info_log("上传便签内容")
        res= RequestsDemo().post(url=self.url2, userid=self.userid, sid=self.sid, data=data2)
        expected_res = {"responseTime": int, "contentVersion": int, "contentUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())

        info_log("用戶A获取便签内容")
        get_notebody_res = RequestsDemo().post(url=self.url3, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual(200, get_notebody_res.status_code)
        info_log(f"{get_notebody_res.json()}")
        exepectget_notebody_res = {'responseTime': int, 'noteBodies': list}
        exepect_res_son = {'summary': str, 'noteId': str, 'infoNoteId': str, 'bodyType': int,
                           'body': str, 'contentVersion': int, 'contentUpdateTime': int, 'title': str, 'valid': int}
        ResCheck().res_check(exepectget_notebody_res, get_notebody_res.json())
        ResCheck().res_check(exepect_res_son, get_notebody_res.json()["noteBodies"][0])
        self.assertEqual(200, get_notebody_res.status_code)

        info_log("上传/更新便签主体")
        res = RequestsDemo().post(url=self.url1, userid=self.userid, sid=self.sid, data=data1)
        expected_res = {"responseTime": int, "infoVersion": int, "infoUpdateTime": int}
        self.assertEqual(200, res.status_code)
        ResCheck().res_check(expected_res, res.json())


    def testCase05(self):
        """用户A已存在 noteId，用户B更新便签主体内容"""
        info_log("用户B账号")
        userid01 = 944475270
        info_log("添加便签")
        num = 1
        """添加便签方法中的data{"noteId": noteId,
                             "title": "text",
                             "summary": "text",
                             "body": "text",
                             "localContentVersion": 1,
                             "BodyType": 0}")"""

        noteIds = AddNotes().add_Usernote(self.userid, self.sid, num)
        info_log(f"{noteIds}")
        noteId = noteIds[0]

        data = {"noteIds": noteIds}
        data1 = {"noteId": noteId,
                 "star": 1,
                 "remindTime": 0,
                 "remindType": 0,
                 }
        data2 = {"noteId": noteId,
                 "title": "abc",
                 "summary": "abc",
                 "body": "abc",
                 "localContentVersion": 1,
                 "BodyType": 0}

        info_log("用戶A获取便签内容")

        info_log("上传/更新便签主体")
        res = RequestsDemo().post(url=self.url1, userid=userid01, sid=self.sid, data=data1)
        expected_res = {"errorCode":int,"errorMsg":str}
        self.assertEqual(-1011, res.json()["errorCode"])
        ResCheck().res_check(expected_res, res.json())
        self.assertEqual(412, res.status_code)

        info_log("上传/更新便签内容")
        res1 = RequestsDemo().post(url=self.url2, userid=userid01, sid=self.sid, data=data2)
        expected_res1 = {"errorCode": int, "errorMsg": str}
        self.assertEqual(-1011, res1.json()["errorCode"])
        ResCheck().res_check(expected_res1, res1.json())
        self.assertEqual(412, res1.status_code)


        info_log("用戶A再次获取便签内容")
        get_notebody_res = RequestsDemo().post(url=self.url3, userid=self.userid, sid=self.sid, data=data)
        self.assertEqual("text", get_notebody_res.json()["noteBodies"][0]["title"])
        info_log(f"{get_notebody_res.json()}")





