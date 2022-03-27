import requests, re


# 解析视频或图文信息
def getDouYinInfo(url):
    share_url = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
    }
    response = requests.get(share_url, headers=headers)
    url = response.url  # 处理页面重定向，提取新连接
    id = re.search(r'/video/(.*?)/', url).group(1)  # 获取视频id

    # 提取带水印的视频链接地址
    url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + id
    response = requests.get(url, headers=headers)
    json = response.json()
    nickname = json['item_list'][0]['author']['nickname']
    unique_id = json['item_list'][0]['author']['short_id']
    desc = json['item_list'][0]['desc']
    # 图片
    if json['item_list'][0]['images'] is not None:
        list = []
        for val in json['item_list'][0]['images']:
            list.append(val['url_list'][0])
        return list, nickname, unique_id, desc
    else:
        download_url = json['item_list'][0]['video']['play_addr']['url_list'][0].replace('wm', '')
        # 最后一个参数是视频封面
        return download_url, nickname, unique_id, desc, json['item_list'][0]['video']['cover']['url_list'][0]
