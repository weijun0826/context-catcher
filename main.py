import streamlit as st
import os
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="Context Catcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

if "selected_example" not in st.session_state:
    st.session_state["selected_example"] = "團隊會議摘要"  # Default to first example

if "result_displayed" not in st.session_state:
    st.session_state["result_displayed"] = False

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
</style>
""", unsafe_allow_html=True)

# 設定頁面標題和描述
st.title("🧠 Context Catcher")
st.subheader("自動摘要你的對話紀錄 & 任務清單產出")

# 設定你的 API 金鑰（從 Streamlit secrets 獲取）
try:
    api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
    if api_key:
        st.sidebar.success("API key 已載入")
    else:
        st.sidebar.error("未找到 API key")
except Exception as e:
    st.sidebar.error(f"無法獲取 API key: {e}")
    api_key = None

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

# 範例對話內容
example_conversations = {
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
}

# 側邊欄功能
with st.sidebar:
    st.header("關於 Context Catcher")
    st.write("Context Catcher 幫助你自動分析會議記錄或對話內容，生成摘要和任務清單，讓你的工作更有效率。")

    st.subheader("使用說明")
    st.write("1. 將對話記錄貼到輸入框中")
    st.write("2. 點擊「分析對話紀錄」按鈕")
    st.write("3. 獲取摘要和任務清單")

    # 加入反饋按鈕 - 使用真實的 Google 表單連結
    st.markdown("### 我們需要您的意見！")
    st.markdown("""
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSegSiDo03OePxu48EK5WMTcIeq_OyQkia_rCpIwu3wyimrm5w/viewform?usp=header" target="_blank" class="feedback-btn">
        🎯 提供反饋
    </a>
    """, unsafe_allow_html=True)

    # 添加說明文字
    st.caption("點擊上方按鈕，在 Google 表單中提供您的寶貴意見")

    st.markdown("---")
    st.markdown("© 2025 Context Catcher")

# 主要內容區域
col1, col2 = st.columns([2, 1])

# 定義一個回調函數來更新對話輸入
def update_chat_input():
    # 直接更新文本區域的值
    st.session_state["chat_input_area"] = example_conversations[st.session_state["selected_example"]]

with col1:
    # 輸入區域 - 不直接使用會話狀態作為初始值
    chat_input = st.text_area("請貼上你的對話紀錄",
                              value="",  # Start with empty string instead of session_state
                              height=300,
                              key="chat_input_area")

    # Update session state after the widget is rendered
    st.session_state["chat_input"] = chat_input

with col2:
    st.subheader("範例對話")

    # 選擇範例下拉框
    selected_example = st.selectbox(
        "選擇一個範例",
        list(example_conversations.keys()),
        key="selected_example"
    )

    # 一鍵貼上範例按鈕
    if st.button("一鍵貼上範例", on_click=update_chat_input):
        # 顯示成功訊息
        st.success("範例已貼上，請點擊「分析對話紀錄」按鈕進行分析")
        # 確保 chat_input 變數也被更新
        chat_input = example_conversations[st.session_state["selected_example"]]

# 控制按鈕區域
analyze_button = st.button("🔍 分析對話紀錄", use_container_width=True)

# Session state variables are already initialized at the top of the script

if analyze_button:
    # 檢查 API key 是否可用
    if not api_key:
        st.error("⚠️ 未找到 API key，請確保已在 Streamlit Secrets 中設置 OPENAI_API_KEY。")
    # 檢查輸入是否為空
    elif not chat_input.strip():
        st.warning("⚠️ 請先輸入對話紀錄或選擇一個範例。")
    else:
        # 確保 session_state 中有最新的輸入值
        st.session_state["chat_input"] = chat_input

        with st.spinner("🤖 AI 正在理解對話內容中..."):
            # 顯示進度條
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            prompt = f"""
你是一個高效的AI分析助手，專門處理文字輸入並提取核心資訊。

請根據以下文字內容進行分析：

1. 讀取輸入的文字內容，分析並提取出最重要的資訊與重點，生成簡明摘要。
2. 從文字中識別可執行的工作項目或後續行動事項，列成清單格式的待辦事項。
3. 最後，請將摘要與待辦事項整理成 **Markdown 格式** 輸出，結構清晰、易於閱讀與複製使用。

請使用以下格式輸出：

## 📌 Summary
- 重點1
- 重點2
- 重點3

## ✅ To-Do List
- [ ] 工作項目1
- [ ] 工作項目2
- [ ] 工作項目3

文字內容：
{chat_input}
"""
            # 使用我們的自定義函數調用 OpenAI API
            output = call_openai_api(prompt)

            # 檢查輸出是否包含錯誤信息
            if output.startswith("錯誤:"):
                st.error(f"⚠️ {output}")
                st.info("如果遇到 API 錯誤，請檢查您的 API key 是否有效，以及是否有足夠的配額。")
            else:
                st.session_state["analysis_result"] = output
                st.session_state["result_displayed"] = False  # 重設顯示狀態
                st.success("✅ 分析完成！")

# 顯示結果
if st.session_state["analysis_result"]:
    # 獲取分析結果文本
    result_text = st.session_state["analysis_result"]

    # 顯示分析結果
    st.markdown("### 📝 分析結果")

    # 使用 st.empty() 創建一個容器，確保內容只顯示一次
    result_container = st.empty()

    # 在容器中顯示 Markdown 格式的分析結果
    with result_container:
        st.markdown(result_text)

    # 創建一個JavaScript函數來複製文本到剪貼簿 (使用現代 Clipboard API)
    copy_js = """
    <script>
    // 複製文本到剪貼簿的函數
    function copyTextToClipboard(text) {
        // 使用現代 Clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text)
                .then(() => {
                    showCopySuccessMessage();
                })
                .catch(err => {
                    console.error('無法複製文本: ', err);
                    fallbackCopyTextToClipboard(text);
                });
        } else {
            // 如果 Clipboard API 不可用，使用備用方法
            fallbackCopyTextToClipboard(text);
        }
    }

    // 備用的複製方法 (針對不支援 Clipboard API 的瀏覽器)
    function fallbackCopyTextToClipboard(text) {
        // 創建臨時元素
        var textArea = document.createElement("textarea");
        textArea.value = text;

        // 設置樣式使其不可見
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);

        // 選中並複製
        textArea.focus();
        textArea.select();

        var successful = false;
        try {
            successful = document.execCommand('copy');
            if (successful) {
                showCopySuccessMessage();
            } else {
                alert('複製失敗，請手動選取文本並複製');
            }
        } catch(err) {
            console.error('無法複製文本: ', err);
            alert('複製失敗，請手動選取文本並複製');
        }

        // 移除臨時元素
        document.body.removeChild(textArea);
    }

    // 顯示複製成功訊息
    function showCopySuccessMessage() {
        // 檢查是否已經有訊息顯示
        var existingMsg = document.getElementById('copy-success-message');
        if (existingMsg) {
            document.body.removeChild(existingMsg);
        }

        // 顯示成功訊息
        const successMsg = document.createElement('div');
        successMsg.id = 'copy-success-message';
        successMsg.textContent = '✅ 已複製到剪貼簿';
        successMsg.style.position = 'fixed';
        successMsg.style.top = '20px';
        successMsg.style.left = '50%';
        successMsg.style.transform = 'translateX(-50%)';
        successMsg.style.padding = '10px 20px';
        successMsg.style.backgroundColor = '#4CAF50';
        successMsg.style.color = 'white';
        successMsg.style.borderRadius = '5px';
        successMsg.style.zIndex = '9999';
        successMsg.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        document.body.appendChild(successMsg);

        // 2秒後移除訊息
        setTimeout(() => {
            if (document.body.contains(successMsg)) {
                document.body.removeChild(successMsg);
            }
        }, 2000);
    }
    </script>
    """

    # 創建一個完整的 HTML 結構，包含 JavaScript、隱藏的文本區域和按鈕
    complete_html = f"""
    {copy_js}
    <div class="copy-container">
        <textarea id="copy_text_area" style="position: absolute; left: -9999px;">{result_text}</textarea>
        <button onclick="copyTextToClipboard(document.getElementById('copy_text_area').value);"
                style="width: 100%; padding: 0.5rem; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 10px;">
            📋 複製分析結果到剪貼簿
        </button>
    </div>
    """

    # 一次性顯示所有 HTML 內容
    st.markdown(complete_html, unsafe_allow_html=True)
