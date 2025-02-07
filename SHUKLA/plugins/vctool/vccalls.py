from ... import *
from pyrogram import filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat


# همون imports قبلی بدون تغییر ...

async def get_vc_call(client, message):
    chat_id = message.chat.id
    chat_peer = await client.resolve_peer(chat_id)
    if isinstance(chat_peer,
        (InputPeerChannel, InputPeerChat)
    ):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(
                    GetFullChannel(channel=chat_peer)
                )
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(
                    GetFullChat(chat_id=chat_peer.chat_id)
                )
            ).full_chat
            
        if full_chat is not None:
            return full_chat.call
            
    return False

@app.on_message(cdx(["svc", "startvc"]) & ~filters.private)
@sudo_users_only
async def create_video_chat(client, message):
    chat_id = message.chat.id
    try:
        aux = await eor(message, "**🔄 در حال پردازش ...**")
        vc_call = await get_vc_call(client, message)
        if vc_call:
            return await aux.edit("**🤖 ویس چت در حال حاضر فعال است❗**")
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            CreateGroupCall(
                peer=peer,
                random_id=client.rnd_id() // 9000000000,
            ),
        )
        await aux.edit("**🤖 ویس چت با موفقیت شروع شد 🌿**")
    except Exception as e:
        print(f"خطا: {e}")
        pass

@app.on_message(cdx(["dvc", "evc", "stopvc", "endvc"]) & ~filters.private)
@sudo_users_only
async def discard_video_chat(client, message):
    user_id = message.from_user.id
    try:
        aux = await eor(message, "**🔄 در حال پردازش ...**")
        vc_call = await get_vc_call(client, message)
        if not vc_call:
            return await aux.edit("**🤖 ویس چت هنوز شروع نشده است❗**")
        await client.invoke(
            DiscardGroupCall(call=vc_call)
        )
        return await aux.edit("**🤖 ویس چت با موفقیت پایان یافت 🌿**")
    except Exception as e:
        print(f"خطا: {e}")
        pass

@app.on_message(cdx(["rvc", "restartvc"]) & ~filters.private)
@sudo_users_only
async def discard_video_chat(client, message):
    chat_id = message.chat.id
    try:
        aux = await eor(message, "**🔄 در حال پردازش ...**")
        vc_call = await get_vc_call(client, message)
        if not vc_call:
            return await aux.edit("**🤖 ویس چت هنوز شروع نشده است❗**")
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            DiscardGroupCall(call=vc_call)
        )
        await aux.edit("**🤖 ویس چت با موفقیت پایان یافت 🌿**")
        await client.invoke(
            CreateGroupCall(
                peer=peer,
                random_id=client.rnd_id() // 9000000000,
            ),
        )
        return await aux.edit("**🤖 ویس چت با موفقیت ریستارت شد 🌿**")
    except Exception as e:
        print(f"خطا: {e}")
        pass

__NAME__ = "ویس چت"
__MENU__ = """
**با دستورات ساده ویس چت را در گروه یا 
کانال خود شروع یا متوقف کنید.**

`.svc` - شروع ویس چت
`.dvc` - پایان ویس چت
`.rvc` - ریستارت ویس چت
"""
