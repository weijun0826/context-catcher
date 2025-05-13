import streamlit as st
import openai
import os

# 設定你的 API 金鑰（從 Streamlit secrets 獲取）
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客戶端
client = openai.OpenAI(api_key=api_key)

# 顯示 API key 狀態（僅用於調試，生產環境應移除）
if api_key:
    st.sidebar.success("API key 已載入")
else:
    st.sidebar.error("未找到 API key，請確認 Streamlit secrets 或 .env 文件中包含 OPENAI_API_KEY")

st.title("🧠 Context Catcher")
st.subheader("自動摘要你的對話紀錄 & 任務清單產出")

# 輸入區域
chat_input = st.text_area("請貼上你的對話紀錄", height=300)

if st.button("分析對話紀錄"):
    with st.spinner("AI 正在理解對話內容中..."):
        prompt = f"""
你是一個任務整理助理，請根據以下對話紀錄進行分析，產出：

1. 一段簡潔摘要（約 3-5 行）
2. 待辦事項清單（格式為：- [ ] 任務名稱 - 負責人（如有） - 截止日（如有））

對話紀錄：
{chat_input}
"""
        try:
            # 使用新版 OpenAI 客戶端
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 使用 gpt-3.5-turbo 替代 gpt-4，因為 gpt-4 可能需要特殊權限
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800,
            )
            output = response.choices[0].message.content
            st.markdown("### 📝 分析結果")
            st.markdown(output)

            # 顯示可複製的 Markdown 格式
            with st.expander("查看可複製的 Markdown 格式"):
                st.code(output, language="markdown")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
            st.info("如果遇到 API 錯誤，請檢查您的 API key 是否有效，以及是否有足夠的配額。")