from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv

# function: generate wordcloud
def genWordcloud(data, name):
    font_path = "/System/Library/Fonts/PingFang.ttc"
    wc = WordCloud(font_path=font_path, background_color="white", max_words=1000,
               max_font_size=200, random_state=42, 
               width=1000, height=860, margin=2,)
    wc.generate_from_frequencies(data)
    wc.to_file(f"../figures/wc_{name}.png")
    return

# function: CSV to Dict
def csvDict(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        dict = {}
        for k,v in reader:
            dict[k] = int(v)
    return dict

# load data
pro_china_freq = csvDict("../data/taiwan/nouns/top1000/translated/pro_china_nouns_1000_translated.csv")
tw_libertytimes_freq = csvDict("../data/taiwan/nouns/tw_libertytimes_nouns_1000_translated.csv")
tw_nextapple_freq = csvDict("../data/taiwan/nouns/tw_nextapple_nouns_1000_translated.csv")

genWordcloud(pro_china_freq, "pro_china")
genWordcloud(tw_libertytimes_freq, "tw_libertytimes")
genWordcloud(tw_nextapple_freq, "tw_nextapple")
