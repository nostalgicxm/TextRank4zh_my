import pandas as pd
from textrank4zh import TextRank4Keyword, TextRank4Sentence

data = pd.read_csv('corpus.csv', encoding='gbk')

for text in data['content']:
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    print('KeyWords:')
    for item in tr4w.get_keywords(20, word_min_len=2):
        print(item.word)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')
    print('Summary:')
    for item in tr4s.get_key_sentences(num=3):
        print(item.sentence)  # index是语句在文本中位置，weight是权重