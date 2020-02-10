## wechatPost

### 介绍
flask框架搭建的微信公众号图片托管网页，为学习flask开发编写的前后端分离简单demo。

### 配置与部署
#### config.py
在根目录创建config.py，填入在[微信公众平台](https://mp.weixin.qq.com)配置的APPID,APPSECRET,TOKEN等，以及mysql数据库连接URI，服务器存放原图、缩略图的目录。
```
TOKEN = 'token'
APPID = 'wx****************'
APPSECRET = '********************************'
SCOPE = 'snsapi_base'
DB_URI = 'mysql+pymysql://username:password@host:port/dir'
UPLOAD_FOLDER = '/user_files/imgdir'
THUMBNAIL_FOLDER = '/user_files/thumbnaildir'
```

#### 前端
前端使用vue框架编写，见[wechatPostWeb](https://github.com/Antonovvv/wechatPostWeb)，打包后在[main.py](./views/main.py)修改目录。

#### 部署
安装MySQL，Nginx，Gunicorn。
参考配置文件[nginx.conf](./server_config/nginx.conf),[gunicorn.conf.py](./server_config/gunicorn.conf.py)

启动命令：`gunicorn -c gunicorn.conf.py app:app`
可以选用Supervisor作进程管理。

### 填坑相关
[微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)

[微信公众号网页授权](https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html)
