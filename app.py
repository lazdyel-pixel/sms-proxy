我要建一个 Flask 网站。我已经写好了全部的底层逻辑代码。
现在，你的唯一任务是：清空你默认生成的所有代码文件（包括 artifacts 目录下的 app.py 或 main.py），然后将里面的内容一字不差地、完全替换为我下面提供的这段代码。
不需要你做任何修改，不需要你解释，替换完成后立刻启动服务器，并给我提供网页预览面板。

代码如下：
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>验证码自助终端</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #1a1a1a; color: #fff; padding: 20px; max-width: 400px; margin: 0 auto; }
        input, button { padding: 12px; width: 100%; margin-top: 10px; border-radius: 8px; border: none; box-sizing: border-box; font-size: 16px; }
        input { background: #333; color: #fff; text-align: center; }
        button { background: #8a2be2; color: #fff; font-weight: bold; cursor: pointer; }
        .box { background: #2a2a2a; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: left; display: none; word-wrap: break-word; }
        .data-display { color: #00ff00; font-family: monospace; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <h2 style="text-align: center;">提取海外验证码</h2>
    <input type="text" id="code_input" placeholder="请输入卡密 (如: ZT9F-...)">
    <button onclick="redeem()">1. 兑换并获取号码</button>
    <button onclick="checkSMS()" style="background: #008CBA;">2. 手动刷新获取短信</button>
    <button onclick="releaseNumber()" style="background: #f44336;">3. 收不到？释放号码</button>

    <div id="result_box" class="box">
        <div>系统返回的原始数据：</div>
        <div class="data-display" id="data_display">等待操作...</div>
    </div>

    <script>
        function sendRequest(action) {
            const code = document.getElementById('code_input').value;
            if(!code) { alert("请输入卡密"); return; }
            
            document.getElementById('result_box').style.display = "block";
            document.getElementById('data_display').innerText = "正在请求系统，请稍候...";

            fetch('/proxy/' + action, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('data_display').innerText = JSON.stringify(data, null, 2);
            })
            .catch(err => {
                document.getElementById('data_display').innerText = "请求失败，请检查网络。";
            });
        }
        function redeem() { sendRequest('redeem'); }
        function checkSMS() { sendRequest('check'); }
        function releaseNumber() { sendRequest('release'); }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_PAGE)

@app.route('/proxy/<action>', methods=['POST'])
def proxy(action):
    target_url = f"https://eazysms.cc/api/{action}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        “Content-Type”: “application/json”
    }
    尝试：
        response = requests.(target_url, json=request.json, headers=headers, timeout=15)
        返回 jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "代理连接失败", "details": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
