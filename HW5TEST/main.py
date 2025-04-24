from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
import pdf
import pw

app = Flask(__name__)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

default_prompt = """請分析以下日記中每一句話的出現的情緒，進行分類：

"快樂",
"難過",
"害怕",
"憤怒",
"愛",
"驚喜",
"備註"

請依據評估結果，對每個項目：若有觸及則標記為 1，否則留空。
最後請在備註欄為這句話下總結，
每一句請依照以下Markdown格式回應：
| 編號 | Text | 快樂 | 難過 | 害怕 | 憤怒 | 愛 | 驚喜 | 備註 |
並將所有類別進行統計、產出報表：
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    pdf_path = None
    if request.method == "POST":
        user_prompt = request.form["user_prompt"]
        csv_file = request.files.get("csv_file")

        if csv_file:
            df = pd.read_csv(csv_file)
            total_rows = df.shape[0]
            block_size = 30
            cumulative_response = ""

            for i in range(0, total_rows, block_size):
                block = df.iloc[i:i+block_size]
                block_csv = block.to_csv(index=False)
                prompt = f"以下是CSV資料第 {i+1} 到 {min(i+block_size, total_rows)} 筆：\n{block_csv}\n\n請根據以下規則進行分析並產出報表：\n{user_prompt}"
                response = client.models.generate_content(
                    model="gemini-2.5-pro-exp-03-25",
                    contents=[prompt]
                )
                cumulative_response += f"區塊 {i//block_size+1}:\n{response.text.strip()}\n\n"

            response_text = cumulative_response
            pdf_path = pdf.generate_pdf(text=response_text)
        else:
            full_prompt = f"未上傳 CSV 檔案。\n\n{user_prompt}"
            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=[full_prompt]
            )
            response_text = response.text.strip()
            pdf_path = pdf.generate_pdf(text=response_text)

    return render_template("index.html", default_prompt=default_prompt, response_text=response_text, pdf_path=pdf_path)

@app.route("/download")
def download():
    path = request.args.get("path")
    return send_file(path, as_attachment=True)

@app.route("/search", methods=["POST"])
def search():
    search_result = pw.search()
    return render_template("index.html", 
                           default_prompt=default_prompt, pdf_path=None)

if __name__ == "__main__":
    app.run(debug=True)
