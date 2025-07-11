# VRChat-WebChat

一个通过网页向 VRChat 发送消息的工具，方便在 VR 中快速打字、发送预设消息。

## 特性

- **网页操作**: 在任何支持浏览器的设备上（电脑、手机）打开网页即可向 VRChat 发送消息。
- **预设词**: 支持添加和一键发送常用语，预设词直接在配置文件中管理。
- **跨平台**: 支持直接通过 `python` 运行，也提供了打包好的 `exe` 版本方便 Windows 用户。
- **异步发送**: 点击发送后页面无刷新，体验流畅。
- **可配置**: 所有参数（IP、端口、预设词）均可通过 `config.ini` 文件轻松修改。

## 如何使用

### 1. 确保 VRChat OSC 已开启

在 VRChat 游戏内，请确保已开启 OSC 功能。通常在 `ESC -> System -> OSC` 菜单中可以找到并启用。

### 2. 配置 (可选)

程序启动时会自动生成一个 `config.ini` 文件。您可以通过编辑此文件来修改 VRChat 的 IP/端口、Web 服务器的监听地址/端口以及预设词。

```ini
[VRChat]
# VRChat OSC 的 IP 地址
ip = 127.0.0.1
# VRChat OSC 的端口
port = 9000

[WebServer]
# Web 服务器监听的主机地址
# 0.0.0.0 表示允许局域网内其他设备访问
host = 0.0.0.0
# Web 服务器的端口
port = 8080

[Presets]
# 预设词，多个词之间用逗号分隔
words = 你好！,谢谢！,再见！
```

### 3. 运行程序

#### 方法一：直接运行 (推荐)

1.  确保你安装了 Python (推荐 3.8+)。
2.  下载本项目代码。
3.  安装所有依赖：
    ```bash
    pip install -r requirements.txt
    ```
4.  运行主程序：
    ```bash
    python app.py
    ```
5.  在浏览器中打开 `http://127.0.0.1:8080` (或 `config.ini` 中配置的地址) 即可开始使用。

#### 方法二：使用打包好的 .exe (仅限 Windows)

1.  从 `dist` 文件夹下载最新的 `.exe` 文件。
2.  双击运行 `VRChat-WebChat.exe`。
3.  在浏览器中打开 `http://127.0.0.1:8080` (或 `config.ini` 中配置的地址)。

## 如何打包 (开发者)

如果你修改了代码，可以自己重新打包：

1.  确保安装了 PyInstaller: `pip install pyinstaller`
2.  **删除旧的 `build` 和 `dist` 文件夹**。
3.  执行打包命令：
    ```bash
    pyinstaller VRChat-WebChat.spec
    ```
4.  新的 `.exe` 文件会生成在 `dist` 文件夹中。

## 贡献

欢迎提交 Bug 报告和功能请求！如果您想贡献代码，请先提交一个 Issue 讨论您的想法。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
