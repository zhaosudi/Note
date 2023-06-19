import time
import unittest
import requests


class AddNotes(unittest.TestCase):

    def add_Usernote(self, userid, sid, num):
        host = "https://note-api.wps.cn"
        set_noteinfo_path = "/v3/notesvr/set/noteinfo"
        set_notecontent_path = "/v3/notesvr/set/notecontent"

        url1 = host + set_noteinfo_path
        url2 = host + set_notecontent_path
        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}

        noteIds = []
        for i in range(num):
            noteId = str(int(time.time() * 1000))
            noteIds.append(noteId)

            """上传/更新便签信息主体"""
            res1 = requests.post(url=url1, headers=headers, json={"noteId": noteId,
                                                                  "star": 1, "remindTime": 0,
                                                                  "remindType": 0}, timeout=3)
            """上传/更新便签信内容"""
            res2 = requests.post(url=url2, headers=headers, json={"noteId": noteId,
                                                                  "title": "text",
                                                                  "summary": "text",
                                                                  "body": "text",
                                                                  "localContentVersion": 1,
                                                                  "BodyType": 0}, timeout=3)
            self.assertEqual(200, res2.status_code)

        return noteIds
