from flask import Flask, request, jsonify, Blueprint
from datetime import datetime
import uuid
import json
import os
from typing import List, Dict

debateck = Blueprint('debateck', __name__)

# 文件存储配置
# 使用绝对路径指向项目根目录下的debates.jsonl文件
DEBATE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'debates.jsonl')
MAX_DEBATES = 100
DEBATES: List[Dict] = []

# 示例数据
sample_debates = [
    {
        "id": "abc",
        "topic": "人工智能利大于弊还是弊大于利",
        "url": "https://baijiahao.baidu.com/s?id=1830686373336419594",
        "pros": {
            "team": "创新者联盟",
            "argument": "AI将推动社会生产力革命性提升"
        },
        "cons": {
            "team": "人文守护者",
            "argument": "AI可能导致大规模失业和社会分化"
        },
        "poster": "https://example.com/posters/ai_debate.jpg",
        "schedule": {
            "time": "2024-03-15 19:00",
            "location": "线上直播厅A"
        },
        "status": "upcoming",
        "view_count": 0,
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "cba",
        "topic": "网络匿名是否有利于公共讨论",
        "url": "https://baijiahao.baidu.com/s?id=1830686373336419594",
        "pros": {
            "team": "自由之声",
            "argument": "保护隐私促进真实意见表达"
        },
        "cons": {
            "team": "责任联盟",
            "argument": "匿名助长网络暴力和虚假信息"
        },
        "poster": "https://example.com/posters/anonymous.jpg",
        "schedule": {
            "time": "2024-03-18 15:00",
            "location": "大学礼堂B"
        },
        "status": "ongoing",
        "view_count": 235,
        "created_at": datetime.now().isoformat()
    }
]


def load_debates_from_file():
    """从文件加载辩论数据"""
    global DEBATES
    DEBATES.clear()
    if os.path.exists(DEBATE_FILE):
        try:
            with open(DEBATE_FILE, 'r', encoding='utf-8') as f:
                debates = []
                for line in f:
                    line = line.strip()
                    if line:
                        debates.append(json.loads(line))
                # 保留最多MAX_DEBATES条最新数据
                DEBATES.extend(debates[:MAX_DEBATES])
        except Exception as e:
            print(f"加载辩论数据失败: {e}，使用示例数据")
            DEBATES.extend(sample_debates.copy())
    else:
        DEBATES.extend(sample_debates.copy())
        save_debates_to_file()

    # 确保数据量不超过最大值
    while len(DEBATES) > MAX_DEBATES:
        DEBATES.pop()


def save_debates_to_file():
    """保存当前辩论数据到文件"""
    try:
        with open(DEBATE_FILE, 'w', encoding='utf-8') as f:
            for debate in DEBATES:
                f.write(json.dumps(debate, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"保存辩论数据失败: {e}")


# 初始化加载数据
load_debates_from_file()


def add_debate(debate: Dict):
    """添加新辩论并保存到文件"""
    DEBATES.insert(0, debate)
    if len(DEBATES) > MAX_DEBATES:
        DEBATES.pop()
    save_debates_to_file()


@debateck.route('/api/debates', methods=['GET'])
def get_debates():
    """获取辩论列表"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        status_filter = request.args.get('status')
        search_query = request.args.get('search')

        if page < 1 or per_page < 1:
            return jsonify({"code": 400, "message": "参数错误"}), 400

        filtered = DEBATES
        if status_filter:
            filtered = [d for d in filtered if d['status'] == status_filter]
        if search_query:
            search_lower = search_query.lower()
            filtered = [d for d in filtered if
                        search_lower in d['topic'].lower() or
                        search_lower in d['pros']['team'].lower() or
                        search_lower in d['cons']['team'].lower()]

        start = (page - 1) * per_page
        end = start + per_page
        paginated = filtered[start:end]

        return jsonify({
            "code": 200,
            "message": "成功",
            "data": {
                "total": len(filtered),
                "page": page,
                "per_page": per_page,
                "debates": [
                    d
                    for d in paginated
                ]
            }
        })
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500


@debateck.route('/api/debate', methods=['GET'])
def get_debate_detail():
    """获取辩论详情"""
    debate_id = request.args.get('debate_id')
    try:
        target_debate = next((d for d in DEBATES if d['id'] == debate_id), None)
        if not target_debate:
            return jsonify({"code": 404, "message": "未找到辩论"}), 404

        target_debate['view_count'] += 1
        save_debates_to_file()

        return jsonify({
            "code": 200,
            "message": "成功",
            "data": target_debate
        })
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500


def get_related_debates(topic: str, limit: int = 3):
    """获取相关辩论"""
    keywords = set(topic.lower().split())
    related = []
    for debate in DEBATES:
        if debate['topic'] == topic:
            continue
        debate_keywords = set(debate['topic'].lower().split())
        if keywords & debate_keywords:
            related.append({
                "id": debate["id"],
                "topic": debate["topic"],
                "status": debate["status"]
            })
        if len(related) >= limit:
            break
    return related


@debateck.route('/api/addDebate', methods=['POST'])
def create_debate():
    """创建新辩论赛接口"""
    try:
        data = request.json

        # 参数校验
        required_fields = [
            'topic', 'url', 'pros', 'cons',
            'poster', 'schedule', 'status'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "code": 400,
                    "message": f"缺少必要参数: {field}"
                }), 400

        # 构造辩论赛对象
        new_debate = {
            "id": str(uuid.uuid4()),  # 生成唯一ID
            "topic": data["topic"],
            "url": data["url"],
            "pros": {
                "team": data["pros"]["team"],
                "argument": data["pros"]["argument"]
            },
            "cons": {
                "team": data["cons"]["team"],
                "argument": data["cons"]["argument"]
            },
            "poster": data["poster"],
            "schedule": {
                "time": data["schedule"]["time"],
                "location": data["schedule"]["location"]
            },
            "status": data["status"],
            "view_count": 0,
            "created_at": datetime.now().isoformat(),
            "rounds": data["rounds"]
        }

        # 添加并持久化
        add_debate(new_debate)

        return jsonify({
            "code": 201,
            "message": "创建成功",
            "data": {"debate_id": new_debate["id"]}
        }), 201

    except KeyError as e:
        return jsonify({
            "code": 400,
            "message": f"参数结构错误: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500