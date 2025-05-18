import datetime

def extract_summary_title(analysis_result):
    """
    Extract a meaningful title from the analysis result.
    
    Args:
        analysis_result: The full analysis result text
        
    Returns:
        A string containing a concise title derived from the summary
    """
    if not analysis_result:
        return "Untitled Analysis"

    # Split by sections
    sections = analysis_result.split("##")

    for section in sections:
        if "📌" in section or "Summary" in section or "摘要" in section:
            # Get the first bullet point that's not a placeholder
            lines = section.strip().split("\n")
            for line in lines:
                if line.strip().startswith("- ") and not (
                    "[" in line and "]" in line and 
                    ("主題" in line or "topic" in line or "背景" in line or "background" in line)
                ):
                    # Clean up the title - remove placeholders and brackets
                    title = line.strip()[2:].strip()
                    title = title.replace("[", "").replace("]", "")
                    
                    # Limit length for display purposes
                    if len(title) > 50:
                        # Try to find a natural break point
                        break_point = title[:50].rfind(",")
                        if break_point == -1:
                            break_point = title[:50].rfind("，")
                        if break_point == -1:
                            break_point = title[:50].rfind(".")
                        if break_point == -1:
                            break_point = title[:50].rfind("。")
                        if break_point == -1:
                            break_point = title[:50].rfind(" ")
                            
                        if break_point != -1:
                            return title[:break_point + 1] + "..."
                        else:
                            return title[:50] + "..."
                    return title
            
            # If we didn't find a good bullet point, use the section title
            section_title = section.strip().split("\n")[0].strip() if "\n" in section else section.strip()
            if section_title:
                return "Summary of " + section_title[:40]

    # If no summary found, return a default title with timestamp
    return f"Analysis {datetime.datetime.now().strftime('%Y-%m-%d')}"
