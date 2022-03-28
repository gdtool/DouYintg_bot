import aiohttp


# 异步解析视频或图文信息
async def getDouYinInfo(url):
    share_url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
    }
    # 获取重定向url
    async with aiohttp.ClientSession() as session:
        async with session.get(share_url, headers=headers) as r:
            url = r.url
            print(url)
            id = url.parts[3]  # 获取视频id
            # 请求真实地址
            url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + id
            async with session.get(url, headers=headers) as r:
                json = await r.json()
                nickname = json['item_list'][0]['author']['nickname']
                unique_id = json['item_list'][0]['author']['short_id']
                desc = json['item_list'][0]['desc']
                print(nickname, unique_id, desc)
                # 图片
                if json['item_list'][0]['images'] is not None:
                    list = []
                    for val in json['item_list'][0]['images']:
                        list.append(val['url_list'][0])
                    return list, nickname, unique_id, desc
                else:
                    download_url = json['item_list'][0]['video']['play_addr']['url_list'][0].replace('wm', '')
                    # 最后一个参数是视频封面
                    return download_url, nickname, unique_id, desc, json['item_list'][0]['video']['cover']['url_list'][
                        0]

# asyncio.get_event_loop().run_until_complete(getDouYinInfo2('https://v.douyin.com/NuqHsbN/'))
