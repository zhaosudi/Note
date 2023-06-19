import yaml
from main import DIR, Environ

"""
yaml文件特性
1.读取结果是个字典对象
2.文件操作时不会影响原有yml文件数据
3.编写文件时有规范要求，如果编写有误会抛异常
"""


class ReadYaml:
    """读取环境层的配置"""
    @staticmethod
    def env_yaml(filename):
        with open((DIR + Environ)+"/"+filename, "r", encoding="utf-8")as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def api_yaml(filename):
        with open((DIR + r"/data")+"/"+filename, "r", encoding="utf-8")as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def common_yaml(filename):
        with open(filename, "r", encoding="utf-8")as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)


if __name__ == '__main__':
    data = ReadYaml().env_yaml()  # 读取数据
    print(data)



