from datetime import datetime
from config import COPYRIGHT_TEXT

def build_submit_message(user, text: str = "") -> str:
    username = f"@{user.username}" if user.username else f"ID: {user.id}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    msg = f"""📩 新投稿
投稿人：{username}
时间：{timestamp}
───

{text if text else "（无文字内容）"}

───
{COPYRIGHT_TEXT}"""
    return msg

def is_admin(user_id: int) -> bool:
    from config import ADMIN_IDS
    return user_id in ADMIN_IDS
