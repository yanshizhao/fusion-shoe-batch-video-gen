
import requests
import time
from config import API_MARK_KEY


def extract_vedio_url_from_response(task_id, token=API_MARK_KEY, max_attempts=60):
    """
    轮询查询任务结果，提取视频URL
    
    Args:
        task_id (str): 任务ID
        token (str): API认证token
        max_attempts (int): 最大轮询次数
    
    Returns:
        str or None: 第一个视频文件的URL，失败时返回None
    """
    url = f"https://api.apimart.ai/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"language": "zh"}

    print(f"🔍 开始轮询任务结果，任务ID: {task_id}")
    
    for attempt in range(max_attempts):
        
        print(f"🔄 第 {attempt + 1}/{max_attempts} 次尝试...")
        
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        # 检查是否有error字段（错误响应）
        if "error" in result:
            error_msg = result["error"].get("message", "未知错误")
            print(f"❌ 任务查询失败: {error_msg}")
            return None  # 直接返回，不再重试
        
        # 正常响应：检查任务状态
        data = result.get("data")
        if not data:
            print("⚠️ 响应中没有data字段，继续轮询...")
            time.sleep(30)
            continue
            
        status = data.get("status")
        
        if status == "completed":
            # 提取视频URL (videos[0].url[0]) - 修正字段名
            videos = data.get("result", {}).get("videos", [])  # 修正：videos 不是 vedios
            
            if videos and len(videos) > 0:
                video_urls = videos[0].get("url", [])
                if video_urls and len(video_urls) > 0:
                    video_url = video_urls[0]
                    print(f"✅ 任务完成！成功获取视频URL")
                    return video_url  # 返回URL字符串
            
            # 如果没有提取到视频URL，返回字典（原逻辑）
            print("⚠️ 任务完成但未找到视频URL，返回完整结果")
            return data.get("result")
            
        else:
            # pending/processing 状态，继续轮询
            progress = data.get("progress", 0)
            print(f"⏳ 任务处理中，进度: {progress}%")
            time.sleep(30)

    print(f"❌ 达到最大轮询次数 ({max_attempts})，仍未获取结果")
    return None