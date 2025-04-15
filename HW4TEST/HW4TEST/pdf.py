from datetime import datetime
import pandas as pd
import pdfkit
from jinja2 import Template
from table import create_table

# 定義 HTML 模板
html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataFrame PDF</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        .table { width: 80%; margin: auto; border-collapse: collapse; }
        .table th, .table td { border: 1px solid black; padding: 8px; text-align: center; }
        .table th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>PDF 生成</h2>
    {{ table | safe }}
</body>
</html>
"""
# 路徑需自行更改
WKHTMLTOPDF_PATH=r"D:\Programmed Files\Python\TEST\wkhtmltox\bin\wkhtmltopdf.exe"

config=pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

#HW4 以HTML生成PDF
def generate_pdf(text: str = None, df: pd.DataFrame = None) -> str:

    print("開始生成 PDF")
    html_table=""
    if df is not None:
        create_table(df)
    elif text is not None:
        # 嘗試檢查 text 是否包含 Markdown 表格格式
        if "|" in text:
            # 找出可能的表格部分（假設從第一個 '|' 開始到最後一個 '|'）
            table_part = "\n".join([line for line in text.splitlines() if line.strip().startswith("|")])
            parsed_df = parse_markdown_table(table_part)
            if parsed_df is not None:
                html_table=create_table(parsed_df)
            else:
                pdf.multi_cell(0, 10, text)
        else:
            pdf.multi_cell(0, 10, text)
    else:
        pdf.cell(0, 10, "沒有可呈現的內容")


    template=Template(html_template)
    html_content=template.render(table=html_table)
    
    pdf_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    html_file="output.html"
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    print("輸出 PDF 至檔案：", pdf_filename)
    pdfkit.from_file("output.html", pdf_filename, verbose=True, configuration=config, options={"enable-local-file-access": True})
    print("PDF 生成完成")
    return pdf_filename