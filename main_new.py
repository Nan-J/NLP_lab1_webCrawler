import requests
from bs4 import BeautifulSoup


def getHtmlText(url):
    try:
        kv = {'user-agent': "Mozilla/5.0"}  # 修改头部信息，伪装成火狐访问
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()  # 如果状态不是200.则引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text

    except:
        print("爬取失败")
        return ""


def fillInList(reviews, html):
    def analisis(soup):
        ct_new = soup.select('div[class="lister-item-content"]')
        for i in range(len(ct_new)):
            title_new = ct_new[i].select('a[class="title"]')[0].get_text()
            review_new = ct_new[i].select('div[class="text show-more__control"]')[0].get_text()
            rate_new = ct_new[i].select('span[class="rating-other-user-rating"]')
            if len(rate_new) < 1:
                rate_new = None
            else:
                rate_new = rate_new[0].select("span")[0].get_text()
            reviews.append({"title": title_new, "review": review_new, "rate": rate_new})
            print("新获取了" + str(len(reviews)) + "条评论")
            return reviews

    soup = BeautifulSoup(html, "html.parser")  # 得到一个BeautifulSoup的对象(标准的缩进格式)
    reviews1 = analisis(soup)
    # 结果写进review.txt
    num = 1
    file = open("reviews//reviews" + str(num) + ".txt", "a", encoding="utf8")
    for each in reviews1:
        file.write(str(each))
    file.close()
    reviews.clear()

    # 如果页面没有load-more按钮，说明数据全部加载显示，退出循环
    while True:
        if len(soup.select(".load-more-data")) < 1:
            break
        # 获取paginationKey参数，用于发送请求更多数据
        paginationKey = soup.select(".load-more-data")[0].attrs["data-key"]
        html_new = getHtmlText(
            "https://www.imdb.com/title/tt0111161/reviews/_ajax?ref_=undefined&paginationKey=" + paginationKey)
        soup_new = BeautifulSoup(html_new, "html.parser")
        reviews_new = analisis(soup_new)
        # 结果写进review.txt
        num = num + 1
        file = open("reviews//reviews" + str(num) + ".txt", "a", encoding="utf8")
        for each in reviews_new:
            file.write(str(each))
        file.close()
        reviews_new.clear()


if __name__ == "__main__":
    print("开始爬虫")
    reviews = []  # 新建列表变量reviews_all,用于存放所有评论
    url = "https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv"
    html = getHtmlText(url)
    print("访问成功！开始解析页面")
    fillInList(reviews, html)
