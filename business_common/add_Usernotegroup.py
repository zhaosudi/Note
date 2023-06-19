import time
import unittest
import requests


class AddNotesgroup(unittest.TestCase):

    def add_Usernotegroup(self, userid, sid, num, groupId):
        host = "https://note-api.wps.cn"
        set_noteinfo_path = "/v3/notesvr/set/noteinfo"
        set_notecontent_path = "/v3/notesvr/set/notecontent"
        set_notegroup_path = "/v3/notesvr/set/notegroup"
        url0 = host + set_notegroup_path
        url1 = host + set_noteinfo_path
        url2 = host + set_notecontent_path
        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}

        noteIds = []
        for i in range(num):
            noteId = str(int(time.time() * 1000))
            noteIds.append(noteId)
            """新增分组"""

            res0 = requests.post(url=url0, headers=headers, json={"groupId": groupId,
                                                                  "groupName": "groupName",
                                                                  "order": 1})

            """上传/更新便签信息主体"""
            res1 = requests.post(url=url1, headers=headers, json={"noteId": noteId,
                                                                  "star": 1, "remindTime": int(time.time() * 1000),
                                                                  "remindType": 0, "groupId": groupId}, timeout=3)
            """上传/更新便签信内容"""
            res2 = requests.post(url=url2, headers=headers, json={"noteId": noteId,
                                                                  "title": "text",
                                                                  "summary": "text",
                                                                  "body": "text",
                                                                  "localContentVersion": 1,
                                                                  "BodyType": 0}, timeout=3)
            self.assertEqual(200, res2.status_code)
        return noteIds
