from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from debateck import debateck
from debates import debateck
from ttv import ttv
from debatefromnews import debatefromnews
from photo import photo
import os

app = Flask(__name__)
# 添加CORS支持，允许所有来源的跨域请求
CORS(app, resources={r"/*": {"origins": "*"}})

# 添加静态文件服务路由，用于提供audio_output目录中的音频文件
@app.route('/audio_output/<path:filename>')
def serve_audio(filename):
    # 使用项目根目录下的audio_output目录
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audio_output')
    
    # 清理文件名，防止路径遍历攻击
    safe_filename = secure_filename(filename)
    
    # 如果清理后的文件名与原始文件名不同，说明可能存在恶意路径
    if safe_filename != filename:
        print(f"[WARN] 检测到潜在路径遍历攻击: {filename}")
        abort(403, "非法文件名")
    
    # 构建完整的文件路径
    full_path = os.path.join(audio_dir, safe_filename)
    
    # 验证最终路径是否在允许的目录内（防止路径遍历）
    real_audio_dir = os.path.realpath(audio_dir)
    real_requested_path = os.path.realpath(full_path)
    
    if not real_requested_path.startswith(real_audio_dir + os.sep) and real_requested_path != real_audio_dir:
        print(f"[WARN] 路径遍历攻击尝试: {filename}")
        abort(403, "访问被拒绝")
    
    print(f"\n[DEBUG] 请求音频文件: {safe_filename}")
    print(f"[DEBUG] 音频目录路径: {audio_dir}")
    print(f"[DEBUG] 完整文件路径: {full_path}")
    print(f"[DEBUG] 文件是否存在: {os.path.exists(full_path)}\n")
    
    # 添加一个测试路由，列出目录中的所有文件
    if safe_filename == 'test':
        files = os.listdir(audio_dir)
        return {'files': files}
    
    return send_from_directory(audio_dir, safe_filename)

app.register_blueprint(debateck)
app.register_blueprint(ttv)
app.register_blueprint(debatefromnews)
app.register_blueprint(photo)

if __name__ == '__main__':
    # 从环境变量读取FLASK_DEBUG设置，默认关闭调试模式
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
    app.run(host='0.0.0.0', port=9000, debug=debug_mode)
