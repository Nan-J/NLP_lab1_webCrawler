import requests
from bs4 import BeautifulSoup


def getHtmlText(url):
    try:
        kv = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/80.0.3987.163 Safari/537.36"}  # 修改头部信息，伪装成火狐访问
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()  # 如果状态不是200.则引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")
        return ""


def fillInList(reviews_all, html):
    num = 1
    soup = BeautifulSoup(html, "html.parser")  # 得到一个BeautifulSoup的对象(标准的缩进格式)
    # 获取评论元素-观察html发现评论内容div的class值为“lister-item-content”
    ct = soup.select('div[class="lister-item-content"]')
    # 遍历解析出的所有div，获取内容
    for i in range(len(ct)):
        # 获取评论标题
        title = ct[i].select('a[class="title"]')[0].get_text()
        # 获取评论正文
        review = ct[i].select('div[class="text show-more__control"]')[0].get_text()
        # 获取评论分数
        rate = ct[i].select('span[class="rating-other-user-rating"]')
        # 部分评论没有给分，因此需要判断是否存在打分。若存在，则获取rate值，否则rate=None
        if len(rate) < 1:
            rate = None
        else:
            rate = rate[0].select("span")[0].get_text()
        # 将获取的评论添加到reviews_all列表中
        reviews_all.append({"title": title, "review": review, "rate": rate})
    print("共获取了" + str(len(reviews_all)) + "条评论")
    # 结果写进review.txt
    file = open("reviews//reviews" + str(num) + ".txt", "a", encoding="utf8")
    for each in reviews_all:
        file.write(str(each))
    file.close()
    reviews_all.clear()
    # 如果页面没有load-more按钮，说明数据全部加载显示，退出循环
    while True:
        if len(soup.select(".load-more-data")) < 1:
            break
        # 获取paginationKey参数，用于发送请求更多数据
        paginationKey = soup.select(".load-more-data")[0].attrs["data-key"]
        html_new = getHtmlText(
            "https://www.imdb.com/title/tt0111161/reviews/_ajax?ref_=undefined&paginationKey=" + paginationKey)
        soup_new = BeautifulSoup(html_new, "html.parser")
        ct_new = soup_new.select('div[class="lister-item-content"]')
        for i in range(len(ct)):
            title_new = ct_new[i].select('a[class="title"]')[0].get_text()
            review_new = ct_new[i].select('div[class="text show-more__control"]')[0].get_text()
            rate_new = ct_new[i].select('span[class="rating-other-user-rating"]')
            if len(rate_new) < 1:
                rate_new = None
            else:
                rate_new = rate_new[0].select("span")[0].get_text()
            reviews_all.append({"title": title_new, "review": review_new, "rate": rate_new})
            print("共获取了" + str(len(reviews_all)) + "条评论")
            # 结果写进review.txt
            num = num + 1
            file = open("reviews//reviews" + str(num) + ".txt", "a", encoding="utf8")
            for each in reviews_all:
                file.write(str(each))
            file.close()
            reviews_all.clear()


if __name__ == "__main__":
    reviews_all = []  # 新建列表变量reviews_all,用于存放所有评论
    url = "https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv"
    html = getHtmlText(url)
    fillInList(reviews_all, html)
