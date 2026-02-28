# Sora-Based E-commerce Video Generator

基于 Sora 模型与 Qwen-VL-Max 的多源融合电商带货视频批量生成系统。依据火山引擎 TOS 对象存储搭建云图床、预置商品信息、自动解析商品图、生成高质量提示词、调用视频生成模型、下载视频。

## ✨ 功能特点

- 🧠 **智能提示词生成**: 集成 **Qwen-VL-Max** 视觉大模型，自动分析商品图生成精准提示词。
- 🎬 **Sora 视频生成**: 对接 Sora (或兼容接口) 模型，批量生成高质量电商展示视频。
- ☁️ **云图床系统**: 基于**火山引擎 TOS**，搭建云图床系统。
- 🔄 **全流程自动化**: 从图片输入到视频入库，一键完成批量处理 。
- 📝 **多源信息融合生成高质量提示词**: 通过 JSON 配置文件自定义用户输入参数 + 模型视觉理解 信息融合生成sora2提示词，减少模型理解偏差。

## 🛠️ 环境要求

- 建议Python 3.12+
- 阿里云账号 (开通 DashScope/Qwen 服务)
- 火山引擎账号 (开通 TOS 对象存储)
- 视频生成模型 API 访问权限 (如 Sora)

## 📦 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yanshizhao/fusion-shoe-batch-video-gen.git
   cd <项目文件夹>
   

2. **安装依赖**
   pip install -r requirements.txt

3. **程序启动**
   python main.py -i <输入文件目录> -o <输出文件目录>