import os
from tos_operations import upload_to_tos
from sora_caller import generate_sora_video
from config import GENERATE_COUNT, DURATION, ASPECT_RATIO,  API_MARK_KEY, VIDEO_SAVE_PATH, load_product_input_config
from prompt_generator_qwen_vl_max import call_qwen_vl_max_generator_prompts
import uuid
from response_parser import extract_video_url_from_response
from video_downloader import download_video
from pathlib import Path

def get_all_image_files(folder_path):

    """获取文件夹下所有图片文件（过滤常见图片格式）"""

    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    image_paths = []
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(image_extensions):
            image_paths.append(file_path)
    
    return image_paths

def process_single_product_image(image_path, succ_task_ids):

     # 1. 加载配置并匹配专属user_input
    product_config = load_product_input_config()
    user_input = product_config.get(image_path)
    print(f"\n🔧 【{image_path}】匹配到专属指令：\n{user_input}")

    #"""处理单张商品图片的核心流程"""
    print(f"\n==================== 开始处理图片：{image_path} ====================")

    # 步骤1：上传图片到TOS
    remote_file_key = f"temp_product/{uuid.uuid4()}.png" 
    image_url = upload_to_tos(image_path, remote_file_key)
    if not image_url:
        print(f"❌ 图片{image_path}上传失败，跳过后续处理")
        return

    # 步骤2：生成多风格Sora指令
    print(image_url)
    for i in range(GENERATE_COUNT):
        sora_prompts = call_qwen_vl_max_generator_prompts(image_url, user_input)
        #print(sora_prompts)
        if sora_prompts:
            print(f"✅ {image_path} 生成指令成功：\n{sora_prompts}")

            # 步骤4：调用apimart---Sora生成视频
            print(f"\n {image_path}-{i}：调用apimart---sora生成视频")
            response_data = generate_sora_video(sora_prompts, DURATION, ASPECT_RATIO, [image_url], API_MARK_KEY)
            print(f"\n=== {image_path}-{i} 调用Sora返回结果{response_data} ===")

            # 解析返回结果
            data_list = response_data.get("data", [])
            first_data = data_list[0] if data_list else None
            task_id = first_data.get("task_id") if first_data else None
            
           # 记录成功/失败
            if response_data.get("code") == 200 and task_id:
                succ_task_ids.append({"image_path": image_path, "style": i, "task_id": task_id})
                print(f"✅ {image_path}-{i} 调用成功，任务ID：{task_id}")

                #提取视频url
                output_file = os.path.join(VIDEO_SAVE_PATH, f"{task_id}_video.mp4") 
                video_data = extract_video_url_from_response(task_id)
                if isinstance(video_data, str):
                    # 如果是字符串，说明是直接的视频URL
                    #print(f"✅ 视频URL: {video_data}")
                    # 直接下载
                    download_video(video_data,output_file, task_id)
                elif isinstance(video_data, dict):
                    # 如果是字典，需要从中提取URL
                    videos = video_data.get('videos', [])
                    if videos:
                        video_urls = videos[0].get('url', [])
                        if video_urls:
                            print(f"✅ 提取到视频URL: {video_urls[0]}")
                            # 下载视频
                            download_video(video_url, output_file, task_id)
            else:
                print(f"❌ {image_path}-{i} 调用失败")
