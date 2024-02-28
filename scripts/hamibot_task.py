import os
import requests
import sys
import json


class VxPusher:
    def __init__(self, token, need_report, uid) -> None:
        self.token = token
        self.need_report = need_report
        self.uid = uid

    def report(self, content: str, title='脚本执行失败'):
        if self.need_report:
            webapi = 'http://wxpusher.zjiecode.com/api/send/message'
            data = {
                "appToken": self.token,
                "content": content,
                "summary": title,  # 该参数可选，默认为 msg 的前10个字符
                "contentType": 1,
                "uids": [self.uid, ],
            }
            result = requests.post(url=webapi, json=data)

            print("--- 发送运行错误报告 ---")
            print(f"{title}:{content}")
        else:
            print('没有配置Vxpusher uid，不发送报告')
            print(f"{title}:{content}")


class HamibotConfig:
    def __init__(self, token, paras, name, wechat_uid) -> None:
        self.token = token
        self.paras = paras
        self.name = name
        self.need_report = False
        self.uid = None
        if wechat_uid and len(wechat_uid) > 0:
            self.need_report = True
            self.uid = wechat_uid

    def is_effective(self, json_data):
        """判断配置是否启用

        Args:
            json_data (str): 变量配置

        Returns:
            bool: 启用结果
        """
        if "enable" in json_data:
            return json_data["enable"]
        else:
            return True


def run(token, script, robots, type_str):
    print(f"script:{script}")
    print(f"robots:{robots}")

    url = f"https://api.hamibot.com/v1/{type_str}/{script}/run"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "robots": robots
    }
    response = requests.post(url, headers=headers, json=data)

    print("HTTP 状态码:", response.status_code)
    print("响应内容:", response.text)
    return response


def run_script(token, script, robots):
    """运行发布脚本

    Args:
        token (_type_): _description_
        script (_type_): _description_
        robots (_type_): _description_
    """
    return run(token, script, robots, 'scripts')


def run_dev_script(token, script, robots):
    """运行调试脚本

    Args:
        token (_type_): _description_
        script (_type_): _description_
        robots (_type_): _description_
    """
    return run(token, script, robots, 'devscripts')


if __name__ == "__main__":
    # 获取环境变量
    HAMIBOT_TOKEN = os.getenv("HAMIBOT_TOKEN")
    HAMIBOT_PARAS = os.getenv("HAMIBOT_PARAS")
    WECHAT_UID = os.getenv("WECHAT_UID")
    WXPUSHER_TOKEN = os.getenv("WXPUSHER_TOKEN")
    RUN_SCRIPT_NAME = os.getenv("RUN_SCRIPT_NAME")
    print(HAMIBOT_TOKEN)
    print(HAMIBOT_PARAS)
    print(WECHAT_UID)
    print(WXPUSHER_TOKEN)
    print(RUN_SCRIPT_NAME)
    # 构建配置信息
    user_config = HamibotConfig(HAMIBOT_TOKEN, HAMIBOT_PARAS, RUN_SCRIPT_NAME, WECHAT_UID)
    pusher = VxPusher(WXPUSHER_TOKEN, user_config.need_report, user_config.uid)

    try:
        data = json.loads(user_config.paras)
    except json.JSONDecodeError:
        pusher.report(f"解析参数失败，可能是Hamibot参数格式设置错误\n:{user_config.paras}")
        sys.exit(1)

    matching_key = next((key for key in data if key.upper()
                         == user_config.name.upper()), None)

    if matching_key is not None:
        value = data[matching_key]
        if user_config.is_effective(value):
            result = run_dev_script(
                user_config.token, value["script"], value["robots"])
            if result.ok:
                print('脚本调用成功')
            else:
                # 调用失败，推送消息
                pusher.report(
                    f"{result.status_code}\n{result.content}", 'Hamibot接口调用异常')
        else:
            print("当前配置没有启用，本次不执行脚本")
    else:
        pusher.report(f"没有获取到 '{user_config.name}' 对应的参数，请检查配置是否正确")
