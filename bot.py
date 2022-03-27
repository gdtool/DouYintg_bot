import datetime
import os
import re
import uuid
# import socks
from telethon import TelegramClient, events

import douyin
import util

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = TelegramClient(None, API_ID, API_HASH,
                     # proxy=(socks.HTTP, '127.0.0.1', 10809)
                     ).start(
    bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.client.send_message(event.chat_id, '向我发送抖音视频的分享链接,下载无水印视频或图片,有问题请留言 @bzhzq')


captionTemplate = '''标题: %s
昵称: %s
抖音号： %s
'''
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式


@bot.on(events.NewMessage)
async def echo_all(event):
    text = event.text
    print(str(datetime.datetime.now()) + ':' + text)
    if 'v.douyin' in text:

        urls = re.findall(pattern,
                          text)
        msg1 = await event.client.send_message(event.chat_id,
                                               '正在下载...')

        msg2 = await event.client.send_message(event.chat_id,
                                               '🤞')
        info = douyin.getDouYinInfo(urls[0])

        if isinstance(info[0], list):
            jpgFiles = await util.downImages(info[0])
            print('------------')
            await event.client.send_file(event.chat_id,
                                         jpgFiles,
                                         caption=captionTemplate % (
                                             info[3], '#' + info[1], '#' + info[2]),
                                         reply_to=event.id, )
            await msg1.delete()
            await msg2.delete()
            for jpgFile in jpgFiles:
                os.remove(jpgFile)

        else:
            # print(info[0])
            uuidstr = str(uuid.uuid4())
            filename = uuidstr + '.mp4'
            cover = uuidstr + '.jpg'
            # 下载视频
            await util.run(info[0], filename)
            # 下载封面
            await util.run(info[4], cover)
            # 发送视频
            await event.client.send_file(event.chat_id,
                                         filename,
                                         supports_streaming=True,
                                         thumb=cover,
                                         caption=captionTemplate % (
                                             info[3], '#' + info[1], '#' + info[2]),
                                         reply_to=event.id,
                                         )
            await msg1.delete()
            await msg2.delete()
            os.remove(filename)
            os.remove(cover)


print('bot启动....')
bot.run_until_disconnected()
