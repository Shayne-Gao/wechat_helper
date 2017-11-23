# wechat_warframe_helper
wechat helper， include many funcitons，like actbook, warframe tools, life tools and etc.

# 依赖 与安装方式
* Django Python web框架

  >pip install Django==1.11.4  
  >django-admin startproject wechat  
  >python manage.py migrate  
  >python manage.py startapp wechat 
  >python manage.py runserver 0.0.0.0:1409 

>配置可以查看wiki https://docs.djangoproject.com/en/1.11/intro/tutorial01/

* 微信sdk
pip install wechat-sdk

* Mysql
  >导入sql文件夹里的sql来新建库和表  
  >warframe相关的库为warframe  
  >记账相关的库为accountbook  

 



# 更新记录

>  2017-9-29 12:13:13 item表的namezh后面多了一个符号  
  2017-9-29 12:13:20 web版本增加了mod的图片展示  
  2017-9-29 12:13:36 web版本初步稳定 
  2017-9-19 11:26:48 新增了入侵查询 整合在wfa中  
  2017-9-19 11:27:00 修复了部分小BUG，如李明博，阴阳等甲wfb中的数字  
  2017-9-19 11:43:19 增加武器 布利斯提卡 Prime价格查询   
  2017-9-15 12:42:07 对于物品的build，做了缓存。避免了频繁查询第三方网站带来的耗时。缓存7天过期。 wfb功能的查询时间缩短了80%  
  2017-9-14 12:14:11 增加了小尾巴，在查询的结果后进行显示。内容随机  
  2017-9-14 11:46:13 对于价格记录足够的物品，将会展示近N天这个物品的最高和最低价格  
  2017-9-14 10:51:06 修复了部分物品查询不到售价的原因（因为url未quote导致）  
  2017-9-13 11:40:35 增加了物品别名的查询，增加了对Wf WF 等的兼容  
  2017-9-11 16:22:24 增加了本地缓存，几分钟内的连续查询不从wm抓数据。减小了失败的可能性  
  2017-9-6 11:17:41 给战甲增加了昵称搜索功能  
  2017-9-6 11:17:55 对搜索后面的p进行了处理，处理了大小写的Prime兼容问题  
  2017-9-5 11:21:05 更新了一些没有名字的MOD ID  
  2017-9-4 12:10:04 规范了mod的ID和名字的对应关系，提升了解析时间  
  2017-9-4 12:10:00 新增武器部分的build查询  
  2017-9-4 12:20:48 build查询有未知的MOD ID ，需要手动更新在对应的表里  
  2017-9-4 18:19:50 解决部分翻译问题 目盲 狂暴化等  
  2017-9-1 17:25:32 修复了trinity等战甲查询无效的问题  
  2017-9-1 17:25:28 限定了查询的结果，避免因为文本太长而无法被微信返回  
  2017-9-1 17:25:14 定时爬虫的结果直接写数据库，减少了请求耗时  

