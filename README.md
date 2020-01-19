# 示例
下载弹幕三步走
1. 先获取视频的aid(一个视频只有一个)
2. 然后获取cid(视频的每一p都有一个)
3. 从获取弹幕的接口进行下载


    url = "https://www.bilibili.com/video/av83611605"
    aid = get_aid(url)
    for array in get_cid(aid):
        cid = array['cid']
        download_comment_xml(cid, path=Path("comment"), name=f"{str(cid)}.xml")