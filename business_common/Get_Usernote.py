import unittest
import requests



class GetNotes(unittest.TestCase):
    def Get_Usernote(self, userid, sid):

        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}

        host = "http://note-api.wps.cn"
        get_noteslist_path = f"/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes"
        url1 = host + get_noteslist_path
        res1 = requests.get(url=url1, headers=headers)
        noteIds = []
        for i in res1.json()["webNotes"]:
            for k, v in i.items():
                if k == "noteId":
                    noteIds.append(v)
        return noteIds
