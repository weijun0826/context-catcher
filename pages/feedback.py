import streamlit as st

# 設置頁面配置
st.set_page_config(
    page_title="Context Catcher - 使用者反饋",
    page_icon="🧠",
    layout="centered"
)

# 頁面標題
st.title("🧠 Context Catcher 使用者反饋")
st.markdown("### 您的意見對我們非常重要！")

# 使用 HTML 組件嵌入 Google 表單
st.components.v1.html("""
<div style="display: flex; justify-content: center;">
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSegSiDo03OePxu48EK5WMTcIeq_OyQkia_rCpIwu3wyimrm5w/viewform?embedded=true" 
            width="100%" 
            height="800" 
            frameborder="0" 
            marginheight="0" 
            marginwidth="0"
            style="background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        載入中…
    </iframe>
</div>
""", height=850)

# 添加返回按鈕
if st.button("返回主頁"):
    st.switch_page("main.py")

# 頁腳
st.markdown("---")
st.markdown("© 2025 Context Catcher")
