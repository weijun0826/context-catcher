import os
import requests
import json
import streamlit as st
import datetime
from typing import Dict, Any, Optional, List

# 獲取本地時區的時間
def get_local_time():
    """獲取當前本地時間，包含時區信息"""
    # 使用本地時區
    local_tz = datetime.datetime.now().astimezone().tzinfo
    return datetime.datetime.now(local_tz)

class NotionIntegration:
    """
    A class to handle integration with Notion API.
    This allows sending analysis results directly to a Notion database.
    """

    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        """
        Initialize the Notion integration with API key and database ID.

        Args:
            api_key: Notion API key (optional, can be set later)
            database_id: Notion database ID (optional, can be set later)
        """
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.version = "2022-06-28"  # Notion API version

    def set_api_key(self, api_key: str) -> None:
        """Set the Notion API key."""
        self.api_key = api_key

    def set_database_id(self, database_id: str) -> None:
        """Set the Notion database ID."""
        # Use the database ID as is, without formatting
        self.database_id = database_id

    def get_headers(self) -> Dict[str, str]:
        """Get the headers required for Notion API requests."""
        if not self.api_key:
            raise ValueError("Notion API key is not set")

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": self.version
        }

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Notion API.

        Returns:
            Dict containing success status and message
        """
        if not self.api_key:
            return {"success": False, "message": "Notion API key is not set"}

        try:
            # Try to get the user's information as a simple test
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.get_headers()
            )

            if response.status_code == 200:
                return {"success": True, "message": "Successfully connected to Notion API"}
            else:
                return {
                    "success": False,
                    "message": f"Failed to connect to Notion API: {response.status_code} - {response.text}"
                }
        except Exception as e:
            return {"success": False, "message": f"Error connecting to Notion API: {str(e)}"}

    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the Notion database.

        Returns:
            Dict containing database information or error message
        """
        if not self.api_key or not self.database_id:
            return {"success": False, "message": "Notion API key or database ID is not set"}

        try:
            response = requests.get(
                f"{self.base_url}/databases/{self.database_id}",
                headers=self.get_headers()
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "title": data.get("title", [{}])[0].get("plain_text", "Untitled"),
                    "properties": data.get("properties", {})
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to get database info: {response.status_code} - {response.text}"
                }
        except Exception as e:
            return {"success": False, "message": f"Error getting database info: {str(e)}"}

    def get_status_options(self) -> List[str]:
        """
        Get available status options from the Notion database.

        Returns:
            List of status option names
        """
        db_info = self.get_database_info()
        if not db_info.get("success", False):
            return ["Not started"]  # Default fallback

        properties = db_info.get("properties", {})
        status_property = properties.get("狀態", {})

        if status_property.get("type") == "status":
            options = status_property.get("status", {}).get("options", [])
            return [option.get("name") for option in options if option.get("name")]

        return ["Not started"]  # Default fallback

    def create_page_with_analysis(self, title: str, summary: str, todo_list: str) -> Dict[str, Any]:
        """
        Create a new page in the Notion database with analysis results.

        Args:
            title: Title for the new page
            summary: Summary text from analysis
            todo_list: To-do list text from analysis

        Returns:
            Dict containing success status and message
        """
        if not self.api_key or not self.database_id:
            return {"success": False, "message": "Notion API key or database ID is not set"}

        try:
            # Get current date for deadline (default to 7 days from now)
            # Use local timezone for accurate time
            current_time = get_local_time()
            default_deadline = (current_time + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

            # Get available status options
            status_options = self.get_status_options()
            default_status = status_options[0] if status_options else "Not started"

            # Prepare the page content
            payload = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "任務名稱": {  # title type
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "狀態": {  # status type
                        "status": {
                            "name": default_status  # Using the first available status option
                        }
                    },
                    "截止日": {  # date type
                        "date": {
                            "start": default_deadline
                        }
                    },
                    "負責人": {  # person type
                        "people": []  # Empty array for people (can't assign specific people via API)
                    },
                    "任務標籤": {  # multi-select type
                        "multi_select": [
                            {
                                "name": "自動生成"
                            }
                        ]
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "摘要"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": summary}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "待辦事項"}}]
                        }
                    }
                ]
            }

            # Add task description (text type)
            payload["properties"]["任務說明"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": summary[:2000] if summary else ""  # Limit to 2000 chars
                        }
                    }
                ]
            }

            # Parse to-do list items and add them as to-do blocks
            if todo_list:
                todo_items = todo_list.strip().split('\n')
                for item in todo_items:
                    if item.strip().startswith('- [ ]') or item.strip().startswith('- [x]'):
                        # Extract the task content
                        is_checked = item.strip().startswith('- [x]')
                        task_content = item.strip()[5:].strip()  # Remove "- [ ]" or "- [x]"

                        # Add to-do block
                        todo_block = {
                            "object": "block",
                            "type": "to_do",
                            "to_do": {
                                "rich_text": [{"type": "text", "text": {"content": task_content}}],
                                "checked": is_checked
                            }
                        }
                        payload["children"].append(todo_block)

            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.get_headers(),
                data=json.dumps(payload)
            )

            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "success": True,
                    "message": "Successfully created page in Notion",
                    "page_id": data.get("id", ""),
                    "url": data.get("url", "")
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to create page: {response.status_code} - {response.text}"
                }
        except Exception as e:
            return {"success": False, "message": f"Error creating page: {str(e)}"}

# Helper functions for Streamlit UI
def get_notion_credentials_from_secrets() -> Dict[str, Optional[str]]:
    """Get Notion credentials from Streamlit secrets."""
    notion_api_key = None
    notion_database_id = None

    try:
        if "NOTION_API_KEY" in st.secrets:
            notion_api_key = st.secrets["NOTION_API_KEY"]

        if "NOTION_DATABASE_ID" in st.secrets:
            notion_database_id = st.secrets["NOTION_DATABASE_ID"]
    except Exception:
        pass

    return {
        "api_key": notion_api_key,
        "database_id": notion_database_id
    }

def parse_analysis_result(result_text: str) -> Dict[str, str]:
    """
    Parse the analysis result to extract summary and to-do list.

    Args:
        result_text: The full analysis result text

    Returns:
        Dict containing summary and todo_list
    """
    summary = ""
    todo_list = ""

    # Split by sections
    sections = result_text.split("##")

    for section in sections:
        if "📌" in section or "Summary" in section or "摘要" in section:
            summary = section.split("\n", 1)[1].strip() if "\n" in section else ""
        elif "✅" in section or "To-Do" in section or "待辦" in section:
            todo_list = section.split("\n", 1)[1].strip() if "\n" in section else ""

    # Format todo_list for better display in Notion
    # We'll do the actual replacement of "- [ ]" to "/[ ]" in the create_page_with_analysis method

    return {
        "summary": summary,
        "todo_list": todo_list
    }
