[![ss203242430](https://circleci.com/gh/ss203242430/punch_line_bot.svg?style=svg)](https://app.circleci.com/pipelines/github/ss203242430/punch_line_bot)

# 專案說明

## 開發環境
* Python 3.9.0 (https://www.python.org/)
* Django 3.1.4 (https://www.djangoproject.com/)
* Sublime Text3 (https://www.sublimetext.com/)

## 執行方法
### 測試
* 網站伺服器
1. 打開cmd並進入專案資料夾
2. 輸入指令```python manage.py runserver```
3. 打開瀏覽器進入登入頁面 (http://localhost:8000/admin/)

* LineBot設定
1. 打開cmd並進入專案資料夾
2. 輸入指令```ngrok.exe http 8000```
3. 進入LINE Developers，選擇LINE Bot並將Webhook URL設定成https://{ngrok提供的隨機碼}.ngrok.io/callback

### 正式
* 網站伺服器
1. uwsgi指令
* 啟動：```uwsgi --ini uwsgi.ini```
* 重啟：```uwsgi --reload uwsgi.pid```
* 停止：```uwsgi --stop uwsgi.pid```

### 進入資料庫cli
* ```python manage.py dbshell```

## 專案目錄簡易說明
+ ```manage.py``` ----> 管理Django專案的命令列工具
+ ```linebotserver/``` ----> 包含重要的設定檔案，如settings.py、urls.py
+ ```applications/``` ----> 包含大部分應用程式的程式檔
+ ```applications/admin.py``` ----> 註冊後台顯示資料表
+ ```applications/api.py``` ----> API定義
+ ```applications/cron.py``` ----> 排程定義
+ ```applications/models.py``` ----> 資料庫models定義
+ ```applications/test.py``` ----> 測試程式
+ ```applications/views.py``` ----> 接收LINE BOT的請求及回應訊息
+ ```static/``` ----> 對外公開的檔案 (例如圖片檔)