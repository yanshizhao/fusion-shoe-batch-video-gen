import config
import os
import sys
import argparse
from batch_processor import get_all_image_files, process_single_product_image
from tos_operations import batch_delete_tos_images
import log

def main():
    """主执行流程"""
    
    # ==================== 1. 命令行参数解析 ====================
    parser = argparse.ArgumentParser(
        description="TikTok Shop 商品视频提示词批量生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
                示例用法:
                python main.py                          (使用默认配置)
                python main.py -i ./my_images -o ./results
                python main.py --input-folder ./images  (仅修改输入，输出保持默认)
                
                当前默认配置:
                输入文件夹：{config.PRODUCT_IMAGE_FOLDER}
                输出文件夹：{config.VEDIO_SAVE_PATH}
        """
    )
    
    parser.add_argument(
        "-i", "--input-folder", 
        type=str, 
        default=config.PRODUCT_IMAGE_FOLDER, 
        help=f"输入文件夹路径 (默认: {config.PRODUCT_IMAGE_FOLDER})"
    )
    
    parser.add_argument(
        "-o", "--output-folder", 
        type=str, 
        default=config.VEDIO_SAVE_PATH, 
        help=f"输出文件夹路径 (默认: {config.VEDIO_SAVE_PATH})"
    )
    
    args = parser.parse_args()
    
    # 获取最终路径
    input_folder = args.input_folder
    output_folder = args.output_folder
    
    # ==================== 2. 路径验证与处理 ====================
    if not os.path.exists(input_folder):
        log.print_log2(input_folder)
        sys.exit(1)
    
    # 如果输出文件夹不存在，自动创建
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder, exist_ok=True)
            print(f"📁 输出文件夹不存在，已自动创建：{output_folder}")
        except Exception as e:
            print(f"❌ 错误：无法创建输出文件夹 {output_folder}: {e}")
            sys.exit(1)
    
    # ==================== 3. 更新 config 模块的全局值 ====================
    """ 
    * 修改 config 模块中的变量
    * 确保其他模块通过 `from config import PRODUCT_IMAGE_FOLDER` 或 `config.PRODUCT_IMAGE_FOLDER`
    * 获取到的都是更新后的值"""
    config.PRODUCT_IMAGE_FOLDER = input_folder
    config.VEDIO_SAVE_PATH = output_folder

    log.print_log1(config.PRODUCT_IMAGE_FOLDER, config.VEDIO_SAVE_PATH)

    # ==================== 4. 业务逻辑 ====================
    
    # 清除 TOS 临时图片
    try:
        # 注意：如果此函数内部硬编码了路径，可能也需要调整
        batch_delete_tos_images("temp_product/")
    except Exception as e:
        print(f"⚠️ 清理临时文件时出错：{e}")
    
    # 获取待处理的商品图片列表
    image_files = get_all_image_files(config.PRODUCT_IMAGE_FOLDER)
    if not image_files:
        print_log2(config.PRODUCT_IMAGE_FOLDER)
        return
    

    # 初始化成功任务 ID 列表
    succ_response_taskId = []

    # 批量处理每张图片
    print(f"✅ 共找到 {len(image_files)} 张商品图片，开始批量处理...\n")

    for idx, image_path in enumerate(image_files, 1):
        print(f"===== 处理进度：{idx}/{len(image_files)} =====")
        
        try:
            # 处理单个商品图片
            process_single_product_image(image_path, succ_response_taskId)
            
        except Exception as e:
            print(f"❌ 处理失败：{image_path}")
            print(f"   错误信息：{e}")
            continue

    # 输出处理汇总
    log.print_log3(len(image_files), len(succ_response_taskId))

    print(f"❌ 失败/跳过数：{len(image_files) - len(succ_response_taskId)}")
    
    if succ_response_taskId:
        log.print_log4()
        for task in succ_response_taskId:
            # 使用 .get() 防止 KeyError
            img_path = task.get('image_path', 'Unknown')
            style = task.get('style', 'Unknown')
            task_id = task.get('task_id', 'Unknown')
            log.print_log5(img_path, style, task_id)
    
    print(f"\n💾 结果已保存至：{config.VEDIO_SAVE_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 程序发生未知错误：{e}")
        sys.exit(1)