# from flask import Flask, request, jsonify,Blueprint
# from datetime import datetime
# import uuid
# from typing import List, Dict
#
# # 初始化Flask应用
# debateck = Blueprint('debateck',__name__)
#
# # 内存数据存储（最多保留100条最新数据）
# DEBATES: List[Dict] = []
# MAX_DEBATES = 100
#
# # 初始化示例数据
# sample_debates = [
#     {
#         "id": str("abc"),
#         "topic": "人工智能利大于弊还是弊大于利",
#         "url":"https://baijiahao.baidu.com/s?id=1830686373336419594",
#         "pros": {
#             "team": "创新者联盟",
#             "argument": "AI将推动社会生产力革命性提升"
#         },
#         "cons": {
#             "team": "人文守护者",
#             "argument": "AI可能导致大规模失业和社会分化"
#         },
#         "poster": "https://example.com/posters/ai_debate.jpg",
#         "schedule": {
#             "time": "2024-03-15 19:00",
#             "location": "线上直播厅A"
#         },
#         "status": "upcoming",  # ongoing/ended
#         "view_count": 0,
#         "created_at": datetime.now().isoformat()
#     },
#     {
#         "id": str("cba"),
#         "topic": "网络匿名是否有利于公共讨论",
#
#         "url": "https://baijiahao.baidu.com/s?id=1830686373336419594",
#         "pros": {
#             "team": "自由之声",
#             "argument": "保护隐私促进真实意见表达"
#         },
#         "cons": {
#             "team": "责任联盟",
#             "argument": "匿名助长网络暴力和虚假信息"
#         },
#         "poster": "https://example.com/posters/anonymous.jpg",
#         "schedule": {
#             "time": "2024-03-18 15:00",
#             "location": "大学礼堂B"
#         },
#         "status": "ongoing",
#         "view_count": 235,
#         "created_at": datetime.now().isoformat()
#     }
# ]
# DEBATES.extend(sample_debates)
#
# def add_debate(debate: Dict):
#     """添加新辩论赛（自动维护最大容量）
#
#     Args:
#         debate (Dict): 新辩论赛的信息字典
#
#     Returns:
#         None
#     """
#     DEBATES.insert(0, debate)
#     if len(DEBATES) > MAX_DEBATES:
#         DEBATES.pop()
#
# @debateck.route('/api/debates', methods=['GET'])
# def get_debates():
#     """获取辩论赛列表，支持分页、状态过滤和搜索功能
#
#     Returns:
#         JSONResponse: 包含辩论赛列表的JSON响应
#     """
#     try:
#         # 解析查询参数
#         page = int(request.args.get('page', 1))
#         per_page = int(request.args.get('per_page', 10))
#         status_filter = request.args.get('status')
#         search_query = request.args.get('search')
#
#         # 参数验证
#         if page < 1 or per_page < 1:
#             return jsonify({"code": 400, "message": "Invalid pagination parameters"}), 400
#
#         # 过滤数据
#         filtered = DEBATES
#         if status_filter:
#             filtered = [d for d in filtered if d['status'] == status_filter]
#         if search_query:
#             search_lower = search_query.lower()
#             filtered = [d for d in filtered if
#                        search_lower in d['topic'].lower() or
#                        search_lower in d['pros']['team'].lower() or
#                        search_lower in d['cons']['team'].lower()]
#
#         # 分页处理
#         start = (page - 1) * per_page
#         end = start + per_page
#         paginated = filtered[start:end]
#
#         # 构建响应数据
#         return jsonify({
#             "code": 200,
#             "message": "success",
#             "data": {
#                 "total": len(filtered),
#                 "page": page,
#                 "per_page": per_page,
#                 "debates": [
#                     {
#                         "id": d["id"],
#                         "topic": d["topic"],
#                         "url": d["url"],
#                         "pros_team": d["pros"]["team"],
#                         "cons_team": d["cons"]["team"],
#                         "poster": d["poster"],
#                         "schedule_time": d["schedule"]["time"],
#                         "status": d["status"],
#                         "view_count": d["view_count"]
#                     } for d in paginated
#                 ]
#             }
#         })
#
#     except Exception as e:
#         return jsonify({"code": 500, "message": str(e)}), 500
#
#
# @debateck.route('/api/debate/<debate_id>', methods=['GET'])
# def get_debate_detail(debate_id):
#     try:
#         # 在内存中查找指定ID的辩论赛
#         # 根据辩论ID查找并返回对应的辩论对象
#         # 使用生成器表达式在DEBATES列表中查找匹配的辩论对象，如果找不到则返回None
#         target_debate = next((d for d in DEBATES if d['id'] == debate_id), None)
#
#         if not target_debate:
#             return jsonify({
#                 "code": 404,
#                 "message": "Debate not found"
#             }), 404
#
#         # 增加观看计数（模拟实时更新）
#         target_debate['view_count'] += 1
#
#         # 构建完整详情响应
#         return jsonify({
#             "code": 200,
#             "message": "success",
#             "data": {
#                 "id": target_debate["id"],
#                 "topic": target_debate["topic"],
#                 "url": target_debate["url"],
#                 "details": {
#                     "pros": {
#                         "team": target_debate["pros"]["team"],
#                         "argument": target_debate["pros"]["argument"],
#                         "members": []  # 可扩展添加成员信息
#                     },
#                     "cons": {
#                         "team": target_debate["cons"]["team"],
#                         "argument": target_debate["cons"]["argument"],
#                         "members": []
#                     }
#                 },
#                 "poster": target_debate["poster"],
#                 "schedule": target_debate["schedule"],
#                 "status": target_debate["status"],
#                 "view_count": target_debate["view_count"],
#                 "created_at": target_debate["created_at"],
#                 "related": get_related_debates(target_debate["topic"])  # 关联辩论功能
#             }
#         })
#
#     except Exception as e:
#         return jsonify({"code": 500, "message": str(e)}), 500
#
#
# def get_related_debates(topic: str, limit: int = 3):
#     """获取关联辩论赛（基于主题关键词匹配）"""
#     keywords = set(topic.lower().split())
#     related = []
#
#     for debate in DEBATES:
#         if debate['topic'] == topic:
#             continue
#         debate_keywords = set(debate['topic'].lower().split())
#         if len(keywords & debate_keywords) > 0:
#             related.append({
#                 "id": debate["id"],
#                 "topic": debate["topic"],
#                 "status": debate["status"]
#             })
#         if len(related) >= limit:
#             break
#
#     return related