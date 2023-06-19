import unittest
import requests
from common.logs_create import info_log


class DeleteNotegroup(unittest.TestCase):
    def delete_notegroup(self, userid, sid):

        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}

        host = "https://note-api.wps.cn"
        set_nodegroup_path = "/v3/notesvr/get/notegroup"
        url = host + set_nodegroup_path
        delete_nodegroup_path = "/v3/notesvr/delete/notegroup"
        url1 = host + delete_nodegroup_path

        res1 = requests.post(url=url, headers=headers, json={"excludeInvalid": "true"}, timeout=3)
        noteGroups = []

        if len(res1.json()["noteGroups"]) > 0:
            pass
        else:
            return True

        for i in res1.json()["noteGroups"]:
            for k, v in i.items():
                if k == "groupId":
                    noteGroups.append(v)
                    res2 = requests.post(url=url1, headers=headers, json={'groupId': v}, timeout=3)

        info_log(f"该用户获取的比便签列表:{res1.json()}")
        info_log(f"删除分组:{res2.json()}")
        if res2.status_code != 200:
            return False
        else:
            return True
