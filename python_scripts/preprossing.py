import pandas as pd
import jieba
import jieba.posseg as pseg
from stopwordsiso import stopwords
# import csv
import re
import json
from collections import Counter

# function: cut into words (tokenizer)
def tokenizerNoun(data):
    # cut into sentences
    temp = list()
    for i in data:
        temp.append(re.split('[。| \?| \!| \.](?!」)', str(i)))
     # run jieba and other preprocess for each sentences
    article = list()
    for i in range(len(temp)):
        sent = list()
        for j in range(len(temp[i])):
            words = list()
            for (w,f) in pseg.cut(temp[i][j]): # cut into words using jieba
                if (f in pos_list and # filter pos
                    w not in list(irrelavent_words.chinese) and # filter irrelavent_words
                    w not in f_stop_seg_list): # filter stop words
                    words.append(synonym_dict.get(w, w)) # process synonyms
            sent.append(words) # join words into a string
        print(f"{i + 1} of {len(temp)} is done!")
        article.append(sent)
    return article

# function: flatten and count words
def countItems(list):
    flatten = [item for sublist in list for subsublist in sublist for item in subsublist]
    count = Counter(flatten)
    return pd.DataFrame(count.items()).sort_values(1, ascending=False).reset_index(drop=True).rename(columns={0:"chinese", 1:"count"})

# load tw_data
tw_libertytimes = pd.read_csv("../data/taiwan/taiwan_raw/tw_libertytimes/tw_libertytimes_all.csv")
tw_chinatimes = pd.read_csv("../data/taiwan/taiwan_raw/tw_chinatimes/tw_chinatimes_all.csv")
tw_udn = pd.read_csv("../data/taiwan/taiwan_raw/tw_udn/tw_udn_all.csv")
tw_nextapple = pd.read_csv("../data/taiwan/taiwan_raw/tw_nextapple/tw_nextapple_all.csv")

# merge datasets into ideology groups
pro_china = pd.concat([tw_udn.reset_index(drop=True), tw_chinatimes.reset_index(drop=True)], axis = 0).reset_index()

# load dictionaries
pos_list = ["n", "s", "nr", "ns", "nz", "ns", "nt", "nw", "PER", "LOC", "ORG"]
## stopwords
f_stop_seg_list = stopwords(["zh"]) 
## custom words dictionary
jieba.load_userdict("../data/dictionaries/custom_words.txt")
## irrelavent words dictionary
irrelavent_words = pd.read_csv("../data/dictionaries/irrelavent_words.csv")
## synonym_dict
synonym_dict = json.load(open('../data/dictionaries/synonym_dict.json'))
## translated dict
translated = pd.read_csv("../data/taiwan/nouns/top1000/translated_top1000.csv")

# pro_china
pro_china_cut = tokenizerNoun(pro_china.content)
with open("../data/taiwan/taiwan_cut/pro_china_cut.json", "w") as f:
    json.dump(pro_china_cut, f, indent=2)
    f.close()

# pro_china = pd.concat([pro_china, pd.Series(pro_china_cut, name="cut")], axis=1)
pro_china_nouns = countItems(pro_china_cut)
pro_china_nouns.to_csv("../data/taiwan/nouns/pro_china_nouns.csv", encoding="utf-8-sig", index=False)
pd.merge(pro_china_nouns[:1000], translated, how="left", on="chinese").to_csv("../data/taiwan/nouns/top1000/pro_china_nouns_1000.csv", encoding="utf-8-sig", index=False)

# libertytimes
tw_libertytimes_cut = tokenizerNoun(tw_libertytimes.content)
with open("../data/taiwan/taiwan_cut/tw_libertytimes_bow.json", "w") as f:
    json.dump(tw_libertytimes_cut, f, indent=2)
    f.close()

tw_libertytimes = pd.concat([tw_libertytimes, pd.Series(tw_libertytimes_cut, name="cut")], axis=1)
tw_libertytimes_nouns = countItems(tw_libertytimes_cut)
tw_libertytimes_nouns.to_csv("../data/taiwan/nouns/tw_libertytimes_nouns.csv", encoding="utf-8-sig", index=False)
pd.merge(tw_libertytimes_nouns[:1000], translated, how="left", on="chinese").to_csv("../data/taiwan/nouns/top1000/tw_libertytimes_nouns_1000.csv", encoding="utf-8-sig", index=False)

# nextapple
tw_nextapple_cut = tokenizerNoun(tw_nextapple.content)
with open("../data/taiwan/taiwan_cut/tw_nextapple_bow.json", "w") as f:
    json.dump(tw_nextapple_cut, f, indent=2)
    f.close()

tw_nextapple = pd.concat([tw_nextapple, pd.Series(tw_nextapple_cut, name="cut")], axis=1)
# tw_nextapple.to_csv("../data/tw_nextapple2.csv", encoding="utf-8-sig", index=False)
tw_nextapple_nouns = countItems(tw_nextapple_cut)
tw_nextapple_nouns.to_csv("../data/taiwan/nouns/tw_nextapple_nouns.csv", encoding="utf-8-sig", index=False)
tw_nextapple_nouns = pd.read_csv("../data/taiwan/nouns/tw_nextapple_nouns.csv")
pd.merge(tw_nextapple_nouns[:1000], translated, how="left", on="chinese").to_csv("../data/taiwan/nouns/top1000/tw_nextapple_nouns_1000.csv", encoding="utf-8-sig", index=False)


############################################################
####################### Synonyms ###########################
############################################################

# Load tokenized data
# with open("../data/taiwan/taiwan_cut/pro_china_bow.json", "r") as f:
#     pro_china = json.load(f)
#     f.close
# 
# 
# pro_china = [[[synonym_dict.get(word, word) for word in sentence] for sentence in article] for article in pro_china]
# pro_china_nouns = countItems(pro_china)
# pro_china_nouns.to_csv("../data/taiwan/nouns/pro_china_nouns_syn.csv", encoding="utf-8-sig", index=False)
# 
# pro_china_nouns_1000_translated = pd.merge(pro_china_nouns[:1000], translate, how="left", on="chinese")
# pro_china_nouns_1000_translated.to_csv("../data/taiwan/nouns/top1000/pro_china_nouns_1000.csv", encoding="utf-8-sig", index=False)
