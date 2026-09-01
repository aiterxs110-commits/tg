from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import GROUP_ID
from database import get_start_message, set_start_message, get_buttons, add_button, delete_button, clear_buttons
from utils import is_admin

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    buttons = get_buttons()
    if buttons:
        kb_buttons = []
        for btn in buttons:
            if btn["type"] == "url":
                kb_buttons.append([InlineKeyboardButton(text=btn["text"], url=btn["value"])])
            else:
                kb_buttons.append([InlineKeyboardButton(text=btn["text"], callback_data=f"btn_{buttons.index(btn)}")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
        await message.reply(get_start_message(), reply_markup=kb)
    else:
        await message.reply(get_start_message())

@router.message(Command("adminhelp"))
async def cmd_adminhelp(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    
    help_text = """管理员面板

📌 基础功能：
/start - 查看欢迎菜单
/adminhelp - 查看管理员帮助

⚙️ 欢迎语管理：
/setstart <文案>

⚙️ 按钮管理：
/addbtn <按钮名> callback <回调指令> - 回调按钮
/addbtn <按钮名> url <链接> - 链接按钮
/addbtn <按钮名> reply <回复文案> - 自定义回复
/delbtn <按钮名> - 删除按钮
/listbtns - 查看所有按钮
/clearbtns - 清空所有按钮

⚙️ 指令管理：
/addcmd <指令名> <文案> - 添加自定义指令
/delcmd <指令名> - 删除自定义指令
/listcmds - 查看所有自定义指令

⚙️ 其他：
/setgroup - 查看当前审核群 ID

📝 指令示例：
/addcmd 帮助 这是帮助内容，用户可以发送 /帮助 触发"""

    await message.reply(help_text)

@router.message(Command("setgroup"))
async def cmd_setgroup(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    await message.reply(f"✅ 当前审核群 ID：{GROUP_ID}\n（如需修改，请编辑 .env 文件中的 GROUP_ID 并重启机器人）")

@router.message(Command("setstart"))
async def cmd_setstart(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    text = message.text.replace("/setstart", "").strip()
    if not text:
        await message.reply("❌ 提供文案内容\n示例：/setstart 欢迎投稿！")
        return
    set_start_message(text)
    await message.reply(f"✅ /start 欢迎文案已更新：\n\n{text}")

# ========== 按钮管理 ==========
@router.message(Command("addbtn"))
async def cmd_addbtn(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    
    content = message.text.replace("/addbtn", "").strip()
    if not content:
        await message.reply("❌ 请提供按钮信息\n\n格式：\n/addbtn <按钮名> callback <回复文案>\n/addbtn <按钮名> url <链接>\n/addbtn <按钮名> reply <回复文案>")
        return
    
    parts = content.split(" ", 2)
    if len(parts) < 3:
        await message.reply("❌ 格式错误\n\n示例：\n/addbtn 投稿 callback 请发送图文\n/addbtn 官网 url https://example.com\n/addbtn 帮助 reply 这是帮助内容")
        return
    
    text, btn_type, value = parts[0], parts[1], parts[2]
    
    if btn_type not in ["callback", "url", "reply"]:
        await message.reply("❌ 按钮类型错误，请使用：callback、url 或 reply")
        return
    
    if btn_type == "url" and not value.startswith(("http://", "https://")):
        await message.reply("❌ 链接格式错误，请以 http:// 或 https:// 开头")
        return
    
    if add_button(text, btn_type, value):
        type_names = {"callback": "回调", "url": "链接", "reply": "自定义回复"}
        await message.reply(f"✅ 已添加按钮：{text}（类型：{type_names[btn_type]}）\n值：{value}")
    else:
        await message.reply(f"❌ 按钮名 {text} 已存在，请使用不同的名称")

@router.message(Command("delbtn"))
async def cmd_delbtn(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    text = message.text.replace("/delbtn", "").strip()
    if not text:
        await message.reply("❌ 请提供要删除的按钮名\n示例：/delbtn 投稿")
        return
    if delete_button(text):
        await message.reply(f"✅ 已删除按钮：{text}")
    else:
        await message.reply(f"❌ 未找到按钮：{text}")

@router.message(Command("listbtns"))
async def cmd_listbtns(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    buttons = get_buttons()
    if not buttons:
        await message.reply("📭 当前没有任何按钮")
        return
    type_names = {"callback": "回调", "url": "链接", "reply": "自定义回复"}
    lines = ["📋 当前按钮列表："]
    for i, btn in enumerate(buttons, 1):
        lines.append(f"{i}. {btn['text']}（类型：{type_names.get(btn['type'], btn['type'])}）")
        lines.append(f"   值：{btn['value']}")
        lines.append("")
    await message.reply("\n".join(lines))

@router.message(Command("clearbtns"))
async def cmd_clearbtns(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    buttons = get_buttons()
    if not buttons:
        await message.reply("📭 当前没有任何按钮")
        return
    clear_buttons()
    await message.reply("✅ 已清空所有按钮")

# ========== 自定义指令管理 ==========
@router.message(Command("addcmd"))
async def cmd_addcmd(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    
    content = message.text.replace("/addcmd", "").strip()
    if not content:
        await message.reply("❌ 请提供指令名和回复文案\n示例：/addcmd 帮助 这是帮助内容")
        return
    
    parts = content.split(" ", 1)
    if len(parts) < 2:
        await message.reply("❌ 格式错误\n示例：/addcmd 帮助 这是帮助内容")
        return
    
    cmd_name, reply_text = parts[0], parts[1]
    
    reserved_cmds = ["start", "adminhelp", "setgroup", "setstart", "addbtn", "delbtn", "listbtns", "clearbtns", "addcmd", "delcmd", "listcmds"]
    if cmd_name.lower() in reserved_cmds:
        await message.reply(f"❌ {cmd_name} 是系统保留指令，请使用其他名称")
        return
    
    from database import add_custom_command
    if add_custom_command(cmd_name, reply_text):
        await message.reply(f"✅ 已添加自定义指令：/{cmd_name}\n回复内容：{reply_text}")
    else:
        await message.reply(f"❌ 指令 /{cmd_name} 已存在")

@router.message(Command("delcmd"))
async def cmd_delcmd(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    
    cmd_name = message.text.replace("/delcmd", "").strip()
    if not cmd_name:
        await message.reply("❌ 请提供要删除的指令名\n示例：/delcmd 帮助")
        return
    
    from database import delete_custom_command
    if delete_custom_command(cmd_name):
        await message.reply(f"✅ 已删除自定义指令：/{cmd_name}")
    else:
        await message.reply(f"❌ 未找到指令：/{cmd_name}")

@router.message(Command("listcmds"))
async def cmd_listcmds(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ 只有管理员可以使用此指令")
        return
    
    from database import get_custom_commands
    commands = get_custom_commands()
    if not commands:
        await message.reply("📭 当前没有自定义指令")
        return
    
    lines = ["📋 当前自定义指令列表："]
    for i, (cmd, reply) in enumerate(commands.items(), 1):
        lines.append(f"{i}. /{cmd}")
        lines.append(f"   回复：{reply}")
        lines.append("")
    await message.reply("\n".join(lines))

# ========== 按钮回调 ==========
@router.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    data = callback.data
    
    if data.startswith("btn_"):
        try:
            index = int(data.split("_")[1])
            buttons = get_buttons()
            if index >= len(buttons):
                await callback.answer("按钮不存在")
                return
            btn = buttons[index]
            
            if btn["type"] == "callback":
                await callback.message.reply(btn["value"])
                await callback.answer()
            elif btn["type"] == "reply":
                await callback.message.reply(btn["value"])
                await callback.answer()
            else:
                await callback.answer("未知按钮类型")
        except (IndexError, ValueError):
            await callback.answer("按钮不存在")
    else:
        await callback.answer("未知操作")
