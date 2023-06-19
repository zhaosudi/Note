import unittest
import requests
from common.logs_create import info_log


class ClearNotes(unittest.TestCase):
    def clean_Usernote(self, userid, sid):

        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}

        host = "https://note-api.wps.cn"
        get_noteslist_path = f"/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes"
        delete_note_path = "/v3/notesvr/delete"
        clean_recycl_path = "/v3/notesvr/cleanrecyclebin"
        url1 = host + get_noteslist_path
        url2 = host + delete_note_path
        url3 = host + clean_recycl_path
        res1 = requests.get(url=url1, headers=headers)

        if len(res1.json()["webNotes"]) > 0:
            pass
        else:
            return True
        noteIds = []
        for i in res1.json()["webNotes"]:
            for k, v in i.items():
                if k == "noteId":
                    noteIds.append(v)
                    requests.post(url=url2, headers=headers, json={'noteId': v}, timeout=3)
        res3 = requests.post(url=url3, headers=headers, json={"noteIds": noteIds}, timeout=3)
        info_log(f"该用户获取的比便签列表:{res1.json()}")
        info_log(f"res3:{res3.json()}")
        if res3.status_code != 200:
            return False
        else:
            return True
