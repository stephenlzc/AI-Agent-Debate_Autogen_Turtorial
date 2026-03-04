import os
import requests
from datetime import datetime
import uuid


def generate_speech(input_text, voice, save_dir="speech_output",
                    api_key="sk-fbpycjnvwyhmzultheyeccfzwezovljdmqxgdpqqwjotxbgp"):
    """
    将文本转换为语音并保存为MP3文件

    参数：
    input_text: str - 需要转换的文本内容
    voice: str - 语音模型名称（如："FunAudioLLM/CosyVoice2-0.5B:alex"）
    save_dir: str - 文件保存目录（默认为当前目录下的speech_output文件夹）

    返回：
    str - 保存的MP3文件绝对路径
    """
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{voice.split(':')[-1]}_{timestamp}_{str(uuid.uuid4())[:8]}.mp3"
    file_path = os.path.join(save_dir, filename)

    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
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