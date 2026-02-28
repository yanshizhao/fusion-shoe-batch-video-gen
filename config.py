import os
import dashscope
import json

# ===================== 火山引擎TOS配置 =====================
AK = "请填写你的 TOS Access Key"   
SK = "请填写你的 TOS Secret Key"
BUCKET_NAME = "请填写你的 TOS BUCKET_NAME"               
REGION = "cn-guangzhou"

# api mart API Key
API_MARK_KEY = "你的_ACCESS_KEY_ID_请填写" #从apimart api聚合网站获取



#================================ali-qewn—================================
DASHSCOPE_API_KEY = '请填写你的 DashScope API Key (Qwen)' #从阿里百炼平台获取
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# ===================== 本地路径配置 =====================
# 商品图片文件夹路径
PRODUCT_IMAGE_FOLDER = r"请替换为你的本地文件夹目录" # 替换成你本地文件夹，例如：E:\product_image\branan_clear_result

# 保存视频的文件夹
VEDIO_SAVE_PATH = r"请替换为你的本地文件夹目录" # 替换成你本地文件夹，例如：E:\product_image\download_video

# ===================== 业务参数配置 =====================
# 每张图生成风格数量
GENERATE_COUNT = 1

# 视频时长（秒）
DURATION = 15

# 视频比例
ASPECT_RATIO = "9:16"

# 调用Sora间隔时间（秒）
WAIT_TIME = 50


def load_product_input_config(config_path="./product_user_input_config.json"):
    """
    加载商品专属user_input配置文件
    参数：config_path-配置文件路径
    返回：商品路径->user_input的字典，失败返回空字典
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"✅ 成功加载配置文件，共配置 {len(config)} 套商品指令")
        return config
    except FileNotFoundError:
        print(f"⚠️ 配置文件 {config_path} 未找到，将使用默认指令")
        return {}
    except json.JSONDecodeError:
        print(f"❌ 配置文件 {config_path} 格式错误，请检查JSON语法")
        return {}
