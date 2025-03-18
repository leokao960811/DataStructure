import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
import io


# 根據你的專案結構調整下列 import
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

load_dotenv()

async def process_problem(problem, level, model_client, termination_condition):
    """
    解析問題的函式：
      - 拆解問題成較小的子問題
      - 讓各代理人合作分析
      - 最後彙整結果
    """
    prompt = (
        f"目前正在進行第 {level + 1} 層問題解析。\n"
        f"使用者的問題：{problem}\n"
        "請將此問題拆解為更小的子問題，\n"
        "再請 MultimodalWebSurfer 針對這些問題尋找相關資料，"
        "並將搜尋結果整合進回答中。\n"
        "請各代理人協同合作，提供一份完整且具參考價值的建議，並用繁體中文回答。\n"
        "請確保解析能幫助使用者更具體地解決問題。\n"
    )

    local_data_agent = AssistantAgent("data_agent", model_client)
    local_web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    local_assistant = AssistantAgent("assistant", model_client)
    local_user_proxy = UserProxyAgent("user_proxy")
    local_team = RoundRobinGroupChat(
        [local_data_agent, local_web_surfer, local_assistant, local_user_proxy],
        termination_condition=termination_condition
    )

    messages = []
    async for event in local_team.run_stream(task=prompt):
        if isinstance(event, TextMessage):
            print(f"[{event.source}] => {event.content}\n")
            messages.append({
                "level": level + 1,
                "source": event.source,
                "question": problem,  # 存入該層的問題
                "response": event.content,  # AI 代理人的回應
            })
    return messages

async def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("請檢查 .env 檔案中的 GEMINI_API_KEY。")
        return

    # 初始化模型用戶端 (此處示範使用 gemini-2.0-flash)
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=gemini_api_key,
    )
    
    termination_condition = TextMentionTermination("exit")
    
    # 使用 pandas 以 chunksize 方式讀取 CSV 檔案
    #csv_file_path = "DataMining06.csv"
    #chunk_size = 1000
    #chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    #total_records = sum(chunk.shape[0] for chunk in chunks)
    
    # 使用者輸入問題與解析層數
    problem_statement = input("請輸入你想解析的問題：")
    num_iterations = int(input("請輸入欲解析的層次數量（數字）："))

    all_results = []
    current_problem = problem_statement

    # 利用 map 與 asyncio.gather 同時處理所有批次（避免使用傳統 for 迴圈）
    #tasks = list(map(
        #lambda idx_chunk: process_chunk(
            #idx_chunk[1],
            #idx_chunk[0] * chunk_size,
            #total_records,
            #model_client,
            #termination_condition
        #),
        #enumerate(chunks)
    #))
    
    for level in range(num_iterations):
        results = await process_problem(current_problem, level, model_client, termination_condition)
        all_results.extend(results)

        # 取最新代理人的回應作為下一層的問題
        current_problem = "\n".join([msg["response"] for msg in results])

    # 存成 CSV（未來可視覺化）
    df_log = pd.DataFrame(all_results)
    output_file = "problem_analysis_log.csv"
    df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"已將問題解析結果存為 {output_file}")

    #results = await asyncio.gather(*tasks)
    # 將所有批次的訊息平坦化成一個清單
    #all_messages = [msg for batch in results for msg in batch]
    
    # 將對話紀錄整理成 DataFrame 並存成 CSV
    #df_log = pd.DataFrame(all_messages)
    #output_file = "all_conversation_log2.csv"
    #df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
    #print(f"已將所有對話紀錄輸出為 {output_file}")

if __name__ == '__main__':
    asyncio.run(main())