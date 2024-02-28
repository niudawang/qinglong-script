import os
import requests


def wxpusher_send_by_webapi(msg, summary, app_token, uid):
    """利用 wxpusher 的 web api 发送 json 数据包，实现微信信息的发送"""
    webapi = 'http://wxpusher.zjiecode.com/api/send/message'
    data = {
        "appToken": app_token,
        "content": msg,
        "summary": summary,  # 该参数可选，默认为 msg 的前10个字符
        "contentType": 1,
        "uids": [uid, ],
    }
    result = requests.post(url=webapi, json=data)
    print(result.text)
    return result.text


def get_video_counts(api_url):
    # response = requests.get(api_url)
    # if response.status_code == 200:
    #     data = response.json()
    #     device_counts = data.get('device_counts')
    #     return device_counts
    # else:
    #     print(f"Failed to get video counts from API. Status code: {response.status_code}")
    #     return []
    return [{"device": "1", "video_count": "2", "publish_count": 3},
            {"device": "1", "video_count": "2", "publish_count": 3},
            {"device": "1", "video_count": "2", "publish_count": 3}]


# 配置接口 URL
api_url = "https://example.com/api/video_counts"

# 获取视频数量信息
video_counts = get_video_counts(api_url)
result = ""
# 输出结果
for device_count in video_counts:
    device_name = device_count.get('device')
    video_count = device_count.get('video_count')
    publish_count = device_count.get('publish_count')
    # print("设备编号：" + video_count["账号"])
    # print("剩余视频数量：" + str(video_count["关注数量"]))
    # print("剩余可发布视频数量：" + str(video_count["粉丝数量"]))
    print(f"设备编号: {device_name}")
    print(f"剩余视频数量: {video_count}")
    print(f"剩余可发布视频数量: {publish_count}")
    print()
    temp_result = f'''
    设备编号:{device_name}
    剩余视频数量:{video_count}
    剩余可发布视频数量:{publish_count}


    '''
    result = result + temp_result
print(result)

WXPUSHER_TOKEN = os.getenv("WXPUSHER_TOKEN")
WECHAT_UID = os.getenv("WECHAT_UID")

if result and len(result) > 0:
    wxpusher_send_by_webapi(result, "设备视频预警推送", WXPUSHER_TOKEN, WECHAT_UID)





