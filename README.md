# biliup_record

对bilibili的**up动态进行留档**，对动态自动分类标记保存到csv文件

使用**协程**下载动态中涉及的图片和视频封面

使用**httpx**模块，请自行pip install

目前比较**粗糙**，等待更新

## 使用

修改python源码中的**UID**

~~~shell
python UP动态留档.py
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

## Need to fix

- [ ] 转发动态的时间戳为0
- [ ] 转发动态的真实url 404（rid）
- [ ] markdown处理: pic_data有误