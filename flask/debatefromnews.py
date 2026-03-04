from datetime import datetime
import json
import uuid
from flask import Flask, request, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
from debates import add_debate
from  photo import get_photo
from ttv3 import text_to_speech
debatefromnews = Blueprint('debatefromnews', __name__)

# 定义目标API的固定参数
API_URL = "https://api.modelarts-maas.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOVu9vLFu3JG5Pl7ruiHud2trqaUNHojAcJVMFcfSUmOhBIJEMWW5Dui9oB1LIImZFSS2tszw51jTDBoqO8Ppg"
}


@debatefromnews.route('/api/generate_debate', methods=['POST'])
def generate_debate():
    # 获取URL参数
    data = request.json
    target_url = data['url']
    if not target_url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 获取目标网页内容
        response = requests.get(target_url, headers=headers)
        response.raise_for_status()
        # 自动处理编码（根据网页内容自适应）
        response.encoding = response.apparent_encoding
        # html_content = response.text
        # 使用BeautifulSoup解析并过滤
        soup = BeautifulSoup(response.text, 'html.parser')

        # 移除所有图片标签
        for img in soup.find_all('img'):
            img.decompose()

        # 移除其他可能包含图片的标签（按需添加）
        for noscript in soup.find_all('noscript'):
            noscript.decompose()

        # 提取纯文本并优化格式
        text = soup.get_text(separator='\n', strip=True)

        # 清理多余空行
        html_content = '\n'.join([line for line in text.split('\n') if line.strip()])
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch URL: {str(e)}"}), 500

    try:
        # 构造请求数据\
        # jsontype = "{\"topic\":\"辩论赛主题\",\"pros\":{\"team\":\"正反\",\"argument\":\"正反立场\"},\"cons\":{\"team\":\"反方\",\"argument\":\"反方立场\"},\"rounds\":[{\"round\":1,\"pro_position\":\"正反论点\",\"pro_evidence\":\"正反论点支持证据\",\"con_position\":\"反方论点\",\"con_evidence\":\"反方论点支持证据\"},{\"round\":2,\"pro_position\":\"正反论点\",\"pro_evidence\":\"正反论点支持证据\",\"con_position\":\"反方论点\",\"con_evidence\":\"反方论点支持证据\"}]}"
        # jsontype = "{\"topic\":\"辩论赛主题\",\"pros\":{\"team\":\"正反\",\"argument\":\"正反立场\"},\"cons\":{\"team\":\"反方\",\"argument\":\"反方立场\"},\"rounds\":[{\"round\":1,\"pro_position\":\"正反论点论据1\",\"con_position\":\"反方论点论据1\",\"emcee\":\"主持人话术1\"},{\"round\":2,\"pro_position\":\"正反论点论据2\",\"con_position\":\"反方论点论据2\",\"emcee\":\"主持人话术2\"]}"
        jsontype = "{\"topic\":\"辩论赛主题\",\"outline\":\"网页内容总结\",\"pros\":{\"team\":\"正反\",\"argument\":\"正反立场\"},\"cons\":{\"team\":\"反方\",\"argument\":\"反方立场\"},\"rounds\":[{\"type\":\"emcee\",\"msg\":\"主持人话术1\"},{\"type\":\"pro\",\"msg\":\"正方论点论据1\"},{\"type\":\"con\",\"msg\":\"反方论点论据1\"},{\"type\":\"emcee\",\"msg\":\"主持人话术2\"},{\"type\":\"pro\",\"msg\":\"正方论点论据2\"},{\"type\":\"con\",\"msg\":\"反方论点论据2\"}]}"
        payload = {
            "model": "DeepSeek-V3",
            "messages": [
                {
                    "role": "user",
                    "content": f"网页HTML内容：\n{html_content}\n请根据这个网页内容生成一个120字左右的内容总结和一个辩论赛主题，并根据正反双方的立场，生成10个辩论轮次，输出格式为标准化的json数据，不要输出任何多余的文本，每个轮次包含一个正方论点，一个反方论点，一个正方论点支持证据，一个反方论点支持证据，论点和论据放在一个字段中且要口语化，并且每个轮次要有一个主持人话术。。标准的json格式如下:\n{jsontype}\n"
                }
            ],
            "stream": False,
            "temperature": 0.6
        }

        # 调用目标API
        api_response = requests.post(API_URL, headers=HEADERS, json=payload)
        api_response.raise_for_status()
        # 提取content字段
        content = api_response.json()['choices'][0]['message']['content']

        # 输出结果
        print(content)

        # 如果需要提取content中的json内容（去除多余的反斜杠和代码块标记）
        try:
            # 去除代码块标记和多余空格
            json_str = content.strip().replace('```json\n', '').replace('\n```', '')
            # 转换json字符串为Python对象
            parsed_json = json.loads(json_str)
            print("\n解析后的JSON对象:")
            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
            parsed_json["url"] = target_url
            parsed_json["id"] = str(uuid.uuid4())
            parsed_json["view_count"] = 0
            parsed_json["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parsed_json["status"] = 'ongoing'
            parsed_json["schedule"]={
                "time" :  datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "线上直播厅"
            }
            # 海报
            parsed_json["poster"] = get_photo(parsed_json["topic"])
            for round_data in parsed_json["rounds"]:
                if "msg" in round_data:
                    audio_path = ""
                    # 调用text_to_speech方法
                    if round_data["type"] == "emcee":
                        audio_path = text_to_speech(round_data["msg"], "chinese_huaxiaogang_common")
                    if round_data["type"] == "pro":
                        audio_path = text_to_speech(round_data["msg"],"chinese_xiaoqi_common")
                    if round_data["type"] == "con":
                        audio_path = text_to_speech(round_data["msg"],"chinese_huaxiaoyan_common")
                    # 添加path字段
                    round_data["path"] = audio_path
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
        add_debate(parsed_json)
        return jsonify(parsed_json)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except ValueError:
        return jsonify({"error": "Invalid response from API"}), 500
