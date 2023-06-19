import unittest

""" 校验http接口返回值校验
        check：
        ：key:是否存在
        ：value: type 是否正确
        ：len(key): key 数量
        """

class ResCheck(unittest.TestCase):
    def res_check(self,expected_body,response):
        self.assertEqual(len(expected_body.keys()),len(response.keys()))
        for k,v in expected_body.items():
            self.assertIn(k,response.keys())
            self.assertEqual(v,type(response[k]))


# import unittest
#
#
# class ResCheck(unittest.TestCase):
#     def res_check(self, expected_body, response):
#         """
#         校验http接口返回值校验
#         :key: is exist.
#         :value type: true or false.
#         :len(key): actual true.
#         """
#         self.assertEqual(len(expected_body.keys()), len(response.keys()))
#         for k, v in expected_body.items():
#             self.assertIn(k, response.keys())
#             self.assertEqual(v, type(response[k]))

