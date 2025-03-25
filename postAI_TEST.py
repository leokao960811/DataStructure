from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()
MOODLE_USERNAME = os.getenv("MOODLE_USERNAME")
MOODLE_PASSWORD = os.getenv("MOODLE_PASSWORD")

DOWNLOAD_PATH = os.path.abspath("downloads")  # 創建downloads目錄
os.makedirs(DOWNLOAD_PATH, exist_ok=True)  # 確認目錄是否存在

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 顯示瀏覽器
    page = browser.new_page()

    print("啟動瀏覽器，登入 Moodle...")

    # 進入登入頁面
    page.goto("https://moodle3.ntnu.edu.tw/?")
    page.wait_for_timeout(3000)

    # 使用 .env 讀取帳號密碼
    page.fill("#username", MOODLE_USERNAME)
    page.fill("#password", MOODLE_PASSWORD)

    # 按下登入按鈕
    page.locator('button:text("登入")').click()

    # 等待登入完成
    page.wait_for_timeout(5000)
    print("登入成功！")
    page.screenshot(path="debug_1_after_login.png")

    # 直接前往私人檔案區
    page.goto("https://moodle3.ntnu.edu.tw/user/files.php")
    page.wait_for_timeout(3000)
    print("進入檔案區")
    page.screenshot(path="debug_2_after_profile.png")

    # 設置文件下載事件處理
    with page.expect_download() as download_info:
        page.locator("[title='全部下載']").click()
    
    # 等待下載完成
    download = download_info.value
    print(f"下載完成，文件名稱: {download.suggested_filename}")

    # 保存文件到指定資料夾
    file_path = os.path.join(DOWNLOAD_PATH, download.suggested_filename)
    download.save_as(file_path)
    print(f"文件已儲存至: {file_path}")

    # 保持瀏覽器開啟
    input("瀏覽器保持開啟，按 Enter 關閉...")

    # 關閉瀏覽器
    browser.close()
    print("瀏覽器已關閉")