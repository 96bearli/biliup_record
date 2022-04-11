# -*- coding = utf-8 -*-
# @Python : 3.8
import asyncio
import json
import os
import sys
import time

import httpx
from loguru import logger

headers = {"accept-encoding": "gzip",  # gzip压缩编码  能提高传输文件速率
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46', }
cookies = {}


#  创建文件夹
def path_creat(_path):
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path


def save_data(path, data, encoding="utf-8"):
    with open(path, "a+", encoding=encoding) as f:
        f.write(f"{data}\n")


def save_img(path, name, data):
    with open(path + name, "wb") as f:
        f.write(data)


async def download(url: str):
    name = url.split("/")[-1]
    if name == '':
        logger.error(f"* 问题url:{url}")
        return 0
    logger.info(f"downloading {name}")
    if "?" in name:
        name = name.split("?")[0]
    try:
        async with httpx.AsyncClient(headers=headers, cookies=cookies, timeout=10) as client:
            req = await client.get(url)
    except Exception as e:
        # print(e)
        logger.error(f"* Error:Download_failed:{url},check file'{paths[1] + 'Img_failed.txt'}")
        with open(paths[1] + "Img_failed.txt", "a+", encoding="utf-8") as f:
            f.write(f"{url}\n")
        return 0
    save_img(paths[1], name, req.content)
    return True


def get_content(s, url: str):
    data = s.get(url).json()
    offset = data['data']['next_offset']
    more = data['data']['has_more']
    return data, offset, more


async def main(uid, d_img: bool):
    more = 1
    count = 1
    offset = 0
    # offset = 634424114892767289
    s = httpx.Client(headers=headers, cookies=cookies)
    while more == 1:
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=283764718&host_uid={uid}&offset_dynamic_id={offset}&need_top=1&platform=web'
        logger.info(f"第{count}页动态爬取中:{url}")
        count += 1
        tasks = []
        try:
            data_json, offset, more = get_content(s, url=url)
        except Exception as e:
            # logger.error(f"{e}")
            logger.info("* 网络请求错误，5秒后重试一次")
            time.sleep(5)
            data_json, offset, more = get_content(s, url=url)
        # print(data_json)
        # exit()
        if more == 0:
            break
        for dict_da in data_json['data']['cards']:

            key = dict_da['card'].split('"')[1]
            dict_data = json.loads(dict_da['card'])
            # print(dict_data)
            save_data(paths[0] + "data.txt", dict_data)
            num = data_json['data']['cards'].index(dict_da)
            if key == "item":  # 图片动态
                upload_time = dict_data['item']['upload_time']  # int
                content = dict_data['item']['description'].replace("\n", "\\n").replace("\r", "").replace(",",
                                                                                                          "，").replace(
                    "'", "‘").replace('"', '”')  # str
                pic_urls = [d["img_src"] for d in dict_data['item']['pictures']]  # list
                # id_ = dict_data['item']['id']  # int
                id_ = data_json['data']['cards'][num]['desc']["dynamic_id"]  # int
                other = "img"
            elif key == "user":  # 文字动态 or 转发 /data/cards/0/desc/dynamic_id
                try:
                    origin = json.loads(dict_data["origin"])
                    try:  # 转发动态
                        upload_time = data_json['data']['cards']['item']['timestamp']
                    except Exception:  # 转发av
                        # logger.warning(f"{Exception}")
                        upload_time = data_json['data']['cards'][num]['desc'][
                            "timestamp"]  # int /data/cards/0/desc/timestamp
                    # if upload_time == 0:
                    #     upload_time = data_json['data']['cards']['item']['timestamp']
                    try:
                        content = f"评论：{dict_data['item']['content']}\n\r转发视频[{origin['title']}](https://b23.tv/av{origin['aid']})".replace(
                            "\r", "").replace("\n", "\\n").replace(",", "，").replace("'", "‘").replace('"', '”')  # str
                        pic_urls = []  # list
                    except KeyError:  # /item/orig_dy_id /item/description
                        # print(KeyError)
                        try:
                            content = f"评论：{dict_data['item']['content']}\n\r转发动态[{dict_data['origin_user']['info']['uname']} UID:{dict_data['origin_user']['info']['uid']}动态](https://t.bilibili.com/{dict_data['item']['orig_dy_id']})\n\r内容：{origin['item']['content']}".replace(
                                "\r", "").replace("\n", "\\n").replace(",", "，").replace("'", "‘").replace('"', '”')  # str
                            pic_urls = []  # list
                        except:
                            content = f"评论：{dict_data['item']['content']}\n\r转发带图动态[{dict_data['origin_user']['info']['uname']} UID:{dict_data['origin_user']['info']['uid']}动态](https://t.bilibili.com/{dict_data['item']['orig_dy_id']})\n\r内容：{origin['item']['description']}".replace(
                                "\r", "").replace("\n", "\\n").replace(",", "，").replace("'", "‘").replace('"', '”')  # str
                            pic_urls = []  # 转发带图动态的图就不下了，太多了
                            # pic_urls = [imd["img_src"] for imd in origin['item']['pictures']]  # list /item/pictures/0/img_src


                    id_ = data_json['data']['cards'][num]['desc']["dynamic_id"]  # int
                    other = "reprint"
                except Exception as e:
                    # logger.warning(f"{e}")
                    upload_time = dict_data['item']['timestamp']  # int /item/upload_time
                    content = dict_data['item']['content'].replace("\n", "\\n").replace("\r", "").replace(",",
                                                                                                          "，").replace(
                        "'", "‘").replace('"', '”')  # str
                    pic_urls = []  # list
                    id_ = data_json['data']['cards'][num]['desc']["dynamic_id"]  # int
                    other = "text"
            elif key == "aid":  # 视频投稿
                upload_time = dict_data['pubdate']  # int
                content = dict_data['dynamic'].replace("\n", "\\n").replace("\r", "").replace(",", "，").replace("'",
                                                                                                                "‘").replace(
                    '"', '”')  # str
                pic_urls = [dict_data["pic"]]  # list
                id_ = dict_data['aid']  # int
                other = "av"
            elif key == "id":  # 专栏投稿
                try:
                    upload_time = dict_data['publish_time']  # int
                    content = dict_data['title'].replace("\n", "\\n").replace("\r", "").replace(",", "，").replace("'",
                                                                                                                  "‘").replace(
                        '"', '”')  # str
                    pic_urls = [dict_data["banner_url"]]  # list
                    id_ = dict_data['id']  # int
                    other = "cv"
                except:
                    upload_time = dict_data['ctime']  # int
                    content = (dict_data['title'] + "\n" + dict_data['intro']).replace("\r", "").replace("\n",
                                                                                                         "\\n").replace(
                        ",", "，").replace("'", "‘").replace('"', '”')  # str
                    pic_urls = [dict_data["cover"]]  # list
                    id_ = dict_data['id']  # int
                    other = "au"
            elif key == "rid":
                upload_time = 0  # int
                content = dict_data['vest']['content'].replace("\n", "\\n").replace("\r", "").replace(",", "，").replace(
                    "'", "‘").replace('"', '”')  # str
                pic_urls = []  # list
                id_ = dict_data['rid']  # int
                other = "decorate"
            else:
                logger.debug("     * 注意本条数据 *")
                logger.debug(dict_data)
                logger.debug(url)
                time.sleep(5)
                continue
            # print(f"{upload_time},{content},{pic_urls},{id_},{other}")  # exit()
            for p_u in pic_urls:
                if p_u == "":
                    pic_urls.remove(p_u)
            save_data(paths[0] + "data.csv", f"{upload_time},{content},{'&'.join(pic_urls)},{id_},{other}",
                      encoding="utf-8-sig")
            for p_u in pic_urls:
                tasks.append(download(p_u))
        if d_img:
            result = await asyncio.gather(*tasks)


if __name__ == '__main__':
    # 目标uids
    uids = [351609538]
    # 是否下载图片
    img = False
    path_creat("./data")
    logger.add(sink=f"./data/log_get_{int(time.time())}.log", format="{level} - {time} - {message}", level="DEBUG",encoding="utf-8")
    logger.info("日志记录开始")
    if len(sys.argv) != 1:
        uids = [uid for uid in sys.argv[1].split(",")]
        if len(sys.argv) == 3:
            img = bool(int(sys.argv[-1]))
        else:
            img = False
        logger.success(f"* 已获取参数参数 <目标UID：{uids},下载图片：{img}>")
    else:
        logger.success(f"* 使用内置参数 <目标UID：{uids},下载图片：{img}>")
        print('''* Usage: python main_get.py <",".join(uids)> <download_img?>
example1: python main_get.py 1111,22222,333333 0   #uids:[1111,22222,333333] download_img?:False
example2: python main_get.py 1111   #uids:[1111] download_img?:False''')
    path_creat("./data")
    time.sleep(1.5)
    # 时间戳转换 Fx = "=(A1+8*3600)/86400+70*365+19"
    for uid in uids:
        logger.info(f"* 正在进行准备工作,当前目标UID:{uid}")
        paths = [f"./data/{uid}/", f"./data/{uid}/img/"]
        for p in paths:
            path_creat(p)
        for i in ["data.txt", "data.csv"]:
            with open(paths[0] + i, "w", encoding="utf-8")as f:
                pass

        asyncio.run(main(uid=uid, d_img=img))
        logger.success(f"* 目标UID:{uid}已完成爬取\n")
        time.sleep(1.5)
