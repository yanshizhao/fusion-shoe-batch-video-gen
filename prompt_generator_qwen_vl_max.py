
import dashscope
from dashscope import MultiModalConversation
from config import DASHSCOPE_API_KEY

def call_qwen_vl_max_generator_prompts(image_urls, user_input):
    """
    调用 qwen-vl-max 模型（Qwen2.5-VL 系列）生成多模态响应。

    Args:
        image_urls (str or list): 单个或多个图片的公网 URL（必须可公开访问）
        user_input (str): 用户提供的鞋子属性描述
    Returns:
        str: 模型返回的文本内容

    Raises:
        ValueError: 参数错误
        Exception: API 调用失败
    """

    # 使用单大括号 {} 作为 format() 占位符 + XML 标签结构化 + 明确定义声明
    prompt_text = """
                    <important_notice>
                    以下所有引用 <shoe_attributes> 标签的地方，均指代该标签内定义的属性值。
                    当参考图像与 <shoe_attributes> 内容冲突时，以 <shoe_attributes> 为唯一权威依据（优先级：<shoe_attributes> > 图像）。
                    </important_notice>

                    <shoe_attributes>
                    {user_shoe_attributes}
                    </shoe_attributes>

                    1、角色定义
                        你是一名专业的 TikTok Shop AI 视频导演。
                    2、输入信息结构
                        接收 <shoe_attributes> 中定义的鞋子属性作为权威数据源。
                    3、核心任务
                        基于参考图像与 <shoe_attributes>，生成一条可直接用于 Sora 的 15 秒 TikTok 商品视频英文提示词。
                    4、目标受众
                        美国和欧洲 18–45 岁女性，强调情感共鸣与功能相关性，激发"我需要这双鞋！"的购买冲动。
                    5、模特呈现规则
                        模特为白人或欧洲女性；
                        严禁露出脸部，仅展示颈部以下身体（肩部、手臂、躯干、腿部、脚部）；
                        动作自然真实：如自信行走、流畅转身、从容起身。
                    6、视觉保真度硬性约束
                        鞋子在每一帧必须严格匹配 <shoe_attributes> 中定义的属性，包括：
                        • 材质
                        • 颜色
                        • 鞋跟高度与形状
                        • 闭合方式
                        • 等信息
                        不得因光线、角度或动作导致外观偏差。
                    7、多模态校验逻辑
                        同时分析图像与 <shoe_attributes>；
                        当两者冲突时，以 <shoe_attributes> 为唯一权威依据。
                        视频中禁止显示鞋低文案。
                    8、视频时序结构
                        0–3 秒（开场）：中近景展示鞋子最具辨识度细节，包含脚踝或地面，叠加 2 到 4 个词的钩子文案；
                        3–13 秒（主场景）：2 到 3 个真实生活场景，采用全身或腰上镜头，摄像机跟随模特自然移动，鞋子始终可见于画面下半部；每场景最多 1 次 ≤1 秒低角度/脚平视特写；
                        13–15 秒（结尾）：这双鞋子置于极简转盘中央，360° 匀速旋转，软定向光突出鞋子的整体设计感。
                    9、文案与 UI 元素（TikTok 原生风格）
                        每场景叠加 2 到 4 个词的利益文案（简洁、动词导向）；
                        第 2 秒：轻柔脉动的红色爱心（靠近鞋子）；
                        第 6 秒：彩色购物车图标 + 微妙 "+" 动画；
                        第 12 秒："Bestseller" 金色徽章 + "Shop Now" 按钮；
                        所有 UI：无衬线字体、中性/低对比色、无价格或促销文字。
                    10、读白智能决策机制
                        自动判断是否加入英文女声读白：
                        • 若鞋款强调功能性→ 加入读白；
                          若有旁白：
                            • 温暖、自信、节奏舒缓的女性声音；
                            • 使用第二人称 "you"；
                            • 内容具体可感；
                            • 总时长 ≤12 秒，且在视频结束前至少 1.5 秒自然收尾，避免戛然而止。
                        • 若鞋款强调时尚/设计/色彩/廓形 → 不加读白，仅靠文案 + 音乐传递情绪。
                    11、背景音乐要求
                        节奏明快、流行感强的背景音乐、音乐匹配鞋款风格；
                        有旁白时：音乐音量低于人声，确保语音清晰，温暖、自信、有亲和力；
                        无旁白时：音乐可主导节奏；
                        最后 1 秒自然淡出，不与画面或语音冲突。
                    12、输出格式规范
                        仅输出一段连续英文文本；
                        无标题、无解释、无换行、无项目符号、无 markdown；
                        可直接复制粘贴至 Sora 使用。
                    """

    #print("image_urls", image_urls)
    
    # 填充变量
    final_prompt = prompt_text.format(user_shoe_attributes=user_input)
    #print("final_prompt:", final_prompt)
    
    # 设置 API Key
    api_key = DASHSCOPE_API_KEY

    # 构造消息内容
    content = []

    # 图片可以是字符串或列表
    if isinstance(image_urls, str):
        content.append({"image": image_urls})
    elif isinstance(image_urls, list):
        for url in image_urls:
            content.append({"image": url})
    
    #使用填充后的 final_prompt 
    content.append({"text": final_prompt})
    messages = [{"role": "user", "content": content}]

    # 调用模型
    try:
        response = MultiModalConversation.call(
            api_key=api_key,
            model="qwen-vl-max",
            messages=messages
        )
        print("status_code:", response.status_code)
        
        # 解析响应
        if response.status_code != 200:
            raise Exception(f"API 调用失败：{response.code} - {response.message}")

        output = response.output.choices[0].message.content
        if isinstance(output, list):
            return output[0]["text"]
        else:
            return str(output)

    except Exception as e:
        raise Exception(f"调用 qwen-vl-max 时出错：{e}")