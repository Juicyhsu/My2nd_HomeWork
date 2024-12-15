from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as geni
import os

# 從環境變數中讀取 Google API 金鑰
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("環境變數 'GOOGLE_API_KEY' 未設定")

geni.configure(api_key=api_key)
model = geni.GenerativeModel("gemini-1.5-pro")

# 初始化 Flask 應用
app = Flask(__name__, static_url_path="", static_folder="static")

# 提供靜態 HTML 文件
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# 路由：處理問題
@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # 獲取請求的 JSON 數據
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        question = data["text"]

        # 調用生成模型
        response = model.generate_content(question)

        # 檢查模型返回的結果
        if not hasattr(response, 'text'):
            return jsonify({"error": "Invalid response from model"}), 500

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 啟動應用（本地開發用）
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        print("進入 CLI 模式 (輸入 'quit' 退出)")
        while True:
            question = input("請輸入您的問題 (或輸入 'quit' 退出): ")
            if question.lower() == 'quit':
                break
            try:
                response = model.generate_content(question)
                print(response.text)
            except Exception as e:
                print(f"發生錯誤: {e}")
    else:
        # 啟動 Web 應用，debug 模式開啟
        app.run(host="0.0.0.0", port=8000, debug=True)
