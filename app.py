import os
import sys
import configparser
from flask import Flask, render_template, request, jsonify, Blueprint
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

# --- 辅助函数 ---
def get_base_path():
    """获取资源的根目录，无论是脚本还是打包后的 exe 都适用。"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

def get_persistent_path():
    """获取一个用于存储用户数据的持久化路径。"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

# --- 配置管理 ---
CONFIG_FILE = os.path.join(get_persistent_path(), "config.ini")

def create_default_config():
    """如果配置文件不存在，则创建一个默认的。"""
    if not os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config['VRChat'] = {
            'ip': '127.0.0.1',
            'port': '9000'
        }
        config['WebServer'] = {
            'host': '0.0.0.0',
            'port': '8080'
        }
        config['Presets'] = {
            'words': '你好！,谢谢！,再见！'
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write("# VRChat-WebChat 配置文件\n")
            f.write("# 在此修改 IP、端口等设置\n\n")
            config.write(f)
        print(f"未找到配置文件，已在 {CONFIG_FILE} 创建默认配置。")

# 加载配置
create_default_config()
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding='utf-8')

VRCHAT_IP = config.get('VRChat', 'ip', fallback='127.0.0.1')
VRCHAT_PORT = config.getint('VRChat', 'port', fallback=9000)
SERVER_HOST = config.get('WebServer', 'host', fallback='0.0.0.0')
SERVER_PORT = config.getint('WebServer', 'port', fallback=8080)


# --- 应用设置 ---
base_path = get_base_path()
main_bp = Blueprint('main', __name__, template_folder=os.path.join(base_path, 'templates'))

# --- OSC 客户端 ---
osc_client = udp_client.SimpleUDPClient(VRCHAT_IP, VRCHAT_PORT)

# --- 预设词管理 ---
def load_presets():
    """从配置文件中加载预设词。"""
    words_str = config.get('Presets', 'words', fallback='')
    if words_str:
        return [word.strip() for word in words_str.split(',') if word.strip()]
    return []

def add_to_presets(new_word):
    """将一个新词添加到配置文件中的预设词列表。"""
    current_words = load_presets()
    if new_word not in current_words:
        current_words.append(new_word)
        config.set('Presets', 'words', ','.join(current_words))
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            config.write(f)

# --- Flask 路由 ---
@main_bp.route("/")
def index():
    """提供主 HTML 页面。"""
    presets = load_presets()
    return render_template("index.html", preset_words=presets)

@main_bp.route("/api/send_message", methods=["POST"])
def send_message():
    """接收消息并通过 OSC 发送。"""
    data = request.get_json()
    if not data or "s" not in data:
        return jsonify(success=False, error="无效的消息格式"), 400

    message = data.get("s", "")
    notify = bool(data.get("n", True))

    try:
        msg = OscMessageBuilder(address="/chatbox/input")
        msg.add_arg(message)
        msg.add_arg(True)
        msg.add_arg(notify)
        osc_client.send(msg.build())
        return jsonify(success=True)
    except Exception as e:
        print(f"发送 OSC 消息时出错: {e}")
        return jsonify(success=False, error=str(e)), 500

@main_bp.route("/api/presets", methods=["GET"])
def get_presets():
    """返回预设词列表。"""
    return jsonify(presets=load_presets())

@main_bp.route("/api/presets", methods=["POST"])
def add_preset_route():
    """添加一个新的预设词。"""
    data = request.get_json()
    word_to_add = data.get("word", "").strip()

    if not word_to_add:
        return jsonify(success=False, error="单词不能为空"), 400

    add_to_presets(word_to_add)
    return jsonify(success=True, word=word_to_add)

def create_app():
    """创建并配置 Flask 应用。"""
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app

# --- 主执行 ---
if __name__ == "__main__":
    app = create_app()
    print("====================================================")
    print(f"  欢迎使用 VRChat-WebChat！")
    print(f"  - OSC 将发送至: {VRCHAT_IP}:{VRCHAT_PORT}")
    print(f"  - 网页服务运行于: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"  - 配置文件路径: {CONFIG_FILE}")
    print("====================================================")
    print("请在浏览器中打开网页开始使用。")
    print("按 Ctrl+C 关闭此窗口。")
    
    from waitress import serve
    serve(app, host=SERVER_HOST, port=SERVER_PORT)