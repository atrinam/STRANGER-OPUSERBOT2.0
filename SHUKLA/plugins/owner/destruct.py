import os

from ... import *
from pyrogram import filters


@app.on_message(cdz(["😋🥰", "op", "wow", "super", "😋😍"])
    & filters.private & filters.me)
async def self_media(client, message):
    try:
        replied = message.reply_to_message
        if not replied:
            return
        if not (replied.photo or replied.video):
            return
        location = await client.download_media(replied)
        await client.send_document("me", location)
        os.remove(location)
    except Exception as e:
        print(f"خطا: {e}")
        return


__NAME__ = "ذخیره‌ساز"
__MENU__ = f"""
**🥀 دانلود و ذخیره عکس و ویدیوهای 
خودنابودشونده در پیام‌های ذخیره شده ✨**

`.op` - این دستور را با ریپلای روی 
عکس/ویدیو خودنابودشونده استفاده کنید.

**🌿 دستورات دیگر:**
[😋🥰, wow, super, 😋😍]
"""
