import os
import re
from pathlib import Path
from typing import Dict, List, Union

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}


def download_file(url: str, path: Union[Path, str], name: str) -> Path:
    """下载文件

    :param url: 文件的url
    :param path: 保存的路径
    :param name: 文件名
    :return: 成功保存后的路径
    """
    p = Path(path) / name
    if p.exists():
        print('该文件已存在')
        return p
    try:
        r = requests.get(url)
        if not Path(path).exists():
            os.makedirs(path)
        with open(p, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.ConnectionError:
        raise KeyError('文件下载失败')
    return p


def get_aid(url: str) -> int:
    """获取视频aid

    :param url: 视频url
    :return:
    """
    endpoint = url.split("/")[-1]
    if endpoint.startswith("ep"):
        aid = _get_aid_ep(url)
    elif endpoint.startswith("ss"):
        aid = _get_aid_ss(url)
    elif endpoint.startswith("av"):
        aid = _get_aid_av(url)
    else:
        raise KeyError("没有找到aid")
    return aid


def _get_aid_ss(url: str) -> int:
    """获取视频码类似 "https://www.bilibili.com/bangumi/play/ss427" 这样的aid

    :param url: 视频url
    :return: 返回aid
    """
    r = requests.get(url, headers=headers)
    aid = re.findall(r'"aid":(\d+)', r.text)[1]  # 在没有登录的情况下第一个值为0，默认取第二个值，不知道会不会有bug
    return int(aid)


def _get_aid_ep(url: str) -> int:
    """

    :param url: 视频url
    :return: 返回aid
    """
    r = requests.get(url, headers=headers)
    aid = re.findall(r'AV(\d+)', r.text)[0]
    return int(aid)


def _get_aid_av(url: str) -> int:
    """

    :param url: 视频url
    :return: 返回aid
    """
    return re.findall(r"av(\d+)", url)[0]


def get_cid(aid: int) -> List[Dict]:
    """获取cid

    :param aid: 每一个视频的分p都有一个不同的cid
    :return: 返回[{"page":1,"pagename":"BLACKDRAGON","cid":143033371}] 这样的数组
    """
    url = "https://www.bilibili.com/widget/getPageList"
    params = {
        "aid": aid
    }
    r = requests.get(url, headers=headers, params=params).json()
    return r


def download_comment_xml(cid: int, path: Union[Path, str], name: str) -> Path:
    """下载弹幕文件

    :param cid: 视频的cid
    :param path: 保存的路径
    :param name: 弹幕的文件名
    :return: 保存的路径
    """
    url = f"https://comment.bilibili.com/{cid}.xml"
    p = download_file(url, path, name)
    return p


def main():
    url = "https://www.bilibili.com/video/av83611605"
    aid = get_aid(url)
    for array in get_cid(aid):
        cid = array['cid']
        download_comment_xml(cid, path=Path("comment"), name=f"{str(cid)}.xml")


if __name__ == '__main__':
    main()
