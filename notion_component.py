import streamlit as st
import datetime
from notion_integration import NotionIntegration, get_notion_credentials_from_secrets, parse_analysis_result
from utils import extract_summary_title

# 獲取本地時區的時間
def get_local_time():
    """獲取當前本地時間，包含時區信息"""
    # 使用本地時區
    local_tz = datetime.datetime.now().astimezone().tzinfo
    return datetime.datetime.now(local_tz)

def render_notion_section(ui_text, analysis_result=None):
    """
    Render the Notion integration section in the Streamlit app.

    Args:
        ui_text: Dictionary containing UI text in the current language
        analysis_result: The analysis result text (optional)
    """
    # Add Notion-specific text to UI text dictionary if not present
    if "notion_section_title" not in ui_text:
        ui_text.update({
            "notion_section_title": "Export to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "匯出到 Notion",
            "notion_description": "Send your analysis results directly to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "將分析結果直接發送到 Notion",
            "notion_api_key_label": "Notion API Key" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "Notion API Key",
            "notion_database_id_label": "Notion Database ID" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "Notion 資料庫 ID",
            "notion_title_label": "Page Title" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "頁面標題",
            "notion_send_button": "Send to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "發送到 Notion",
            "notion_test_connection": "Test Connection" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "測試連接",
            "notion_connection_success": "✅ Connected to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "✅ 已連接到 Notion",
            "notion_connection_failed": "❌ Connection failed" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "❌ 連接失敗",
            "notion_send_success": "✅ Successfully sent to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "✅ 已成功發送到 Notion",
            "notion_send_failed": "❌ Failed to send to Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "❌ 發送到 Notion 失敗",
            "notion_view_in_notion": "View in Notion" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "在 Notion 中查看",
            "notion_no_analysis": "Please analyze a conversation first" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "請先分析對話",
            "notion_api_key_help": "You can get your API key from https://www.notion.so/my-integrations" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "您可以從 https://www.notion.so/my-integrations 獲取 API key",
            "notion_database_id_help": "The ID of the database where you want to save the analysis" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "您想要保存分析結果的資料庫 ID",
            "notion_setup_instructions": "How to set up Notion integration" if "language_selector" in ui_text and ui_text.get("language_selector") == "Select Language" else "如何設置 Notion 集成",
        })

    # Get credentials from secrets
    credentials = get_notion_credentials_from_secrets()

    # Initialize Notion integration
    notion = NotionIntegration(
        api_key=credentials.get("api_key"),
        database_id=credentials.get("database_id")
    )

    # Create an expander for Notion integration
    with st.expander(f"📘 {ui_text['notion_section_title']}", expanded=True):
        st.write(ui_text["notion_description"])

        # Auto-test connection if credentials are available
        if credentials.get("api_key") and credentials.get("database_id"):
            with st.spinner("Testing Notion connection..."):
                result = notion.test_connection()
                if result["success"]:
                    st.success(ui_text["notion_connection_success"])

                    # If database ID is provided, get database info
                    db_info = notion.get_database_info()
                    if db_info["success"]:
                        st.success(f"✅ {ui_text.get('language_selector') == 'Select Language' and 'Connected to database:' or '已連接到資料庫:'} {db_info.get('title', 'Untitled')}")
                    else:
                        st.warning(f"⚠️ {db_info.get('message', 'Failed to connect to database')}")
                        # Add helpful guidance for database access issues
                        if "object_not_found" in db_info.get('message', ''):
                            st.error(f"""
                            **請確保您已完成以下步驟：**
                            1. 在 Notion 中創建了一個資料庫
                            2. 在 https://www.notion.so/my-integrations 創建了一個整合
                            3. 在 Notion 中與您的整合共享了資料庫（點擊資料庫右上角的「Share」按鈕，添加您的整合）
                            4. 資料庫 ID 是正確的（從資料庫 URL 中獲取）
                            """)
                else:
                    st.error(f"{ui_text['notion_connection_failed']}: {result.get('message', '')}")
                    # Add helpful guidance for API connection issues
                    if "unauthorized" in result.get('message', '').lower():
                        st.error("請確保您的 Notion API Key 是正確的，並且具有訪問權限。")

        # Setup instructions
        st.markdown(f"**{ui_text['notion_setup_instructions']}:**")
        st.markdown("""
        1. Create a Notion integration at https://www.notion.so/my-integrations
        2. Get your API key from the integration page
        3. Create a database in Notion where you want to save your analysis results
        4. Share the database with your integration (click "Share" in Notion and add your integration)
        5. Copy the database ID from the URL (it's the part after the workspace name and before the question mark)
        """)

        # Check if credentials are already set in secrets
        has_api_key = bool(credentials.get("api_key"))
        has_database_id = bool(credentials.get("database_id"))

        # API Key input
        if has_api_key:
            st.success(f"{ui_text.get('language_selector') == 'Select Language' and 'Notion API Key is set in secrets' or 'Notion API Key 已在 secrets 中設置'}")
            notion_api_key = credentials.get("api_key", "")
        else:
            notion_api_key = st.text_input(
                ui_text["notion_api_key_label"],
                value="",
                type="password",
                help=ui_text["notion_api_key_help"],
                key="notion_api_key_input"
            )

        # Database ID input
        if has_database_id:
            st.success(f"{ui_text.get('language_selector') == 'Select Language' and 'Notion Database ID is set in secrets' or 'Notion 資料庫 ID 已在 secrets 中設置'}")
            notion_database_id = credentials.get("database_id", "")
        else:
            notion_database_id = st.text_input(
                ui_text["notion_database_id_label"],
                value="",
                help=ui_text["notion_database_id_help"],
                key="notion_database_id_input"
            )

        # Update the Notion integration with the input values
        notion.set_api_key(notion_api_key)
        notion.set_database_id(notion_database_id)

        # Test connection button - only show if credentials are not from secrets
        if not (has_api_key and has_database_id):
            if st.button(ui_text["notion_test_connection"], key="notion_test_connection_button"):
                with st.spinner("Testing connection..."):
                    result = notion.test_connection()

                    if result["success"]:
                        st.success(ui_text["notion_connection_success"])

                        # If database ID is provided, get database info
                        if notion_database_id:
                            db_info = notion.get_database_info()
                            if db_info["success"]:
                                st.success(f"✅ Connected to database: {db_info.get('title', 'Untitled')}")
                            else:
                                st.error(f"❌ {db_info.get('message', 'Failed to connect to database')}")
                    else:
                        st.error(f"{ui_text['notion_connection_failed']}: {result.get('message', '')}")

        # Only show the send section if there's an analysis result
        if analysis_result:
            st.markdown("---")

            # Parse the analysis result
            parsed_result = parse_analysis_result(analysis_result)

            # Get a meaningful title from the summary content using the utility function
            extracted_title = extract_summary_title(analysis_result)

            # Use the stored analysis timestamp if available, otherwise use current time
            # Ensure we have a timezone-aware datetime with microseconds removed for consistent formatting
            current_time = get_local_time().replace(microsecond=0)

            # Get the timestamp from session state or use current time
            analysis_time = st.session_state.get("analysis_timestamp", current_time)

            # Format with full time including seconds for accuracy
            time_str = analysis_time.strftime('%Y-%m-%d %H:%M:%S')

            # Combine the extracted title with the timestamp
            default_title = f"{extracted_title} ({time_str})"

            # Title input
            notion_page_title = st.text_input(
                ui_text["notion_title_label"],
                value=default_title,
                key="notion_page_title_input"
            )

            # Send button
            if st.button(ui_text["notion_send_button"], key="notion_send_button"):
                if not notion_api_key or not notion_database_id:
                    st.error("Please enter both Notion API Key and Database ID")
                else:
                    with st.spinner("Sending to Notion..."):
                        result = notion.create_page_with_analysis(
                            title=notion_page_title,
                            summary=parsed_result["summary"],
                            todo_list=parsed_result["todo_list"]
                        )

                        if result["success"]:
                            st.success(ui_text["notion_send_success"])

                            # Add a link to view the page in Notion
                            if "url" in result and result["url"]:
                                st.markdown(f"[{ui_text['notion_view_in_notion']}]({result['url']})")
                        else:
                            st.error(f"{ui_text['notion_send_failed']}: {result.get('message', '')}")
        else:
            st.info(ui_text["notion_no_analysis"])
