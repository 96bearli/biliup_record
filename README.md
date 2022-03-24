# biliup_record

对bilibili的**up动态进行留档**，对动态自动分类标记保存到csv文件

使用**协程**下载动态中涉及的图片和视频封面

使用**httpx**模块，请自行pip install

目前比较**粗糙**，等待更新

## 使用

修改python源码中的**UID**

~~~shell
python UP动态留档.py
# 等待完成后数据存放在./data/UID/
python UP动态数据处理.py
# ./data/UID/data.md
~~~

## Future

* ~~进行数据处理，**markdown**格式整理动态和图片~~(Done)
* 放弃CSV的数据储存方式
* 美化代码，优化逻辑
* 修复BUG

## Update

|Time|Content|
|----|----|
|2022-3-23|协程爬虫主程序|
|2022-3-24|.md生成主程序|
|2022-3-24|修复.md处理BUG|
|2022-3-24|Fix type & More strong|
|2022-3-24|常用的动态转发已修复|
## Need to fix

- [x] 新card_type：audio(au)
- [x] markdown处理: pic_data有空数据无法识别
- [x] markdown处理: pic_data识别成功的多一'
- [x] ~~Type:text 真实url 404（rid）~~
- [x] Type:reprint 时间戳为0
- [x] Type:reprint 真实url 404（rid）
- [x] Type:reprint_2 转发动态无法识别
- [ ] Type:reprint_3 转发cv无法正确识别
- [ ] Type:reprint_4 转发音频无法正确识别-猜测
- [ ] Type:reprint_5 转发装扮无法正确识别-猜测

 