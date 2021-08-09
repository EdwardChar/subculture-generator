#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import time
import random
import argparse

import jieba
import newspaper
from newspaper import Config, Article


def get_articles(article_cnt) -> list:
    paper = newspaper.build("http://tech.sina.com.cn", language="zh")
    paragraphs = []
    config = Config()
    config.request_timeout = 3
    for article in paper.articles[:article_cnt]:
        try:
            good_article = Article(url=article.url.rstrip("\r\n").rstrip(" "), config=config, language='zh')
            good_article.download()
            good_article.parse()
            # good_article.nlp()
            if len(good_article.text):
                paragraphs.append(good_article.text)
        except Exception as err:
            print("Encountered exception. Automatically skips this article. {}".format(err))
        finally:
            time.sleep(0.1)
    return paragraphs


def generate(articles: list, words=2000, keywords=None, percentage=0.1):
    raw = "".join(articles)
    for c in ["\n", " ", "，", ",", "。"]:
        raw = raw.replace(c, "")
    lr = list(jieba.cut(raw))
    if len(lr) < words:
        print("words number too large")
        sys.exit()
    ln = random.choices(lr, k=words)
    keywords = keywords or ["马斯克", "马云", "扎克伯格", "马化腾", "比尔盖茨", "Facebook", "阿里巴巴", "贝索斯", "库克", "苹果", "小米", "华为", "5G"]

    random.shuffle(ln)
    cur = ""
    paragraphs = []
    length = len(ln)
    para_stops = [int(stop) for stop in [length * 0.1, length * 0.2, length * 0.4, length * 0.6, length * 0.9, length]]
    j = 0
    for i, word in enumerate(ln):
        r = random.random()

        if r < 0.02:
            cur += "。"
        elif r < 0.06:
            cur += "，"

        if r > 1.0 - percentage:
            cur += random.choice(keywords)
        else:
            cur += word

        if i == para_stops[j] - 1:
            j += 1
            if cur.endswith("，"):
                cur = cur[:-1] + '。'
            if not cur.endswith("。"):
                cur = cur + "。"
            paragraphs.append(cur)
            cur = ""
            continue

    paragraphs[0] = f"编者按：{paragraphs[0]}"
    paragraphs[-1] = f"结语：{paragraphs[-1]}"
    passa = "\n\n".join(paragraphs)
    return passa


def cult(words=2000, article_cnt=10, keywords=None, keyword_percentage=0.1):
    articles = get_articles(article_cnt)
    with open("subculture_revived.txt", "w", newline="", encoding="utf-8") as cult_file:
        cult_file.write(generate(articles, words=words, keywords=keywords))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Subculture generator: generate random shit
    example: python3 genertate.py -w 256 -p 0.1 -k 马斯克 马云 扎克伯格 马化腾""")
    parser.add_argument("-w", "--words", help="result word count", type=int, default=1000)
    parser.add_argument("-a", "--articles", help="source article count", type=int, default=10)
    parser.add_argument("-k", "--keywords", nargs='+', default=[], help="add some keywords")
    parser.add_argument("-p", "--keyword-percentage", type=float, default=0.1, help="keyword percentage")
    args = parser.parse_args()
    if args.keyword_percentage > 1 or args.keyword_percentage < 0:
        print("keyword parcentage must between 0 and 1")
        sys.exit()
    cult(args.words, article_cnt=args.articles, keywords=args.keywords, keyword_percentage=args.keyword_percentage)
