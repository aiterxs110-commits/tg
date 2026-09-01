from aiogram import Router, types
from aiogram.types import InputMediaPhoto, InputMediaVideo
from asyncio import sleep

from config import GROUP_ID, ADMIN_IDS
from utils import build_submit_message
from database import get_custom_commands

router = Router()

media_group_cache = {}

async def process_media_group(message: types.Message):
    group_id = message.media_group_id
    
    if group_id not in media_group_cache:
        media_group_cache[group_id] = {
            "messages": [],
            "user": message.from_user,
            "caption": message.caption or "",
            "timestamp": message.date
        }
    
    media_group_cache[group_id]["messages"].append(message)
    
    await sleep(1)
    
    if group_id in media_group_cache:
        data = media_group_cache.pop(group_id)
        messages = data["messages"]
        user = data["user"]
        caption_text = data["caption"]
        
        header = build_submit_message(user, caption_text or "")
        
        media_group = []
        for i, msg in enumerate(messages):
            if msg.photo:
                if i == 0:
                    media_group.append(
                        InputMediaPhoto(
                            media=msg.photo[-1].file_id,
                            caption=header
                        )
                    )
                else:
                    media_group.append(
                        InputMediaPhoto(media=msg.photo[-1].file_id)
                    )
            elif msg.video:
                if i == 0:
                    media_group.append(
                        InputMediaVideo(
                            media=msg.video.file_id,
                            caption=header
                        )
                    )
                else:
                    media_group.append(
                        InputMediaVideo(media=msg.video.file_id)
                    )
        
        if media_group:
            await message.bot.send_media_group(
                chat_id=GROUP_ID,
                media=media_group
            )
            
            for admin_id in ADMIN_IDS:
                await message.bot.send_message(
                    admin_id,
                    f"📩 收到新投稿（含 {len(messages)} 张图片）\n投稿人：@{user.username or user.id}"
                )

@router.message()
async def handle_message(message: types.Message):
    user = message.from_user
    
    if message.chat.type != "private":
        return
    
    if message.text and message.text.startswith("/"):
        # 检查是否是自定义指令
        cmd_name = message.text[1:].strip().split()[0]  # 去掉 / 和后面的参数
        custom_commands = get_custom_commands()
        if cmd_name in custom_commands:
            await message.reply(custom_commands[cmd_name])
            return
        # 如果是系统指令，不处理（由 admin.py 处理）
        return
    
    if message.media_group_id:
        await process_media_group(message)
        return
    
    await message.reply("✅ 已收到你的投稿，我们将尽快处理！")
    
    caption = build_submit_message(user, message.text or "")
    
    try:
        if message.text:
            await message.bot.send_message(
                chat_id=GROUP_ID,
                text=caption
            )
        elif message.photo:
            await message.bot.send_photo(
                chat_id=GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=caption
            )
        elif message.video:
            await message.bot.send_video(
                chat_id=GROUP_ID,
                video=message.video.file_id,
                caption=caption
            )
        elif message.document:
            await message.bot.send_document(
                chat_id=GROUP_ID,
                document=message.document.file_id,
                caption=caption
            )
        elif message.voice:
            await message.bot.send_voice(
                chat_id=GROUP_ID,
                voice=message.voice.file_id,
                caption=caption
            )
        elif message.audio:
            await message.bot.send_audio(
                chat_id=GROUP_ID,
                audio=message.audio.file_id,
                caption=caption
            )
        elif message.animation:
            await message.bot.send_animation(
                chat_id=GROUP_ID,
                animation=message.animation.file_id,
                caption=caption
            )
        elif message.sticker:
            await message.bot.send_sticker(
                chat_id=GROUP_ID,
                sticker=message.sticker.file_id
            )
            await message.bot.send_message(
                chat_id=GROUP_ID,
                text=caption
            )
        elif message.video_note:
            await message.bot.send_video_note(
                chat_id=GROUP_ID,
                video_note=message.video_note.file_id
            )
            await message.bot.send_message(
                chat_id=GROUP_ID,
                text=caption
            )
        else:
            await message.bot.send_message(
                chat_id=GROUP_ID,
                text=f"{caption}\n\n⚠️ 不支持的消息类型，已转发原始消息"
            )
            await message.bot.forward_message(
                chat_id=GROUP_ID,
                from_chat_id=user.id,
                message_id=message.message_id
            )
        
        for admin_id in ADMIN_IDS:
            await message.bot.send_message(
                admin_id,
                f"📩 收到新投稿\n投稿人：@{user.username or user.id}"
            )
            
    except Exception as e:
        await message.reply("❌ 投稿转发失败，请稍后重试")
        print(f"转发失败: {e}")
