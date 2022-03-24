# -*- coding = utf-8 -*-
# @Python : 3.8
import re
import time


def get_data(base_path):
    with open(base_path + "data.csv", "r", encoding="utf-8-sig") as f:
        lines = [l.replace("\n", "").split(",") for l in f.readlines()]
    return lines


def time_md(_time: str):
    if len(_time) > 10:
        timeStamp = int(int(_time)/1000)
    else:
        timeStamp = int(_time)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("## %Y年%m月%d日 %H:%M:%S", timeArray)
    # ## 2020年11月23日 20:16:20
    # print(otherStyleTime)
    return otherStyleTime


def title_md(_time: str, type) -> str:
    return f"{_time} Type:{type}\n"


def pic_md(pic_str: str) -> str:
    pics = pic_str.replace("'","").replace("[","").replace("]","").split("&")
    print(pics)
    if len(pics) == 0:
        return None
    text = ""
    for pic in pics:
        name = pic.split("/")[-1]
        if "?" in name:
            name = name.split("?")[0]
        if name == "":
            continue
        text += f"![{name}]({img_path + name}) "
    return text


def content_md(text, pic_content) -> str:
    return f"{text}\n{pic_content}\n"


def id_url_md(id, type) -> str:
    if type == "img" or type == "text" or type == "decorate" or type == "reprint":
        url = f"https://t.bilibili.com/{id}"
        text = f"[点击直达动态]({url})"
    elif type == 'av':
        url = f"https://b23.tv/av{id}"
        text = f"[点击直达视频]({url})"
    elif type == "cv":
        url = f"https://www.bilibili.com/read/cv{id}"
        text = f"[点击直达专栏]({url})"
    elif type == "au":
        url = f"https://www.bilibili.com/audio/au{id}"
        text = f"[点击直达音乐]({url})"
    else:
        print(type, "   ", id)
        exit()
    return text + "\n"


if __name__ == '__main__':
    UID = 4
    base_path = f"./data/{UID}/"
    img_path = "./img/"
    md_path = base_path + "data.md"
    with open(md_path, "w", encoding="utf8") as f:
        f.write(f"# UID:{UID} 动态留档\n动态页面：[点此直达](https://space.bilibili.com/{UID}/dynamic)\n")
    datas = get_data(base_path)
    for data in datas:
        print(data)
        time_ = time_md(data[0])
        title = title_md(time_, data[4])
        print(title)
        pic_data = pic_md(data[2])

        content = data[1].replace("\\n", "\n") + "\n"
        find_tag = re.compile("#.+?#")
        tags = re.findall(find_tag, content)
        for tag in tags:
            content = content.replace(tag, f'Tag:{tag.replace("#", "")} ')

        if pic_data is None:
            content = content
        else:
            content = content_md(content, pic_data)

        click_url = id_url_md(data[3], data[4])
        print(click_url)
        print(content)
        with open(md_path, "a+", encoding="utf8") as f:
            f.write(title)
            f.write(click_url)
            f.write(content)
