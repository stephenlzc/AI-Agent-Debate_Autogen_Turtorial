from flask import Flask, request, Response,Blueprint
import requests
# 初始化 Flask 应用
ttv = Blueprint('ttv',__name__)

# 固定的 API 密钥和请求头
API_URL = "https://api.siliconflow.cn/v1/audio/speech"
HEADERS = {
    "Authorization": "Bearer sk-fbpycjnvwyhmzultheyeccfzwezovljdmqxgdpqqwjotxbgp",
    "Content-Type": "application/json"
}

# 定义生成语音的路由和方法
@ttv.route('/api/generate_speech', methods=['POST'])
def generate_speech():
    """
    生成语音接口。

    该接口接收 POST 请求，根据客户端提供的文本生成语音。
    它调用第三方 API 完成语音合成，并将结果流式返回给客户端。
    """
    try:
        # 获取客户端请求参数
        data = request.get_json()

        # 验证必要参数
        if 'input' not in data:
            return {"error": "Missing required parameter: input"}, 400

        # 构造请求参数（包含默认值）
        # 初始化payload字典，用于配置音频生成模型的参数
        payload = {
            # 指定使用的模型为"FunAudioLLM/CosyVoice2-0.5B"
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            # 从data字典中获取输入文本
            "input": data['input'],
            # 获取指定的声音风格，如果没有提供，则使用默认值
            "voice": data.get('voice', 'FunAudioLLM/CosyVoice2-0.5B:alex'),
            # 获取期望的响应格式，默认为mp3
            "response_format": data.get('response_format', 'mp3'),
            # 获取采样率，默认为32000Hz
            "sample_rate": data.get('sample_rate', 32000),
            # 获取是否为流式响应，默认为True
            "stream": data.get('stream', True),
            # 获取生成速度，默认为1倍速
            "speed": data.get('speed', 1),
            # 获取音量增益，默认为0
            "gain": data.get('gain', 0)
        }

        # 调用语音合成 API
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            stream=True  # 启用流式响应
        )

        # 处理错误响应
        if response.status_code != 200:
            error = response.json().get('error', 'Unknown error')
            return {"error": f"API request failed: {error}"}, response.status_code

        # 流式返回音频数据
        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers['Content-Type']
        )

    except Exception as e:
        # 捕获并返回内部服务器错误
        return {"error": f"Internal server error: {str(e)}"}, 500

# 主函数，启动 Flask 应用
if __name__ == '__main__':
    # 运行Flask应用程序
    # 参数host设置为'0.0.0.0'，表示应用程序将监听所有公网IP接口，不仅限于localhost
    # 参数port设置为9000，指定应用程序运行的端口号为9000
    # 参数debug设置为True，启用调试模式，便于开发过程中自动重载应用并提供调试信息
    app.run(host='0.0.0.0', port=9000, debug=True)
