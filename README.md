# Modified from [bilibili-live-tools](https://github.com/Dawnnnnnn/bilibili-live-tools)
## Bilibili 直播助手

精简了log显示  
使用随机等待时间  
增加定时关闭  
增加邮件发送结果  
修复奖励不领取bug  
修复SSL在python3.7+环境下的偶然性报错  

更多功能详见原repo [Wiki](https://github.com/Dawnnnnnn/bilibili-live-tools/wiki)

Requirement
```
pip install requests
pip install rsa
pip install aiohttp
pip install termcolor
pip install colorama
```
运行：
windows环境下在cmd内键入
```
cd <path> (path为文件夹所处路径)
python main.py
```

配置邮箱：
找到mail.py文件，打开编辑
```
mail_host =
mail_user =
mail_pass =
 
From = 
To = 
```

---
辣条数量: 
  工作日:  ~150/H
  周末:  ~200/H
---
*采用晚间21时左右数据
