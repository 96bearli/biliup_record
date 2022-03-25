# biliup_record

对bilibili的**up动态进行留档**，对动态自动分类标记保存到csv文件

使用**协程**下载动态中涉及的图片和视频封面

使用**httpx**模块，请自行pip install

目前比较**粗糙**，等待更新

## 使用
### 获取数据
file  main_get.py
```shell
# 两个参数
# uids：一个用英文','隔开的数字串（无空格）
# 是否下载图片：1或0（不输入第二项参数默认不下载）
python main_get.py <",".join(uids)> <download_img?>
# 两个实例
# uids:[1111,22222,333333] download_img?:False
python main_get.py 1111,22222,333333 0   #
# uids:[1111] download_img?:False
python main_get.py 1111
```
### 处理数据
~~~shell
python main_get.py
# 等待完成后数据存放在./data/UID/
python main_data.py
# ./data/UID/data.md

# 如果有pandoc可以把markdown文件转为html
bash ./2html.sh UID # linux下
~~~

## Future

* ~~进行数据处理，**markdown**格式整理动态和图片~~(Done)
* 使用json存放参数
* sys指定参数（uid）
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
|2022-3-24|修改文件名|
|2022-3-25|pandoc md2html shell|

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

 