import os
import requests
from datetime import datetime
from pathlib import Path

# Install SDK:  pip install 'volcengine-python-sdk[ark]' .
from volcenginesdkarkruntime import Ark 

# 配置客户端
api_key = os.getenv('ARK_API_KEY')
if not api_key:
    print("❌ 错误: ARK_API_KEY 环境变量未设置")
    print("📝 请设置 API 密钥:")
    print("   export ARK_API_KEY='你的API密钥'")
    print("   然后重新运行脚本")
    exit(1)

client = Ark(
    # The base URL for model invocation
    base_url="https://ark.cn-beijing.volces.com/api/v3", 
    # Get API Key：https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
    api_key=api_key, 
)

# 定义提示词
PROMPT = """A coffee shop entrance features a chalkboard sign reading "Qwen Coffee 😊 $2 per cup," with a neon light beside it displaying "通义千问". Next to it hangs a poster showing a beautiful Chinese woman, and beneath the poster is written "π≈3.1415926-53589793-23846264-33832795-02384197"."""

def generate_filename():
    """根据当前时间生成文件名：月日小时分钟.png (例如: 1221_1530.png)"""
    now = datetime.now()
    return f"{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}.png"

def download_and_save_image(image_url, filename):
    """下载图片并保存到当前目录"""
    try:
        print(f"📥 正在下载图片...")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 保存到当前目录
        save_path = Path(filename)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        file_size = save_path.stat().st_size / 1024  # 转换为 KB
        print(f"✅ 图片已保存到: {save_path.absolute()}")
        print(f"   文件大小: {file_size:.1f} KB")
        return str(save_path.absolute())
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")
        return None

def main():
    try:
        print("🎨 开始生成图片...")
        print(f"📝 提示词: {PROMPT[:50]}...")
        
        # 调用 API 生成图片
        imagesResponse = client.images.generate( 
            model="doubao-seedream-4-5-251128",
            prompt=PROMPT,
            size="2K",
            response_format="url",
            watermark=False
        )
        
        # 获取图片 URL
        image_url = imagesResponse.data[0].url
        print(f"🔗 生成的图片 URL: {image_url}")
        
        # 生成文件名并下载保存
        filename = generate_filename()
        saved_path = download_and_save_image(image_url, filename)
        
        if saved_path:
            print(f"\n✨ 完成! 图片已保存为: {filename}")
            return saved_path
        else:
            print(f"\n⚠️  图片 URL 已获得但下载失败")
            print(f"   可以手动访问: {image_url}")
            return image_url
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    main()