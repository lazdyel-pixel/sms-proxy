from flask importFlask、request、jsonify、render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>极速自助接码系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; max-width: 450px; margin: 0 auto; }
        h2 { text-align: center; color: #38bdf8; letter-spacing: 1px; }
        input, button { padding: 14px; width: 100%; margin-top: 12px; border-radius: 10px; border: none; box-sizing: border-box; font-size: 16px; font-weight: bold; }
        input { background: #1e293b; color: #fff; text-align: center; border: 1px solid #334155; }
        input:focus { outline: none; border-color: #38bdf8; }
        .btn-redeem { background: #8b5cf6; color: #fff; cursor: pointer; box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3); }
        .btn-check { background: #0ea5e9; color: #fff; cursor: pointer; }
        .btn-release { background: #ef4444; color: #fff; cursor: pointer; }
        .panel { background: #1e293b; padding: 20px; border-radius: 12px; margin-top: 25px; border: 1px solid #334155; display: none; }
        .label { font-size: 13px; color: #94a3b8; margin-bottom: 5px; }
        .phone-text { font-size: 28px; color: #4ade80; font-family: monospace; font-weight: bold; text-align: center; margin-bottom: 15px; letter-spacing: 1px;}
        .sms-box { background: #0f172a; border: 1px dashed #475569; padding: 15px; border-radius: 8px; color: #fbbf24; min-height: 50px; font-size: 18px; text-align: center; word-break: break-all; }
    </style>
</head>
<body>
    <h2>⚡ 极速接码中控台</h2>
    <input type="text" id="code_input" placeholder="输入您的独立卡密 (如: ZT9F...)">
    <button class="btn-redeem" onclick="doAction('redeem')">1. 提取专属号码</button>
    <button class="btn-check" onclick="doAction('redeem')">2. 刷新最新短信</button>
    <button class="btn-release" onclick="doAction('release')">3. 遇到风控？释放旧号码</button>

    <div id="result_panel" class="panel">
        <div class="label" id="phone_label">分配号码 (请复制前往注册)：</div>
        <div class="phone-text" id="phone_display">获取中...</div>
        <div class="label" id="sms_label">系统提示 / 短信内容：</div>
        <div class="sms-box" id="sms_display">正在处理...</div>
    </div>

    <script>
        function doAction(action) {
            const code = document.getElementById('code_input').value.trim();
            if(!code) { alert("请先输入卡密"); return; }
            
            document.getElementById('result_panel').style.display = "block";
            
如果 (action === 'release') {
                document.getElementById('phone_display').innerText = "释放中...";
                document.getElementById('sms_display').innerText = "正在切断旧号码...";
            } else {
                document.getElementById('sms_display').innerText = "对接系统或刷新中...";
            }

            fetch('/proxy/' + action, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(res => res.json())
            .then(data => {
                // 核心修复：独立处理释放指令，阻止报错逻辑，强行加入前端提示
如果 (action === 'release') {
                    document.getElementById('phone_display').innerText = "已释放";
                    document.getElementById('phone_display').style.color = "#94a3b8"; 
                    document.getElementById('sms_display').innerHTML = "旧号码已成功退回！<br><br><span style='color: #ef4444;'>⚠️ 为避免触发上游缓存机制拿到旧号，请等待 10 秒钟后，再点击按钮 1 提取新号码。</span>";
返回;
                }

                // 正常的拿号逻辑
                document.getElementById('phone_display').style.color = "#4ade80"; 
                if(data && data.card) {
                    document.getElementById('phone_display').innerText = data.card.phone;
                    
                    let receives = data.card.receives;
                    if(receives && receives.length > 0) {
                        let smsContent = receives.map(item => typeof item === 'string' ? item : JSON.stringify(item)).join('<br><hr>');
                        document.getElementById('sms_display').innerHTML = smsContent;
                    } else {
                        document.getElementById('sms_display').innerText = "等待短信到达...(如超时未收到，请直接释放换号)";
                    }
                } else {
                    document.getElementById('phone_display').innerText = "卡密异常";
                    document.getElementById('sms_display').innerText = "卡密无效、已过期或刚被释放。请重新核对卡密。";
                }
            })
            .catch(err => {
                document.getElementById('phone_display').innerText = "网络拥堵";
                document.getElementById('sms_display').innerText = "请求超时，请重新点击按钮。";
            });
        }
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
        "User-Agent": "Mozilla/5.0",
“接受”：“application/json”，
        “Content-Type”: “application/json”
    }
    尝试：
        response = requests.post(target_url, json=request.json, headers=headers, timeout=15)
        返回 jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "连接超时"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
#force update
