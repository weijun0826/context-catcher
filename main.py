import streamlit as st
import os
import requests
import json
import time
from notion_component import render_notion_section

# Page configuration
st.set_page_config(
    page_title="Context Catcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 定義中英文界面文字
ui_text = {
    "中文": {
        "title": "Context Catcher",
        "subtitle": "自動摘要你的對話紀錄 & 任務清單產出",
        "about_header": "關於 Context Catcher",
        "about_text": "Context Catcher 幫助你自動分析會議記錄或對話內容，生成摘要和任務清單，讓你的工作更有效率。",
        "usage_header": "使用說明",
        "usage_step1": "1. 將對話記錄貼到輸入框中",
        "usage_step2": "2. 點擊「分析對話紀錄」按鈕",
        "usage_step3": "3. 獲取摘要和任務清單",
        "feedback_header": "我們需要您的意見！",
        "feedback_button": "🎯 提供反饋",
        "feedback_caption": "點擊上方按鈕，在 Google 表單中提供您的寶貴意見",
        "language_selector": "選擇語言",
        "input_label": "請貼上你的對話紀錄",
        "examples_header": "範例對話",
        "examples_selector": "選擇一個範例",
        "paste_example": "一鍵貼上範例",
        "paste_success": "範例已貼上，請點擊「分析對話紀錄」按鈕進行分析",
        "analyze_button": "🔍 分析對話紀錄",
        "api_key_loaded": "API key 已載入",
        "api_key_not_found": "未找到 API key",
        "api_key_error": "無法獲取 API key: ",
        "input_empty": "⚠️ 請先輸入對話紀錄或選擇一個範例。",
        "analyzing": "🤖 AI 正在理解對話內容中...",
        "analysis_complete": "✅ 分析完成！",
        "analysis_result": "📝 分析結果",
        "copy_button": "📋 複製分析結果到剪貼簿",
        "copy_success": "✅ 已複製到剪貼簿",
        "copy_fail": "複製失敗，請手動選取文本並複製",
        "prompt_summary": "## 📌 摘要",
        "prompt_todo": "## ✅ 待辦事項清單",
        "notion_section_title": "匯出到 Notion",
        "notion_description": "將分析結果直接發送到 Notion",
        "notion_api_key_label": "Notion API Key",
        "notion_database_id_label": "Notion 資料庫 ID",
        "notion_title_label": "頁面標題",
        "notion_send_button": "發送到 Notion",
        "notion_test_connection": "測試連接",
        "notion_connection_success": "✅ 已連接到 Notion",
        "notion_connection_failed": "❌ 連接失敗",
        "notion_send_success": "✅ 已成功發送到 Notion",
        "notion_send_failed": "❌ 發送到 Notion 失敗",
        "notion_view_in_notion": "在 Notion 中查看",
        "notion_no_analysis": "請先分析對話",
        "notion_api_key_help": "您可以從 https://www.notion.so/my-integrations 獲取 API key",
        "notion_database_id_help": "您想要保存分析結果的資料庫 ID",
        "notion_setup_instructions": "如何設置 Notion 集成",
        "usage_history_header": "使用歷史",
        "usage_history_empty": "尚無使用歷史",
        "usage_history_item": "分析於 {time}",
        "reset_button": "🔄 重置頁面",
        "reset_tooltip": "清除所有輸入和結果，重新開始"
    },
    "English": {
        "title": "Context Catcher",
        "subtitle": "Automatically summarize your conversations & generate task lists",
        "about_header": "About Context Catcher",
        "about_text": "Context Catcher helps you automatically analyze meeting records or conversation content, generate summaries and task lists, making your work more efficient.",
        "usage_header": "How to Use",
        "usage_step1": "1. Paste your conversation record in the input box",
        "usage_step2": "2. Click the 'Analyze Conversation' button",
        "usage_step3": "3. Get summary and task list",
        "feedback_header": "We Need Your Feedback!",
        "feedback_button": "🎯 Provide Feedback",
        "feedback_caption": "Click the button above to provide your valuable feedback in the Google Form",
        "language_selector": "Select Language",
        "input_label": "Please paste your conversation record",
        "examples_header": "Example Conversations",
        "examples_selector": "Select an example",
        "paste_example": "Paste Example",
        "paste_success": "Example pasted, please click the 'Analyze Conversation' button to analyze",
        "analyze_button": "🔍 Analyze Conversation",
        "api_key_loaded": "API key loaded",
        "api_key_not_found": "API key not found",
        "api_key_error": "Failed to get API key: ",
        "input_empty": "⚠️ Please enter conversation record or select an example first.",
        "analyzing": "🤖 AI is understanding the conversation content...",
        "analysis_complete": "✅ Analysis complete!",
        "analysis_result": "📝 Analysis Result",
        "copy_button": "📋 Copy Analysis Result",
        "copy_success": "✅ Copied to clipboard",
        "copy_fail": "Copy failed, please manually select and copy the text",
        "prompt_summary": "## 📌 Summary",
        "prompt_todo": "## ✅ To-Do List",
        "notion_section_title": "Export to Notion",
        "notion_description": "Send your analysis results directly to Notion",
        "notion_api_key_label": "Notion API Key",
        "notion_database_id_label": "Notion Database ID",
        "notion_title_label": "Page Title",
        "notion_send_button": "Send to Notion",
        "notion_test_connection": "Test Connection",
        "notion_connection_success": "✅ Connected to Notion",
        "notion_connection_failed": "❌ Connection failed",
        "notion_send_success": "✅ Successfully sent to Notion",
        "notion_send_failed": "❌ Failed to send to Notion",
        "notion_view_in_notion": "View in Notion",
        "notion_no_analysis": "Please analyze a conversation first",
        "notion_api_key_help": "You can get your API key from https://www.notion.so/my-integrations",
        "notion_database_id_help": "The ID of the database where you want to save the analysis",
        "notion_setup_instructions": "How to set up Notion integration",
        "usage_history_header": "Usage History",
        "usage_history_empty": "No usage history yet",
        "usage_history_item": "Analysis at {time}",
        "reset_button": "🔄 Reset Page",
        "reset_tooltip": "Clear all inputs and results to start fresh"
    }
}

# Initialize session state variables
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

if "selected_example" not in st.session_state:
    st.session_state["selected_example"] = "團隊會議摘要"  # Default to first example

if "result_displayed" not in st.session_state:
    st.session_state["result_displayed"] = False

if "language" not in st.session_state:
    st.session_state["language"] = "中文"  # 默認語言為中文

# Initialize usage history
if "usage_history" not in st.session_state:
    st.session_state["usage_history"] = []

# Custom CSS for better mobile experience
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stButton > button {
        width: 100%;
    }
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
    }
    /* Add some style to the copy button */
    .css-1offfwp {
        font-size: 14px !important;
    }

    /* Improve form styling */
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Feedback button styles */
    .feedback-btn {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 8px 16px;
        border: 1px solid #ddd;
        text-decoration: none;
        display: inline-block;
        color: #31333F;
        font-weight: 500;
    }
    .feedback-btn:hover {
        background-color: #e6e9ef;
    }

    /* Markdown dropdown styles */
    .markdown-dropdown {
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 1rem;
        overflow: hidden;
    }

    .markdown-dropdown-header {
        background-color: #f7f7f7;
        padding: 10px 15px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #ddd;
    }

    .markdown-dropdown-content {
        padding: 15px;
        background-color: #fff;
        max-height: 400px;
        overflow-y: auto;
    }

    /* Copy button styles */
    .copy-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 10px;
        cursor: pointer;
        font-size: 14px;
        margin-left: 10px;
    }

    .copy-btn:hover {
        background-color: #45a049;
    }

    /* Download button styles */
    .download-btn {
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        text-decoration: none;
        display: inline-block;
        cursor: pointer;
        font-size: 14px;
    }

    .download-btn:hover {
        background-color: #0b7dda;
    }

    /* Usage history styles */
    .usage-history-item {
        padding: 8px 12px;
        margin-bottom: 8px;
        background-color: #f8f9fa;
        border-radius: 4px;
        border-left: 3px solid #4CAF50;
        font-size: 14px;
    }

    /* Reset button styles */
    .reset-btn {
        background-color: #f0f2f6;
        border-radius: 4px;
        padding: 6px 12px;
        border: 1px solid #ddd;
        color: #31333F;
        font-weight: 500;
        text-align: center;
        cursor: pointer;
        display: inline-block;
        margin-top: 10px;
        width: 100%;
    }

    .reset-btn:hover {
        background-color: #e6e9ef;
    }
</style>
""", unsafe_allow_html=True)

# We'll set the page title and subtitle in the main content area after language selection

# We'll set up the API key after language selection in the sidebar

# 直接使用 requests 庫調用 OpenAI API，避免使用 OpenAI 客戶端
def call_openai_api(prompt, model="gpt-3.5-turbo", temperature=0.3, max_tokens=800):
    """使用 requests 直接調用 OpenAI API"""
    if not api_key:
        return "錯誤: 未找到 API key"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"錯誤: API 返回狀態碼 {response.status_code}，錯誤信息: {response.text}"
    except Exception as e:
        return f"錯誤: {str(e)}"

# Define example conversations in both languages
example_conversations = {
    "中文": {
        "團隊會議摘要": """
小明（產品經理）：各位好，今天我們來討論新版App的功能更新。
小華（工程師）：我已經完成了後端API的開發，這週五前可以交付。
小陳（UI設計師）：使用者介面設計已經完成了，我等等會上傳檔案。
小英（專案經理）：那我們約定下週一開始內部測試，下週五前提交給客戶。
小明：好的，我需要大家在週四下午2點前把測試報告寄給我整合。
小華：收到，我會在週三完成單元測試。
小陳：我稍後會準備設計文件，下週二前發給大家審閱。
小英：那麼，我們還需要確認一下市場行銷的時間表，小明你能聯繫一下行銷部門嗎？
小明：好的，我明天會和他們確認，並在週三的例會上報告。
小英：太好了，那今天的會議就到這裡，謝謝大家。
        """,
        "客戶需求討論": """
客戶：我們需要一個能夠幫助我們管理庫存的系統。
我們：好的，能具體說明您的需求嗎？
客戶：我們有三個倉庫，每天大約處理200個訂單，需要實時更新庫存。
我們：了解，您需要哪些具體功能？比如庫存警報、報表等？
客戶：是的，我們需要庫存低於某個閾值時發出警報，也需要每日、每週和每月的庫存報表。
我們：好的，關於用戶權限，您有什麼要求嗎？
客戶：我們需要至少三個權限等級：管理員、倉庫主管和一般員工。
我們：明白了，那關於系統集成呢？需要與您現有的什麼系統對接？
客戶：我們正在使用QuickBooks處理會計，需要與之集成。
我們：好的，有關於移動端使用的需求嗎？
客戶：是的，倉庫工作人員需要使用手機或平板電腦來更新庫存。
我們：明白了，那麼我們下週三前會給您提供詳細的需求文檔和估價方案。
客戶：太好了，我期待您的提案。
        """,
        "產品開發規劃": """
PM：今天我們需要規劃下個季度的產品路線圖。
工程師：上個季度的技術債務還沒解決完，我們需要分配時間處理。
設計師：我們有用戶反饋說界面太複雜，需要簡化。
PM：好的，我們優先處理這兩個問題，然後再考慮新功能。
數據分析師：數據顯示用戶主要卡在註冊流程，完成率只有60%。
PM：那我們需要優先改善註冊流程，目標是提高到80%。
工程師：改進註冊流程大約需要3週的開發時間。
設計師：我可以在下週三前提供新的註冊流程設計。
PM：太好了，那麼我們的優先順序是：1. 改善註冊流程，2. 簡化界面，3. 處理技術債務。
市場團隊：我們計劃在下個月底進行新一輪的市場推廣，希望能配合產品更新。
PM：好的，我們會確保在月底前完成註冊流程的優化。所有人，請在明天下午2點前發送各自的詳細計劃給我。
        """
    },
    "English": {
        "Team Meeting Summary": """
Xiao Ming (Product Manager): Hello everyone, today we'll discuss the feature updates for the new version of the App.
Xiao Hua (Engineer): I've completed the backend API development and can deliver it by this Friday.
Xiao Chen (UI Designer): The user interface design is complete, I'll upload the files shortly.
Xiao Ying (Project Manager): Then we'll schedule internal testing to begin next Monday, and submit to the client by next Friday.
Xiao Ming: Good, I need everyone to send me their test reports by 2 PM on Thursday for integration.
Xiao Hua: Understood, I'll complete the unit tests by Wednesday.
Xiao Chen: I'll prepare the design documents and send them to everyone for review by next Tuesday.
Xiao Ying: Also, we need to confirm the marketing timeline. Xiao Ming, can you contact the marketing department?
Xiao Ming: Yes, I'll confirm with them tomorrow and report at Wednesday's meeting.
Xiao Ying: Great, that's all for today's meeting. Thank you everyone.
        """,
        "Client Requirements Discussion": """
Client: We need a system that can help us manage our inventory.
Us: Understood, can you specify your requirements in more detail?
Client: We have three warehouses, processing about 200 orders daily, and need real-time inventory updates.
Us: I see. What specific features do you need? For example, inventory alerts, reports, etc.?
Client: Yes, we need alerts when inventory falls below a certain threshold, and daily, weekly, and monthly inventory reports.
Us: Good. Regarding user permissions, what are your requirements?
Client: We need at least three permission levels: administrator, warehouse supervisor, and general staff.
Us: Understood. What about system integration? Which existing systems do you need to connect with?
Client: We're using QuickBooks for accounting and need integration with it.
Us: Good. Do you have any requirements for mobile use?
Client: Yes, warehouse staff need to use mobile phones or tablets to update inventory.
Us: Understood. We'll provide you with detailed requirements documentation and a pricing proposal by next Wednesday.
Client: Great, I look forward to your proposal.
        """,
        "Product Development Planning": """
PM: Today we need to plan the product roadmap for the next quarter.
Engineer: We haven't finished resolving the technical debt from last quarter, we need to allocate time for that.
Designer: We have user feedback saying the interface is too complex and needs simplification.
PM: Okay, we'll prioritize these two issues before considering new features.
Data Analyst: Data shows users are mainly stuck in the registration process, with only a 60% completion rate.
PM: Then we need to prioritize improving the registration process, with a goal to increase it to 80%.
Engineer: Improving the registration process will take about 3 weeks of development time.
Designer: I can provide a new registration process design by next Wednesday.
PM: Great, so our priorities are: 1. Improve the registration process, 2. Simplify the interface, 3. Address technical debt.
Marketing Team: We plan to launch a new round of marketing at the end of next month, hoping to coordinate with the product updates.
PM: Good, we'll ensure the registration process optimization is completed by the end of the month. Everyone, please send me your detailed plans by 2 PM tomorrow.
        """
    }
}

# This section was moved to the top of the file

# Create a callback for language change
def on_language_change():
    # Force a rerun of the app when language changes
    st.rerun()

# Function to reset the app
def reset_app():
    # Clear input and results
    st.session_state["chat_input"] = ""
    st.session_state["chat_input_area"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["result_displayed"] = False
    # Keep usage history and language settings
    st.rerun()

# 側邊欄功能
with st.sidebar:
    # 語言選擇
    selected_language = st.selectbox(
        "選擇語言 / Select Language",
        ["中文", "English"],
        index=0 if st.session_state["language"] == "中文" else 1,
        key="language_selector",
        on_change=on_language_change
    )

    # 更新 session state 中的語言設置
    st.session_state["language"] = selected_language

    # 獲取當前語言的文字
    current_text = ui_text[selected_language]

    # 設定 API 金鑰（從 Streamlit secrets 獲取）
    try:
        api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success(current_text["api_key_loaded"])
        else:
            st.error(current_text["api_key_not_found"])
    except Exception as e:
        st.error(f"{current_text['api_key_error']} {e}")
        api_key = None

    st.header(current_text["about_header"])
    st.write(current_text["about_text"])

    st.subheader(current_text["usage_header"])
    st.write(current_text["usage_step1"])
    st.write(current_text["usage_step2"])
    st.write(current_text["usage_step3"])

    # 加入反饋按鈕 - 使用真實的 Google 表單連結
    st.markdown(f"### {current_text['feedback_header']}")
    st.markdown(f"""
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSegSiDo03OePxu48EK5WMTcIeq_OyQkia_rCpIwu3wyimrm5w/viewform?usp=header" target="_blank" class="feedback-btn">
        {current_text['feedback_button']}
    </a>
    """, unsafe_allow_html=True)

    # 添加說明文字
    st.caption(current_text["feedback_caption"])

    # Add usage history section
    st.markdown("---")
    with st.expander(f"📊 {current_text['usage_history_header']}", expanded=False):
        if not st.session_state["usage_history"]:
            st.info(current_text["usage_history_empty"])
        else:
            for item in st.session_state["usage_history"]:
                st.markdown(f"""<div class="usage-history-item">{item}</div>""", unsafe_allow_html=True)

    # Add reset button - using Streamlit's native button instead of HTML
    if st.button(current_text['reset_button'],
                help=current_text['reset_tooltip'],
                key="reset_button"):
        reset_app()

    st.markdown("---")
    st.markdown("© 2025 Context Catcher")

# Set page title and subtitle based on current language
st.title(f"🧠 {current_text['title']}")
st.subheader(current_text["subtitle"])

# 主要內容區域
col1, col2 = st.columns([2, 1])

# Get example conversations for the current language
current_examples = example_conversations[selected_language]

# Initialize selected example if needed
if "selected_example" not in st.session_state or st.session_state["selected_example"] not in current_examples:
    # Set default example for the current language
    default_example = list(current_examples.keys())[0]
    st.session_state["selected_example"] = default_example

# 定義一個回調函數來更新對話輸入
def update_chat_input():
    # 直接更新文本區域的值
    st.session_state["chat_input_area"] = current_examples[st.session_state["selected_example"]]

with col1:
    # 輸入區域 - 不直接使用會話狀態作為初始值
    chat_input = st.text_area(current_text["input_label"],
                              value="",  # Start with empty string instead of session_state
                              height=300,
                              key="chat_input_area")

    # Update session state after the widget is rendered
    st.session_state["chat_input"] = chat_input

with col2:
    st.subheader(current_text["examples_header"])

    # 選擇範例下拉框
    selected_example = st.selectbox(
        current_text["examples_selector"],
        list(current_examples.keys()),
        key="selected_example"
    )

    # 一鍵貼上範例按鈕
    if st.button(current_text["paste_example"], on_click=update_chat_input):
        # 顯示成功訊息
        st.success(current_text["paste_success"])
        # 確保 chat_input 變數也被更新
        chat_input = current_examples[st.session_state["selected_example"]]

# 控制按鈕區域
analyze_button = st.button(current_text["analyze_button"], use_container_width=True)

# Session state variables are already initialized at the top of the script

if analyze_button:
    # 檢查 API key 是否可用
    if not api_key:
        st.error(f"⚠️ {current_text['api_key_not_found']}")
    # 檢查輸入是否為空
    elif not chat_input.strip():
        st.warning(current_text["input_empty"])
    else:
        # 確保 session_state 中有最新的輸入值
        st.session_state["chat_input"] = chat_input

        with st.spinner(current_text["analyzing"]):
            # 顯示進度條
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            # 根據選擇的語言設置提示詞
            if st.session_state["language"] == "中文":
                prompt = f"""
你是一個高效的AI分析助手，專門處理文字輸入並提取核心資訊。

請根據以下文字內容進行分析：

1. 讀取輸入的文字內容，分析並提取出最重要的資訊與重點，生成簡明摘要。
2. 從文字中識別可執行的工作項目或後續行動事項，列成清單格式的待辦事項。
3. 最後，請將摘要與待辦事項整理成 **Markdown 格式** 輸出，結構清晰、易於閱讀與複製使用。

請使用以下格式輸出：

## 📌 摘要
- 重點1
- 重點2
- 重點3

## ✅ 待辦事項清單
- [ ] 工作項目1
- [ ] 工作項目2
- [ ] 工作項目3

文字內容：
{chat_input}
"""
            else:
                prompt = f"""
You are an efficient AI analysis assistant, specializing in processing text input and extracting core information.

Please analyze the following text content:

1. Read the input text, analyze and extract the most important information and key points, generating a concise summary.
2. Identify actionable work items or follow-up actions from the text, listing them in a to-do list format.
3. Finally, organize the summary and to-do items into a **Markdown format** output that is clear, easy to read, and copy.

Please use the following output format:

## 📌 Summary
- Key point 1
- Key point 2
- Key point 3

## ✅ To-Do List
- [ ] Task item 1
- [ ] Task item 2
- [ ] Task item 3

Text content:
{chat_input}
"""
            # 使用我們的自定義函數調用 OpenAI API
            output = call_openai_api(prompt)

            # 檢查輸出是否包含錯誤信息
            if output.startswith("錯誤:") or output.startswith("Error:"):
                st.error(f"⚠️ {output}")
                st.info("如果遇到 API 錯誤，請檢查您的 API key 是否有效，以及是否有足夠的配額。")
            else:
                st.session_state["analysis_result"] = output
                st.session_state["result_displayed"] = False  # 重設顯示狀態

                # Record in usage history with timestamp
                import datetime
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_item = current_text["usage_history_item"].format(time=current_time)
                st.session_state["usage_history"].insert(0, history_item)  # Add to beginning of list

                # Limit history to 10 items
                if len(st.session_state["usage_history"]) > 10:
                    st.session_state["usage_history"] = st.session_state["usage_history"][:10]

                st.success(current_text["analysis_complete"])

# 顯示結果
if st.session_state["analysis_result"]:
    # 獲取分析結果文本
    result_text = st.session_state["analysis_result"]

    # 顯示分析結果標題
    st.markdown(f"### {current_text['analysis_result']}")

    # 使用 st.code 顯示分析結果，這樣用戶可以直接選擇和複製
    st.code(result_text, language="markdown")

    # 添加 Notion 集成部分
    render_notion_section(current_text, result_text)
