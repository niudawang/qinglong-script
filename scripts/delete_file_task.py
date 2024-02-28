import os

import requests


# 获取已经使用过的视频集合
def get_file_list_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        file_list = response.json()
        return file_list
    else:
        print(f"Failed to get file list from API. Status code: {response.status_code}")
        return []


# 删除已经使用过的视频
def delete_files(file_list, base_path):
    if file_list is None or len(file_list)==0:
        print(f"数据获取失败")
    for filename in file_list:
        file_path = os.path.join(base_path, filename)
        # 判断是否存在
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Failed to delete file: {file_path}. Error: {str(e)}")
        else:
            print(f"File does not exist: {file_path}. Skipping deletion.")


# # 配置接口 URL 和文件路径
# api_url = "https://example.com/api/files"
# base_path = "/path/to/files"

#定义在配置文件中
print(os.getenv("api_url2"))
print(os.getenv("api_url"))
print(os.getenv("base_path"))

# # 配置接口 URL 和文件路径
api_url = os.getenv("api_url")
base_path = os.getenv("base_path")

# 获取文件名列表
file_list = get_file_list_from_api(api_url)
# 删除文件
delete_files(file_list, base_path)
