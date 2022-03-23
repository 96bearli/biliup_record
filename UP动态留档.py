# -*- coding = utf-8 -*-
# @Python : 3.8
import time
import httpx
import os
import asyncio
import json

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
        print(f"* 问题url:{url}")
        return 0
    print(f"downloading {name}")
    if "?" in name:
        name = name.split("?")[0]
    try:
        async with httpx.AsyncClient(headers=headers, cookies=cookies, timeout=20) as client:
            req = await client.get(url)
    except Exception as e:
        print(e)
        print(f"* Error:Download_failed:{url}")
        return 0
    save_img(paths[1], name, req.content)


def get_content(s, url: str):
    data = s.get(url).json()
    offset = data['data']['next_offset']
    more = data['data']['has_more']
    return data, offset, more


async def main(uid):
    more = 1
    count = 1
    offset = 0
    # offset = 634424114892767289
    s = httpx.Client(headers=headers)
    while more == 1:
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=283764718&host_uid={uid}&offset_dynamic_id={offset}&need_top=1&platform=web'
        print(f"第{count}页动态爬取中:{url}")
        count += 1
        tasks = []
        data_json, offset, more = get_content(s, url=url)
        if more == 0:
            break
        for dict_da in data_json['data']['cards']:

            key = dict_da['card'].split('"')[1]
            dict_data = json.loads(dict_da['card'])
            # print(dict_data)
            save_data(paths[0] + "data.txt", dict_data)
            if key == "item":  # 图片动态
                upload_time = dict_data['item']['upload_time']  # int
                content = dict_data['item']['description'].replace("\n", "\\n").replace(",", "，")  # str
                pic_urls = [d["img_src"] for d in dict_data['item']['pictures']]  # list
                # id_ = dict_data['item']['id']  # int
                id_ = data_json['data']['cards'][data_json['data']['cards'].index(dict_da)]['desc']["dynamic_id"]  # int
                other = "img"
            elif key == "user":  # 文字动态 or 转发
                try:
                    origin = json.loads(dict_data["origin"])
                    upload_time = dict_data['item']['timestamp']  # int
                    try:
                        content = f"{dict_data['item']['content']},转发视频av{origin['aid']}".replace("\n", "\\n").replace(
                            ",", "，")  # str
                    except KeyError:
                        content = f"{dict_data['item']['content']},{origin['item']['rp_id']}".replace("\n",
                                                                                                      "\\n").replace(
                            ",", "，")  # str
                    pic_urls = []  # list
                    id_ = dict_data['item']['rp_id']  # int
                    other = "reprint"
                except KeyError as e:
                    upload_time = dict_data['item']['timestamp']  # int
                    content = dict_data['item']['content'].replace("\n", "\\n").replace(",", "，")  # str
                    pic_urls = []  # list
                    id_ = dict_data['item']['rp_id']  # int
                    other = "text"
            elif key == "aid":  # 视频投稿
                upload_time = dict_data['pubdate']  # int
                content = dict_data['dynamic'].replace("\n", "\\n").replace(",", "，")  # str
                pic_urls = [dict_data["pic"]]  # list
                id_ = dict_data['aid']  # int
                other = "av"
            elif key == "id":  # 专栏投稿
                upload_time = dict_data['publish_time']  # int
                content = dict_data['title'].replace("\n", "\\n").replace(",", "，")  # str
                pic_urls = [dict_data["banner_url"]]  # list
                id_ = dict_data['id']  # int
                other = "cv"
            elif key == "rid":
                upload_time = 0  # int
                content = dict_data['vest']['content'].replace("\n", "\\n").replace(",", "，")  # str
                pic_urls = []  # list
                id_ = dict_data['rid']  # int
                other = "decorate"
            else:
                print("     * 注意本条数据 *")
                print(dict_data)
                print(url)
                time.sleep(5)
                continue
            # print(f"{upload_time},{content},{pic_urls},{id_},{other}")  # exit()
            for p_u in pic_urls:
                if p_u == "":
                    pic_urls.remove(p_u)
            save_data(paths[0] + "data.csv", f"{upload_time},{content},{pic_urls},{id_},{other}", encoding="utf-8-sig")
            for p_u in pic_urls:
                tasks.append(download(p_u))
        result = await asyncio.gather(*tasks)


if __name__ == '__main__':
    uids = [672328094]
    path_creat("./data")
    # 时间戳转换 Fx = "=(A1+8*3600)/86400+70*365+19"
    for uid in uids:
        print(f"正在进行准备工作,当前目标UID:{uid}")
        paths = [f"./data/{uid}/", f"./data/{uid}/img/"]
        for p in paths:
            path_creat(p)
        for i in ["data.txt", "data.csv"]:
            with open(paths[0] + i, "w", encoding="utf-8")as f:
                pass
        asyncio.run(main(uid=uid))
