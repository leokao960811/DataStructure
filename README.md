# DataStructure

### HW1檔案：DataAgent_TEST.py

該週程式建立多個 AI 代理人，以Round Robin形式協作分析數據並提供建議:

- AssistantAgent：負責處理數據與分析
- MultimodalWebSurfer：負責網頁搜尋
- UserProxyAgent：代表使用者的輸入或需求
- RoundRobinGroupChat：讓 AI 代理人輪流參與對話，確保資訊交流

主程式使用 asyncio.gather() 並行處理所有批次

最後會將 AI 代理人的對話記錄儲存進csv中

### HW2檔案：DRaiTEST 資料夾

該週程式讀取 CSV 檔案，從中偵測日記欄位，選取合適欄位作為日記內容進行情緒分析

批量處理對話，將對話內容發送至 Gemini API 

最後解析 API 回傳的 JSON 結果，並將結果寫入新的 CSV 檔案

程式執行結果：

![螢幕擷取畫面 2025-04-14 184226](https://github.com/user-attachments/assets/13d3a9d2-c319-43ba-82f6-ca16fa25d49b)


### HW3檔案：PostAITEST 資料夾

該週程式用playwright進行自動化網頁瀏覽，這次製作一個自動下載、備份的程式

程式首先創建一個downloads目錄，並確認目錄是否存在

進行完下載後，會輸出檔案名稱，並將文件保存到指定資料夾

(一般下載後會存在暫時位置，瀏覽器關掉後**就會不見**，因此要創建目錄及路徑)

### HW4檔案：HW4TEST 資料夾

該週程式以HW2為起始點進行PDF的生成。

PDF的生成方式：
1. 先將生成的CSV檔轉成HTML形式
2. 將轉好的HTML交由pdfkit轉成PDF檔

介面以gradio製作，使用者可輸入自己的PDF檔，

下方有一個按鍵，會自動開啟網頁搜尋論壇上跟心理健康有關的內容。

### HW5檔案：HW5TEST 資料夾

該週程式是將HW4的主程式轉換成flask的APP，
其中使用bootstrap進行HTML介面的優化。

![螢幕擷取畫面 2025-05-09 173415](https://github.com/user-attachments/assets/da6306be-926e-4d27-8739-055a2c1a8460)

## AI Agent 設計圖：

![AI Agent](https://github.com/user-attachments/assets/63da1fc0-ec58-4b6f-92d5-80e72e1a1c38)
