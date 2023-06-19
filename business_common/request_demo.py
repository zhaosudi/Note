import requests
import json
from common.logs_create import info_log,error_log

class RequestsDemo:

    #self 实例方法，没有被使用，所以声明成静态方法
    @staticmethod
    def get(url,userid,sid):
        headers = {"X-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}
        info_log(f"requests url :{url}")
        info_log(f"requests headers :{headers}")
        res = requests.get(url=url, headers=headers)
        info_log(f"res code :{res.status_code}")
        info_log(f"res body :{res.text}")
        return res

    @staticmethod
    def post(url,userid,sid,data) :
        headers = {"x-user-key": "{}".format(userid),
                   "Content-Type": "application/json",
                   "Cookie": "wps_sid={}".format(sid)}
        info_log(f"requests url :{url}")
        info_log(f"requests body: {json.dumps(data)}")
        info_log(f"requests headers :{headers}")
        res = requests.post(url=url, headers=headers,json=data,timeout=3)
        info_log(f"res code :{res.status_code}")
        info_log(f"res body :{res.text}")
        return res


