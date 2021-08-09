import jieba
import newspaper
import random
import time
from newspaper import Config, Article


def cult():
    # crawl 200 articles
    paper = newspaper.build("http://tech.sina.com.cn", language="zh")
    paragraph = []
    config = Config()
    config.request_timeout = 3
    for article in paper.articles[:50]:
        try:
            good_article = Article(url=article.url.rstrip("\r\n").rstrip(" "), config=config, language='zh')
            good_article.download()
            good_article.parse()
            if len(good_article.text):
                paragraph.extend(good_article.text)
        except Exception as err:
            print("Encountered exception. Automatically skips this article. {}".format(err))
        finally:
            time.sleep(0.1)
    raw = "".join(paragraph)
    lr = list(jieba.cut(raw))
    ln = random.choices(lr, k=2000)
    # add names to make it funnier
    ln.extend(["马斯克", "马云", "扎克伯格", "马化腾", "比尔盖茨", "Facebook", "阿里巴巴", "贝索斯", "库克", "苹果", "小米", "华为", "5G"])
    random.shuffle(ln)
    naw = ""
    for i, word in enumerate(ln):
        r = random.random()

        if r < 0.02:
            naw += "。|"
        elif r < 0.06:
            naw += "，"
        naw += word
    if not naw.endswith("。|"):
        naw += "。"
    sent = naw.split("|")
    abstract = "编者按："
    pg1 = ""
    pg2 = ""
    pg3 = ""
    concl = "结语："
    # create "abstract"
    for i in range(5):
        abstract += sent.pop()
    abstract += "\n\n"

    for i in range(3):
        concl += sent.pop()
    concl += "\n"
    perp = len(sent) // 4 + 1
    for i in range(perp):
        pg1 += sent.pop()
        pg2 += sent.pop()
        pg3 += sent.pop()
    pg1 += "\n\n"
    pg2 += "\n\n"
    pg3 += "\n\n"
    pg4 = "".join(sent) + "\n\n"
    passage = abstract + pg1 + pg2 + pg3 + pg4 + concl
    return passage


with open("subculture_revived.txt", "w", newline="", encoding="utf-8") as cult_file:
    cult_file.write(cult())
