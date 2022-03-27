import asyncio
import uuid
import aiofiles
import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed

headers = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}


# 下载视频
@retry(stop=stop_after_attempt(4), wait=wait_fixed(10))
async def run(url, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            async with aiofiles.open(name, "wb") as fp:
                while True:
                    chunk = await r.content.read(64 * 1024)
                    if not chunk:
                        break
                    await fp.write(chunk)
                print("\r", '任务文件 ', name, ' 下载成功', end="", flush=True)


async def downImg(session, url, filename):
    url=url.replace('-sign', '') #这部很重要,去掉签名验证,防止403
    async with session.get(url, headers=headers) as r:
        content = await r.content.read()
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(content)
        print("\r", '任务文件 ', filename, ' 下载成功', end="", flush=True)

# 下载图片
async def downImages(urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        jpgFiles = []
        # print(urls)
        for url in urls:
            jpgname = str(uuid.uuid4()) + '.jpg'
            jpgFiles.append(jpgname)
            task = asyncio.create_task(downImg(session, url, jpgname))
            tasks.append(task)
        await asyncio.wait(tasks)
        return jpgFiles
