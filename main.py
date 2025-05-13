import streamlit as st
import os

# 嘗試導入 openai 庫
try:
    import openai
    openai_import_error = None
except ImportError as e:
    openai_import_error = str(e)
    st.error(f"無法導入 openai 庫: {e}")
    st.info("請確保已安裝 openai 庫: pip install openai==1.12.0")

# 設定你的 API 金鑰（從 Streamlit secrets 獲取）
try:
    api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
except Exception as e:
    st.sidebar.error(f"無法獲取 API key: {e}")
    api_key = None

# 只有在成功導入 openai 庫時才初始化客戶端
if openai_import_error is None and api_key:
    try:
        # 顯示 OpenAI 庫版本，幫助診斷問題
        st.sidebar.info(f"OpenAI 庫版本: {openai.__version__}")

        # 使用最簡單的方式初始化客戶端，只傳入 API key
        client = openai.OpenAI(api_key=api_key)
        st.sidebar.success("API key 已載入且 OpenAI 客戶端已初始化")
    except Exception as e:
        st.sidebar.error(f"初始化 OpenAI 客戶端時出錯: {e}")
        # 嘗試使用舊版 API 初始化方式
        try:
            st.sidebar.warning("嘗試使用替代方法初始化 OpenAI 客戶端...")
            openai.api_key = api_key  # 直接設置 API key
            client = openai.Client()  # 不傳入任何參數
            st.sidebar.success("使用替代方法成功初始化 OpenAI 客戶端")
        except Exception as e2:
            st.sidebar.error(f"替代初始化方法也失敗: {e2}")
            client = None
else:
    client = None
    if not openai_import_error:
        st.sidebar.error("未找到 API key，請確認 Streamlit secrets 或 .env 文件中包含 OPENAI_API_KEY")

st.title("🧠 Context Catcher")
st.subheader("自動摘要你的對話紀錄 & 任務清單產出")

# 輸入區域
chat_input = st.text_area("請貼上你的對話紀錄", height=300)

if st.button("分析對話紀錄"):
    # 檢查是否有導入錯誤
    if openai_import_error:
        st.error("無法使用 OpenAI API，因為 openai 庫未正確導入。")
        st.info("請聯繫管理員解決此問題。")
    # 檢查客戶端是否可用
    elif client is None:
        st.error("OpenAI 客戶端未初始化。")
        st.info("請確保 API key 已正確設置，並且 openai 庫已正確安裝。")
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
            try:
                # 使用安全的方式調用 OpenAI API
                st.info("正在調用 OpenAI API...")

                # 定義通用參數
                model = "gpt-3.5-turbo"
                messages = [{"role": "user", "content": prompt}]
                temperature = 0.3
                max_tokens = 800

                try:
                    # 嘗試使用新版 API
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    output = response.choices[0].message.content
                except AttributeError:
                    # 如果新版 API 失敗，嘗試使用舊版 API
                    st.warning("使用替代 API 調用方法...")
                    try:
                        # 嘗試使用舊版 API 格式
                        response = openai.ChatCompletion.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                        )
                        output = response.choices[0].message.content
                    except Exception as e3:
                        raise Exception(f"新舊 API 調用方法都失敗: {e3}")

                st.markdown("### 📝 分析結果")
                st.markdown(output)

                # 顯示可複製的 Markdown 格式
                with st.expander("查看可複製的 Markdown 格式"):
                    st.code(output, language="markdown")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                st.info("如果遇到 API 錯誤，請檢查您的 API key 是否有效，以及是否有足夠的配額。")
                st.error(f"詳細錯誤信息: {str(e)}")