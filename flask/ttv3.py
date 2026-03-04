#
# coding: utf-8

import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdksis.v1.region.sis_region import SisRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdksis.v1 import *
import base64
import os
import uuid


def base64_to_mp3(base64_str: str,
                  output_dir: str = "audio_output",
                  filename: str = None) -> str:
    """
    将Base64编码的音频数据转换为MP3文件

    参数：
    base64_str: str - Base64编码的音频字符串
    output_dir: str - 输出目录（默认：audio_output）
    filename: str - 自定义文件名（可选，默认自动生成）

    返回：
    str - 生成的MP3文件路径

    异常：
    ValueError - 当输入不是有效Base64字符串时
    IOError - 文件写入失败时
    """
    try:
        # 去除可能的Base64前缀（如："data:audio/mp3;base64,"）
        if "," in base64_str:
            base64_str = base64_str.split(",")[-1]

        # 解码Base64字符串
        audio_data = base64.b64decode(base64_str)

        # 使用项目根目录下的audio_output目录
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        abs_output_dir = os.path.join(root_dir, output_dir)
        
        # 创建输出目录
        os.makedirs(abs_output_dir, exist_ok=True)

        # 生成唯一文件名（如果未指定）
        if not filename:
            filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
        elif not filename.endswith(".mp3"):
            filename += ".mp3"

        # 生成绝对路径
        abs_file_path = os.path.join(abs_output_dir, filename)
        
        # 生成相对路径（用于返回）
        rel_file_path = os.path.join(output_dir, filename)

        # 写入MP3文件
        with open(abs_file_path, "wb") as f:
            f.write(audio_data)
            
        # 返回相对路径，以便前端使用
        return rel_file_path

    except base64.binascii.Error as e:
        raise ValueError("无效的Base64字符串") from e
    except IOError as e:
        raise IOError(f"文件写入失败: {str(e)}") from e

# if __name__ == "__main__":
#     # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
#     # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
#     ak = "HPUAUF7PCLU03FNVVFW2"
#     sk = "YOKpeKt6bIfYPCYVVbaxKlUc7IIATnITXs7qlF4B"
#
#     credentials = BasicCredentials(ak, sk)
#
#     client = SisClient.new_builder() \
#         .with_credentials(credentials) \
#         .with_region(SisRegion.value_of("cn-north-4")) \
#         .build()
#
#     try:
#         request = RunTtsRequest()
#         config= TtsConfig(
#             audio_format="mp3" ,
#             _property="chinese_xiaoqi_common"
#          )
#         request.body = PostCustomTTSReq(text="你好", config=config
#         )
#         response = client.run_tts(request)
#         data = response.result.data
#         mp_ = base64_to_mp3(base64_str=data)
#         print(response)
#     except exceptions.ClientRequestException as e:
#         print(e.status_code)
#         print(e.request_id)
#         print(e.error_code)
#         print(e.error_msg)


def text_to_speech(text: str,
                   property: str = "chinese_xiaoqi_common",
                   audio_format: str = "mp3",
                   region: str = "cn-north-4") -> str:
    """
    将文本转换为语音并返回MP3文件路径

    参数:
        text: str - 要转换的文本内容
        property: str - 语音属性/发音人 (默认: "chinese_xiaoqi_common")
        audio_format: str - 音频格式 (默认: "mp3")
        region: str - 华为云区域 (默认: "cn-north-4")

    返回:
        str - 生成的MP3文件路径

    异常:
        ValueError - 当认证失败或参数无效时
        RuntimeError - 当语音合成失败时
    """
    # 安全获取凭证 - 从环境变量读取
    ak = "HPUAUF7PCLU03FNVVFW2"
    sk = "YOKpeKt6bIfYPCYVVbaxKlUc7IIATnITXs7qlF4B"

    if not ak or not sk:
        raise ValueError("华为云AK/SK未配置，请设置HUAWEI_CLOUD_AK和HUAWEI_CLOUD_SK环境变量")

    try:
        # 初始化客户端
        credentials = BasicCredentials(ak, sk)
        client = SisClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(SisRegion.value_of(region)) \
            .build()

        # 构建请求
        request = RunTtsRequest()
        config = TtsConfig(
            audio_format=audio_format,
            _property=property
        )
        request.body = PostCustomTTSReq(
            text=text,
            config=config
        )

        # 执行请求
        response = client.run_tts(request)

        if not response or not response.result.data:
            raise RuntimeError("语音合成返回空数据")

        # 保存为MP3文件
        mp3_path = base64_to_mp3(response.result.data)
        return mp3_path

    except exceptions.ClientRequestException as e:
        error_msg = (f"语音合成请求失败: [状态码: {e.status_code}] "
                     f"[错误码: {e.error_code}] {e.error_msg}")
        raise RuntimeError(error_msg) from e
    except Exception as e:
        raise RuntimeError(f"语音合成处理异常: {str(e)}") from e


# 使用示例
# if __name__ == "__main__":
#     try:
#         # 使用前请先设置环境变量:
#         # export HUAWEI_CLOUD_AK="your_ak"
#         # export HUAWEI_CLOUD_SK="your_sk"
#
#         mp3_file = text_to_speech(
#             text="你好，欢迎使用语音合成服务",
#             property="chinese_xiaoqi_common"
#         )
#         print(f"语音文件已生成: {mp3_file}")
#         mp3_file2 = text_to_speech(
#             text="你好，欢迎使用语音合成服务",
#             property="chinese_huaxiaoxuan_common"
#         )
#         print(f"语音文件已生成: {mp3_file2}")
#
#     except Exception as e:
#         print(f"错误: {str(e)}")

#
# # 使用示例
# if __name__ == "__main__":
#     # 测试用Base64字符串（示例数据）
#     test_base64 = "UklGRlw/AABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YTw/AAD//w=="
#
#     try:
#         # 基本用法
#         output_path = base64_to_mp3(test_base64)
#         print(f"MP3文件已保存至：{output_path}")
#
#         # 自定义文件名和路径
#         custom_path = base64_to_mp3(
#             base64_str=test_base64,
#             output_dir="custom_audio",
#             filename="my_audio.mp3"
#         )
#         print(f"自定义路径文件：{custom_path}")
#
#     except Exception as e:
#         print(f"转换失败：{str(e)}")
