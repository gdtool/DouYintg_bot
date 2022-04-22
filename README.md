# DouYintg_bot
简单的无水印抖音视频图文异步下载电报机器人


### docker运行



#### 安装 docker
```
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh --mirror Aliyun&&systemctl enable docker&&systemctl start docker

```

#### 安装docker-compose

```yaml
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose &&chmod +x /usr/local/bin/docker-compose
```


### 配置
创建目录 /douyin
```yaml
mkdir /douyin
```
### 编辑docker-compose.yml

```angular2html
      
      API_ID: 2222222222222
      API_HASH: 22222
      BOT_TOKEN: 5161622943:AAEQwISVYsatw_5UcC6MIs8GtmrlokdYeyY
```

### 启动项目

```yaml
docker-compose up 
```

查看日志

```
docker logs -f douyintgbot
```











