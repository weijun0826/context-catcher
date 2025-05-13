# Context Catcher - 對話摘要與任務產生器

![Context Catcher Demo](demo_screenshot.png)

Context Catcher 是一個基於 OpenAI API 的 Streamlit 應用程序，能夠自動分析對話紀錄，生成摘要並產出任務清單。這個工具特別適合處理會議記錄、團隊討論和客戶對話，幫助用戶快速理解重點並追蹤待辦事項。

## 🚀 主要功能

- **對話分析**：自動理解並分析對話內容
- **摘要生成**：提供簡潔的 3-5 行摘要
- **任務清單**：自動提取對話中的任務項目，包含負責人和截止日期
- **一鍵範例**：提供範例對話快速體驗功能
- **匯出功能**：支持複製或下載 Markdown 格式的結果
- **移動端優化**：響應式設計，在手機上也能舒適使用
- **使用者反饋**：整合 Google Form 收集用戶意見

## 📋 需求

- Python 3.7+
- OpenAI API Key
- Streamlit 1.0.0+

## 🛠️ 安裝與設置

1. **Clone 儲存庫**

```bash
git clone https://github.com/yourusername/context-catcher.git
cd context-catcher
```

2. **安裝依賴**

```bash
pip install -r requirements.txt
```

3. **設置 API Key**

創建 `.env` 文件，添加你的 OpenAI API Key：

```
OPENAI_API_KEY=your_api_key_here
```

或在 Streamlit Cloud 中添加到 Secrets 中。

4. **啟動應用**

```bash
streamlit run main.py
```

對於着陸頁：

```bash
streamlit run landing_page.py
```

## 📱 使用方法

1. 在文本框中貼上對話記錄，或使用「一鍵貼上範例」按鈕選擇預設範例
2. 點擊「分析對話紀錄」按鈕
3. 查看生成的摘要和任務清單
4. 複製或下載分析結果

## 📸 創建 Demo GIF

我們提供了一個腳本來幫助你創建演示 GIF：

```bash
pip install pyautogui pillow
python demo_gif_creator.py
```

按照屏幕上的指示操作，完成後會生成演示 GIF 文件。

## 🔄 使用者反饋

我們重視您的意見！點擊應用中的「提供反饋」按鈕，分享您的使用體驗和建議。主要收集以下反饋：

1. 應用是否容易上手？
2. 使用過程中遇到哪些困難？
3. 最希望添加什麼新功能？

## 📊 Landing Page

使用 `landing_page.py` 來展示應用的主要功能和優勢。這個頁面包含：

- 功能亮點
- 使用說明
- 用戶評價
- 常見問題
- 行動號召按鈕

## 📄 文件結構

```
context-catcher/
├── .env                     # API Key 環境變量（未包含在 Git 中）
├── .gitignore               # Git 忽略文件
├── main.py                  # 主要應用代碼
├── landing_page.py          # 着陸頁面
├── demo_gif_creator.py      # Demo GIF 創建腳本
├── feedback_form_template.html # Google Form 反饋表單模板
├── requirements.txt         # 項目依賴
├── check_api_key.py         # API Key 檢查工具
├── check_account.py         # 賬戶檢查工具
├── test_embeddings.py       # Embeddings 測試工具
└── README.md                # 項目說明
```

## 🤔 常見問題

### API Key 無法正常工作？

使用 `check_api_key.py` 腳本來驗證你的 API Key：

```bash
python check_api_key.py
```

### 賬戶配額問題？

使用 `check_account.py` 來檢查你的賬戶狀態：

```bash
python check_account.py
```

## 📋 後續開發計劃

- [ ] 多語言支持
- [ ] 自定義提示詞選項
- [ ] 集成到日曆和任務管理工具
- [ ] 文件上傳分析功能
- [ ] 語音轉文字功能

## 📝 授權

MIT

---

使用 Context Catcher 提高您的工作效率！如有任何問題，請隨時提出 issue 或聯繫我們。
