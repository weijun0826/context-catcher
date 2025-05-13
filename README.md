# Context Catcher - OpenAI API with Streamlit

這個項目展示了如何在 Streamlit 應用程序中安全地使用 OpenAI API，自動摘要對話紀錄並生成任務清單。

## 本地開發設置

1. **Get your OpenAI API Key**:

   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key if you don't have one
   - Copy the API key (it starts with "sk-")

2. **Add your API Key to the .env file**:

   - Create a `.env` file in this project (use `.env.example` as a template)
   - Replace `your_api_key_here` with your actual OpenAI API key
   - Save the file

3. **Install dependencies**:

   ```bash
   source venv/bin/activate  # Activate the virtual environment
   pip install -r requirements.txt
   ```

4. **運行 Streamlit 應用程序**:

   ```bash
   streamlit run main.py
   ```

   應用程序將在 http://localhost:8501 啟動。

## Streamlit Cloud 部署

1. **Push your code to GitHub**:

   - Create a new GitHub repository
   - Push your code to the repository

2. **Deploy on Streamlit Cloud**:

   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account
   - Click "New app" and select your repository
   - Set the main file path to `main.py`
   - Add your OpenAI API key in the Secrets section (format shown below)

3. **設置 Streamlit Secrets**:
   - In the Streamlit Cloud dashboard, find your app
   - Go to "Settings" > "Secrets"
   - Add your API key in the following format:
   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

## Using OpenAI API in Your Code

The `openai_example.py` file shows how to use the OpenAI API. Here's the basic pattern:

1. Load the API key from the `.env` file
2. Initialize the OpenAI client
3. Make API calls using the client

## VSCode Integration

This project includes VSCode settings that help with OpenAI API integration:

- Environment variables are loaded from the `.env` file
- Python linting is enabled
- The virtual environment's packages are included in the Python path

## API Key 安全最佳實踐

- **永遠不要**將 API key 直接寫在代碼中
- **永遠不要**將包含 API key 的文件上傳到版本控制系統
- 使用 `.env` 文件存儲 API key，並確保它被 `.gitignore` 忽略
- 如果您不小心上傳了 API key，立即在 OpenAI 平台上重新生成一個新的 key
- 考慮使用環境變量或專門的密鑰管理服務來存儲敏感信息

### 上傳到 GitHub 時的安全措施

1. **使用 .gitignore**：確保 `.env` 文件被列在 `.gitignore` 中（本項目已設置）
2. **使用示例文件**：提供一個 `.env.example` 文件，顯示需要哪些環境變量，但不包含實際的 API key
3. **提交前檢查**：在提交代碼前，使用 `git status` 確認敏感文件不會被上傳
4. **使用 Git 鉤子**：考慮設置 pre-commit 鉤子來防止敏感信息被提交

### 部署注意事項

當部署到生產環境時：

- 使用環境變量而不是 `.env` 文件
- 考慮使用 Streamlit Secrets Management 或其他密鑰管理服務
- 定期輪換您的 API key

## Troubleshooting

If you encounter issues:

1. Make sure your API key is correctly set in the `.env` file
2. Ensure the virtual environment is activated
3. Check that all dependencies are installed
4. Verify your OpenAI account has sufficient credits
