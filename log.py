import sys



"""
工具函数模块
包含打印、文件处理等辅助功能
"""

def print_log1(input_path, output_path):
    """
    打印程序启动，显示输入/输出路径信息。
    Args:
        input_path (str): 输入文件夹路径
        output_path (str): 输出文件夹路径
    """
    separator = "=" * 60
    title = "🎬 TikTok Shop 商品视频提示词批量生成器"
    
    print("\n" + separator)
    print(title.center(60)) 
    print(separator)
    print(f"📂 输入文件夹：{input_path}\n📂 输出文件夹：{output_path}")
    print(separator + "\n")


def print_log2(folder_path):
    """
    打印未找到图片文件的警告日志。
    
    Args:
        folder_path (str): 被检查的文件夹路径
    """
    print(f"⚠️  文件夹 {folder_path} 下未找到任何图片文件")
    print("💡 支持的文件格式：.jpg, .jpeg, .png, .webp, .bmp")

def print_log3(total_count, success_count):
    """
    打印批量处理完成的统计汇总。
    
    Args:
        total_count (int): 总计处理的图片数量
        success_count (int): 成功生成的任务数量
    """
    fail_count = total_count - success_count
    separator = "=" * 60
    
    print("\n" + separator)
    print("📊 批量处理完成汇总".center(60))
    print(separator)
    print(f"📊 总计处理图片数：{total_count}")
    print(f"✅ 成功生成任务数：{success_count}")
    print(f"❌ 失败/跳过数：{fail_count}")
    print(separator + "\n")

def print_log4():
    """
    打印成功任务详情的表头。
    通常在遍历打印具体成功任务列表之前调用。
    """
    print("\n📋 成功任务详情：")
    print("-" * 60)

def print_log5(img_path, style, task_id):
    """
    打印单个成功任务的详细信息。
    
    Args:
        img_path (str): 图片路径
        style (str): 生成的风格
        task_id (str): 任务 ID
    """
    print(f"🖼️  图片：{img_path}")
    print(f"   风格：{style}")
    print(f"   任务 ID: {task_id}")
    print("-" * 60)