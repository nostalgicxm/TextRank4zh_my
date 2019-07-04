import pandas as pd
import numpy as np
import jieba
import jieba.analyse
import re
import json

def getThose(s):
    sentences = re.split(sentence_p, s)
    keywords = jieba.analyse.tfidf(s, topK =100)
    isin = np.zeros((100, len(sentences)))

    for index_s, s in enumerate(sentences):
        seg = list(jieba.cut(s))
        for index_w, w in enumerate(keywords):
            if w in seg:
                isin[index_w][index_s] = 1
    result = []
    for i in range(5):
        count = np.sum(isin,axis=0)
        arg = np.argmax(count)
        result.append(arg)
        mask = 1-isin[:,arg]
        mask = np.repeat(mask,len(sentences)).reshape((-1,len(sentences)))
        isin = np.multiply(isin,mask)
    for i in range(5):
        result[i] = sentences[result[i]]
    return keywords, result

sentence_p = '。|！|\!|\.|？|\?'
data = pd.read_csv('corpus.csv', encoding='gbk')
with open('result.txt', 'a', encoding='utf-8') as f:
    x = 0
    for s in data['content']:
        keywords, result = getThose(s)
        print(keywords)
        summary = ''
        for i in result:
            summary = summary + '  ' + i
        items = {'索引': x, '关键字': keywords, '摘要': summary}
        f.write(json.dumps(items, ensure_ascii=False)+'\n')
        x = x + 1

