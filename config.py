import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
GROUP_ID = int(os.getenv("GROUP_ID"))

COPYRIGHT_TEXT = """🤖 Powered by @YourBotName
📦 开发：XXX工作室 仅供授权使用
💬 定制联系：@YourContact"""

DEFAULT_START_MESSAGE = """欢迎使用投稿机器人！ 📮

直接发送图文消息即可投稿，我们会尽快处理。

使用 /help 查看帮助"""
