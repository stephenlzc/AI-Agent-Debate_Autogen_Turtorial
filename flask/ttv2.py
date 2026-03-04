import os
import requests
from datetime import datetime
import uuid
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 从环境变量获取默认API key
DEFAULT_SPEECH_API_KEY = os.getenv('SPEECH_API_KEY')


def generate_speech(input_text, voice, save_dir="speech_output",
                    api_key=None):
    """
    将文本转换为语音并保存为MP3文件

    参数：
    input_text: str - 需要转换的文本内容
    voice: str - 语音模型名称（如："FunAudioLLM/CosyVoice2-0.5B:alex"）
    save_dir: str - 文件保存目录（默认为当前目录下的speech_output文件夹）
    api_key: str - API key（优先使用传入的值，否则使用环境变量SPEECH_API_KEY）

    返回：
    str - 保存的MP3文件绝对路径

    抛出：
    ValueError - 当api_key和环境变量都未设置时
    """
    # 确定使用的API key：优先使用传入的参数，否则使用环境变量
    effective_api_key = api_key if api_key is not None else DEFAULT_SPEECH_API_KEY
    
    if not effective_api_key:
        raise ValueError(
            "未设置API key。请通过以下方式之一设置：\n"
            "1. 传入api_key参数：generate_speech(..., api_key='your-api-key')\n"
            "2. 设置环境变量：export SPEECH_API_KEY='your-api-key'\n"
            "3. 在.env文件中添加：SPEECH_API_KEY=your-api-key"
        )
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{voice.split(':')[-1]}_{timestamp}_{str(uuid.uuid4())[:8]}.mp3"
    file_path = os.path.join(save_dir, filename)

    # 请求头
    headers = {
        "Authorization": f"Bearer {effective_api_key}",
        "Content-Type": "application/json"
    }

    # 请求体
    payload = {
        "model": "FunAudioLLM/CosyVoice2-0.5B",
        "input": input_text,
        "voice": voice,
        "response_format": "mp3",
        "sample_rate": 32000,
        "stream": True,
        "speed": 1,
        "gain": 0
    }

    try:
        # 发送请求
        response = requests.post(
            "https://api.siliconflow.cn/v1/audio/speech",
            headers=headers,
            json=payload,
            stream=True
        )

        # 检查响应状态
        if response.status_code == 200:
            # 保存音频文件
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return os.path.abspath(file_path)
        else:
            raise Exception(f"API请求失败，状态码：{response.status_code}，响应内容：{response.text}")

    except Exception as e:
        raise Exception(f"生成语音时发生错误：{str(e)}")


# 使用示例
if __name__ == "__main__":
    try:
        output_path = generate_speech(
            input_text="你站在桥上看风景，看风景的人在楼上看你。",
            voice="FunAudioLLM/CosyVoice2-0.5B:alex"
        )
        print(f"语音文件已保存至：{output_path}")
    except Exception as e:
        print(f"发生错误：{str(e)}")