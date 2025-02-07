from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound

from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues


# پخش کننده صوتی
@app.on_message(cdz(["ply", "play"]) & ~filters.private)
@sudo_users_only
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**در حال پردازش ...**")
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    type = "Audio"
    try:
        if audio:
            await aux.edit("در حال دانلود ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 لطفا یک درخواست برای پخش\nموزیک یا ویدیو ارسال کنید❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type)
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("در حال پخش!")
            elif (a.status == "playing"
                or a.status == "paused"
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"در صف قرار گرفت: {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("در حال پخش!")
    except Exception as e:
       print(f"خطا: {e}")
       return await aux.edit("**لطفا دوباره تلاش کنید!**")
    except:
        return


# پخش کننده ویدیویی
@app.on_message(cdz(["vply", "vplay"]) & ~filters.private)
@sudo_users_only
async def video_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**در حال پردازش ...**")
    video = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message
        else None
    )
    type = "Video"
    try:
        if video:
            await aux.edit("در حال دانلود ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 لطفا یک درخواست برای پخش\nموزیک یا ویدیو ارسال کنید❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type)
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("در حال پخش!")
            elif (a.status == "playing"
                or a.status == "paused"
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"در صف قرار گرفت: {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("در حال پخش!")
    except Exception as e:
       print(f"خطا: {e}")
       return await aux.edit("**لطفا دوباره تلاش کنید!**")
    except:
        return


# پخش کننده صوتی (پخش از هر جایی)
@app.on_message(cdz(["cply", "cplay"]))
@sudo_users_only
async def audio_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message,
            "**🥀 لطفا یک چت برای شروع پخش تنظیم کنید❗**"
    )
    aux = await eor(message, "**در حال پردازش ...**")
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    type = "Audio"
    try:
        if audio:
            await aux.edit("در حال دانلود ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 لطفا یک درخواست برای پخش\nموزیک یا ویدیو ارسال کنید❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type)
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("در حال پخش!")
            elif (a.status == "playing"
                or a.status == "paused"
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"در صف قرار گرفت: {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("در حال پخش!")
    except Exception as e:
       print(f"خطا: {e}")
       return await aux.edit("**لطفا دوباره تلاش کنید!**")
    except:
        return


# پخش کننده ویدیویی (پخش از هر جایی)
@app.on_message(cdz(["cvply", "cvplay"]))
@sudo_users_only
async def video_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message,
            "**🥀 لطفا یک چت برای شروع پخش تنظیم کنید❗**"
    )
    aux = await eor(message, "**در حال پردازش ...**")
    video = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message
        else None
    )
    type = "Video"
    try:
        if video:
            await aux.edit("در حال دانلود ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 لطفا یک درخواست برای پخش\nموزیک یا ویدیو ارسال کنید❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type)
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("در حال پخش!")
            elif (a.status == "playing"
                or a.status == "paused"
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"در صف قرار گرفت: {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("در حال پخش!")
    except Exception as e:
       print(f"خطا: {e}")
       return await aux.edit("**لطفا دوباره تلاش کنید!**")
    except:
        return
