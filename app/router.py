def route_intent(message: str) -> str:
    text = message.lower()

    meeting_keywords = [
        "會議", "會議紀錄", "逐字稿", "決議", "待辦",
        "action item", "minutes", "meeting"
    ]

    sop_keywords = [
        "sop", "標準作業", "作業流程", "操作流程",
        "流程", "步驟", "怎麼做"
    ]

    analyze_keywords = [
        "異常", "問題", "原因", "分析", "改善",
        "品質", "缺料", "少料", "溫度", "設備",
        "出餐", "錯誤", "風險"
    ]

    if any(keyword in text for keyword in meeting_keywords):
        return "meeting"

    if any(keyword in text for keyword in sop_keywords):
        return "sop"

    if any(keyword in text for keyword in analyze_keywords):
        return "analyze"

    return "general"