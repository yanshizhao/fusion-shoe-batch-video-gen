import requests
from config import API_MARK_KEY
import json


# 关闭SSL警告（解决证书问题）
requests.packages.urllib3.disable_warnings()

def generate_sora_video(prompt, duration=15, aspect_ratio="9:16", image_urls=None, token=API_MARK_KEY):

    """调用Sora API生成视频，返回接口响应数据"""

    url = "https://api.apimart.ai/v1/videos/generations"

    payload = {
        "model": "sora-2",
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "private": False,
        "image_urls": image_urls
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    #print(f"\n【{image_urls}】：{prompt}")
    response = requests.post(url, json=payload, headers=headers)
    #print(" response.json()", response.json())
    return response.json()




