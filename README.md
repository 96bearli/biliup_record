# biliup_record

**warn**: 20240322发现历史动态接口`api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history`已部分功能失效,本程序故障,待作者有时间进行修复和重构

对bilibili的**up动态进行留档**，对动态自动分类标记保存到csv文件

处理得到的数据，整理得到有一定格式的markdown文件

使用**协程**下载动态中涉及的图片和视频封面

使用**httpx**模块，请自行pip install

目前能将就用了，有些小BUG，代码还是很乱
**偶然发现本脚本使用的接口对已注销用户同样生效**
## 使用
### 获取数据
file  **main_get.py**
```shell
# 两个参数
# parm1 uids：一个用英文','隔开的字符串（无空格）
# parm2 是否下载图片：1或0（不输入第二项参数默认不下载）
python main_get.py <",".join(uids)> <download_img?>
# 两个示例
# uids:[1111,22222,333333] download_img?:False
python main_get.py 1111,22222,333333 0   #
# uids:[1111] download_img?:False
python main_get.py 1111
# out: ./data/1111
```
### 处理数据
file  **main_data.py**
~~~shell
# 参数 单个UID
python main_data.py <UID>
# 示例 整理./data/1111内的数据
python main_data.py 1111
# out: ./data/1111/data.md

# 如果有pandoc可以把markdown文件转为html
# 脚本根目录，下面命令三选一
bash ./2html.sh <UID> # linux下
.\2html.cmd <UID> # windows下
pandoc -f markdown -t html -o data/<UID>/index.html data/<UID>/data.md # All
~~~

## Future

* ~~进行数据处理，**markdown**格式整理动态和图片~~ (Done)
* 使用json存放参数
* ~~sys指定参数（uid~~ (Done)
* 放弃CSV的数据储存方式
* 美化代码，优化逻辑
* 修复BUG
* 检测img文件夹，如果图片存在不会重新下载
* 指定动态类型
* 指定关键词
* 代码重构2.0
* 数据分析、信息挖掘模式

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
|2022-3-25|改变两个主程序参数获取方式|
|2022-3-25|完善生成的.md格式|
|2022-3-26|修复转发带图动态内容（默认不下动态图）|
|2022-3-26|pandoc md2html cmd|
|2022-4-11|loguru 记录日志|


## Need to fix

- [x] 新card_type：audio(au)
- [x] markdown处理: pic_data有空数据无法识别
- [x] markdown处理: pic_data识别成功的多一'
- [x] ~~Type:text 真实url 404（rid）~~
- [x] Type:reprint 时间戳为0
- [x] Type:reprint 真实url 404（rid）
- [x] Type:reprint_2 转发文字动态无法识别
- [ ] Type:reprint_3 转发cv无法正确识别
- [ ] Type:reprint_4 转发音频无法正确识别-猜测
- [ ] Type:reprint_5 转发装扮无法正确识别-猜测
- [ ] Type:reprint_6 转发带图动态无法获得时间戳

## 欢迎参与本项目
如何参与
1. Fork 本仓库
2. clone fork的仓库
3. new branch
4. git push
5. Pull Request
