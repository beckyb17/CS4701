import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

df = pd.read_csv('final_taylor_swift_lyrics.tsv', sep='\t')

df_dict = df.to_dict(orient = 'records')

#song to index maps song titles to their index
#index dic maps song index to a list of its lyrics

song_to_index = {}
index_dic = {}
for i in df_dict:
  index = i['index']
  lyric = i['lyric']
  if index in index_dic:
      index_dic[index].append(lyric)
  else:
      index_dic[index] = [lyric]
      title = i['song_title'].lower()
      song_to_index[title] = index 

num_songs = len(song_to_index)

vectorizer = TfidfVectorizer(stop_words = 'english', min_df = 2)

#code from 4300 class demo
word_splitter = re.compile(r"""
  (\w+)
  """, re.VERBOSE)

def getwords(lyric):
  return [w.lower() for w in word_splitter.findall(lyric)]

lyrics_list = []
for i in index_dic:
  lyric = index_dic[i]
  lyric_str = ""
  for l in lyric:
      l.lower()
      lyric_str += " "
      lyric_str += l
  all_words = getwords(lyric_str)
  lyrics_list.append(" ".join(all_words))

tfidf_vec = vectorizer.fit_transform(lyrics_list).toarray()

cos_sim = np.zeros((num_songs,num_songs))
i = 0
while i < num_songs:
  j = 0
  while j < num_songs:
    song1 = tfidf_vec[i]
    song2 = tfidf_vec[j]
    song1_norm = np.linalg.norm(tfidf_vec[i])
    song2_norm = np.linalg.norm(tfidf_vec[j])
    numerator = np.dot(song1, song2)
    denominator = song1_norm * song2_norm
    cosine_similarity = numerator/denominator
    cos_sim[i][j] = cosine_similarity
    j += 1
  i += 1

np.save('cosine_matrix', cos_sim)


