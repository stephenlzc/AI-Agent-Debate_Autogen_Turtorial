from flask import Flask, send_from_directory
from flask_cors import CORS
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
    print(f"\n[DEBUG] 请求音频文件: {filename}")
    print(f"[DEBUG] 音频目录路径: {audio_dir}")
    print(f"[DEBUG] 完整文件路径: {os.path.join(audio_dir, filename)}")
    print(f"[DEBUG] 文件是否存在: {os.path.exists(os.path.join(audio_dir, filename))}\n")
    
    # 添加一个测试路由，列出目录中的所有文件
    if filename == 'test':
        files = os.listdir(audio_dir)
        return {'files': files}
    
    return send_from_directory(audio_dir, filename)

app.register_blueprint(debateck)
app.register_blueprint(ttv)
app.register_blueprint(debatefromnews)
app.register_blueprint(photo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
