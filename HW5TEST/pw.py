from playwright.sync_api import sync_playwright
# from dotenv import load_dotenv

# HW3 網頁開啟
def search():

    # 讀取 .env 檔案
    # load_dotenv()
    #REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
    #REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 顯示瀏覽器
        page = browser.new_page()

        print("啟動瀏覽器，登入 Reddit...")

        # 進入登入頁面
        page.goto("https://www.reddit.com/")
        #page.wait_for_timeout(3000)

        #page.locator("a[href*='/login']").click()

        # 使用 .env 讀取帳號密碼
        #page.fill("input[name=username]", REDDIT_USERNAME)
        #page.fill("input[name=password]", REDDIT_PASSWORD)
        #page.press("input[name=password]","Enter")

        # 等待登入完成
        page.wait_for_timeout(5000)
        print("登入成功！")
        
        search_box = page.locator("input[placeholder='Search Reddit']").first
        search_box.wait_for(state="visible",timeout=10000)
        search_box.fill("Mental Health")
        page.press("input[placeholder='Search Reddit']","Enter")
        print("搜尋心理健康相關資訊...")

        page.wait_for_timeout(4000)

        # 保持瀏覽器開啟
        input("瀏覽器保持開啟，按 Enter 關閉...")
        # 關閉瀏覽器
        browser.close()
        print("瀏覽器已關閉")