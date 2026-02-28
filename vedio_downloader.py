import requests
from pathlib import Path
from config import VEDIO_SAVE_PATH
import os

def download_video(url, filename, taskid): 
    """
    下载视频文件到 VEDIO_SAVE_PATH 目录（异常安全版）
    
    参数:
        url (str): 视频文件的URL
        filename (str): 要保存的文件名
        taskid (str/int): 任务ID，用于标识本次下载任务
    
    返回:
        str or None: 成功返回完整保存路径，失败返回None
    """
    # 拼接完整的保存路径
    full_save_path = Path(VEDIO_SAVE_PATH) / filename
    print(f"📋 任务{taskid}: 开始处理 - 文件名: {filename}, URL: {url}")

    try:
        # 1. 确保目标目录存在
        Path(VEDIO_SAVE_PATH).mkdir(parents=True, exist_ok=True)
        print(f"📁 目标目录: {VEDIO_SAVE_PATH}")

        # 2. 检查目录是否可写
        if not os.access(VEDIO_SAVE_PATH, os.W_OK):
            print(f"❌ 任务{taskid}: 目录不可写 - {VEDIO_SAVE_PATH}")
            return None
        
        # 3. 如果文件已存在，跳过下载（避免覆盖）
        if full_save_path.exists():
            print(f"🔄 任务{taskid}: 文件已存在，跳过下载 - {full_save_path}")
            return str(full_save_path)  # 存在即视为"成功"，返回路径
        
        # 4. 下载文件（流式下载，避免内存溢出）
        print(f"📥 任务{taskid}: 开始下载视频...")
        response = requests.get(
            url, 
            stream=True, 
            timeout=300,
            headers={"User-Agent": "Mozilla/5.0"}  # 新增UA，避免部分网站拒绝请求
        )
        response.raise_for_status()  # 触发HTTP状态码异常（如404/500）
        
        # 5. 写入文件
        with open(full_save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # 6. 验证下载结果
        if full_save_path.exists() and full_save_path.stat().st_size > 0:
            file_size = full_save_path.stat().st_size / 1024 / 1024
            print(f"✅ 任务{taskid}: 下载成功 - {full_save_path} (大小: {file_size:.1f} MB)")
            return str(full_save_path)
        else:
            print(f"⚠️ 任务{taskid}: 文件创建失败或为空 - {full_save_path}")
            return None

    except Exception as e:
        # 捕获所有异常，仅打印失败信息，不中断程序
        print(f"❌ 任务{taskid}: 下载失败 - 原因: {str(e)}")
        return None