import streamlit as st
import os
import requests
import json

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

# 移除重複的標題
st.markdown("---")

# 輸入區域
chat_input = st.text_area("請貼上你的對話紀錄", height=300)

if st.button("分析對話紀錄"):
    # 檢查 API key 是否可用
    if not api_key:
        st.error("未找到 API key，請確保已在 Streamlit Secrets 中設置 OPENAI_API_KEY。")
    # 檢查輸入是否為空
    elif not chat_input.strip():
        st.warning("請先輸入對話紀錄。")
    else:
        with st.spinner("AI 正在理解對話內容中..."):
            prompt = f"""
你是一個任務整理助理，請根據以下對話紀錄進行分析，產出：

1. 一段簡潔摘要（約 3-5 行）
2. 待辦事項清單（格式為：- [ ] 任務名稱 - 負責人（如有） - 截止日（如有））

對話紀錄：
{chat_input}
"""
            # 使用我們的自定義函數調用 OpenAI API
            st.info("正在調用 OpenAI API...")
            output = call_openai_api(prompt)

            # 檢查輸出是否包含錯誤信息
            if output.startswith("錯誤:"):
                st.error(output)
                st.info("如果遇到 API 錯誤，請檢查您的 API key 是否有效，以及是否有足夠的配額。")
            else:
                st.markdown("### 📝 分析結果")
                st.markdown(output)

                # 顯示可複製的 Markdown 格式
                with st.expander("查看可複製的 Markdown 格式"):
                    st.code(output, language="markdown")