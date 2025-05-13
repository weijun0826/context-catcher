import streamlit as st
import base64

# Page configuration
st.set_page_config(
    page_title="Context Catcher | 對話摘要與任務產生器",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the landing page
st.markdown("""
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1000px;
    }
    
    h1, h2, h3 {
        color: #1E3A8A;
    }
    
    .hero-section {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .feature-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .cta-button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }
    
    .cta-button:hover {
        background-color: #1E40AF;
    }
    
    .testimonial {
        font-style: italic;
        padding: 1rem;
        border-left: 4px solid #1E3A8A;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6B7280;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    .demo-gif {
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        max-width: 100%;
    }
    
    @media (max-width: 768px) {
        .feature-card {
            width: 100%;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .hero-section {
            padding: 1rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Function to generate a GitHub-style badge
def github_badge(text, bg_color, text_color="#fff"):
    return f"""<span style="
        background-color: {bg_color};
        color: {text_color};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-right: 5px;
    ">{text}</span>"""

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">🧠 Context Catcher</h1>
    <h2 style="font-weight: normal; color: #4B5563; margin-bottom: 2rem;">
        一鍵轉換對話紀錄成摘要和任務清單
    </h2>
    
    <div>
        {0}
        {1}
        {2}
    </div>
</div>
""".format(
    github_badge("AI 工具", "#1E3A8A"),
    github_badge("會議助手", "#2563EB"),
    github_badge("工作效率", "#3B82F6")
), unsafe_allow_html=True)

# Add the demo GIF
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # You'll need to create and add your own demo GIF
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://via.placeholder.com/800x450.png?text=Context+Catcher+Demo" alt="Context Catcher Demo" class="demo-gif">
    </div>
    """, unsafe_allow_html=True)
    st.caption("Context Catcher 如何工作的演示")

# Start using button
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="#" class="cta-button">立即開始使用</a>
    </div>
    """, unsafe_allow_html=True)

# Features section
st.markdown("## 💡 主要功能")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 智能對話分析</h3>
        <p>利用 OpenAI 強大的 GPT 模型，分析任何對話內容，不論是會議記錄、客戶對話還是團隊討論。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>✅ 自動任務提取</h3>
        <p>自動識別並列出對話中的所有任務項目，包括負責人和截止日期，讓您不會錯過任何重要工作。</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📝 摘要生成</h3>
        <p>生成簡潔的對話摘要，幫助您快速理解長時間會議或複雜討論的重點。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>💾 一鍵匯出</h3>
        <p>將分析結果輕鬆匯出為 Markdown 格式，方便您在任何工具中使用或與團隊分享。</p>
    </div>
    """, unsafe_allow_html=True)

# How it works section
st.markdown("## 🛠️ 如何使用")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>1️⃣ 貼上對話</h3>
        <p>將您的會議記錄、客戶對話或團隊討論內容貼到輸入框中。不確定？使用我們的範例測試！</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>2️⃣ 點擊分析</h3>
        <p>點擊「分析對話紀錄」按鈕，讓 AI 智能分析您的內容，這只需要幾秒鐘。</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>3️⃣ 獲取結果</h3>
        <p>查看生成的摘要和任務清單，一鍵複製或下載為 Markdown 格式，輕鬆整合到您的工作流程。</p>
    </div>
    """, unsafe_allow_html=True)

# Testimonials
st.markdown("## 💬 用戶評價")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="testimonial">
        "Context Catcher 幫我節省了大量整理會議紀錄的時間，現在我可以專注於執行任務而非記錄它們。"
        <br><br>
        <strong>— 王小明，專案經理</strong>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial">
        "作為遠端團隊的領導者，這個工具幫助我確保所有成員都理解了會議中分配的任務和責任。"
        <br><br>
        <strong>— 林小華，技術主管</strong>
    </div>
    """, unsafe_allow_html=True)

# FAQ Section
st.markdown("## ❓ 常見問題")

with st.expander("Context Catcher 是如何工作的？"):
    st.write("Context Catcher 使用 OpenAI 的 GPT 模型分析您的對話內容，識別關鍵點並提取任務項目。它能夠理解上下文，並生成簡潔明了的摘要和任務清單。")

with st.expander("我的數據是否安全？"):
    st.write("我們非常重視您的數據安全。您的對話內容僅用於處理您的請求，不會被永久存儲或用於訓練模型。所有資料傳輸均使用加密保護。")

with st.expander("Context Catcher 支持哪些語言？"):
    st.write("目前，Context Catcher 主要支持中文和英文對話分析。我們計劃在未來版本中增加更多語言支持。")

with st.expander("我可以集成這個工具到我的工作流程中嗎？"):
    st.write("是的！Context Catcher 生成的結果可以輕鬆導出為 Markdown 格式，方便您集成到任何支持 Markdown 的工具中，如 Notion、GitHub、Trello 等。")

# CTA Section
st.markdown("""
<div style="text-align: center; margin: 3rem 0; padding: 2rem; background-color: #f0f9ff; border-radius: 12px;">
    <h2>準備好提升您的工作效率了嗎？</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">
        從現在開始，讓 Context Catcher 幫您自動處理對話分析和任務提取。
    </p>
    <a href="#" class="cta-button">立即開始使用</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 Context Catcher | 📧 <a href="mailto:info@contextcatcher.com">info@contextcatcher.com</a></p>
    <p>由 AI 技術驅動，為提升工作效率而設計</p>
</div>
""", unsafe_allow_html=True)
