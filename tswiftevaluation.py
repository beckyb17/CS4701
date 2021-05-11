import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import PorterStemmer
import random

#original code from cosinesim.py edited to add stemming
def stemming():
  df = pd.read_csv('final_taylor_swift_lyrics.tsv', sep='\t')

  df_dict = df.to_dict(orient = 'records')

  #song to index maps song titles to their index
  #index dic maps song index to a list of its lyrics
  song_to_index = {}
  index_dic = {}
  current_song = "Lover" #first song in dataset
  index = 0
  for i in df_dict:
    if i['song_title'].lower().strip() != current_song.lower().strip():
        index += 1
        current_song = i['song_title']
    #index = i['index']
    lyric = i['lyric']
    if index in index_dic:
        index_dic[index].append(lyric)
    else:
        index_dic[index] = [lyric]
        title = i['song_title'].lower().strip()
        song_to_index[title] = index 

  index_to_song = {index:song for song, index in song_to_index.items()} #https://dev.to/petercour/swap-keys-and-values-in-a-python-dictionary-1njn
  num_songs = len(song_to_index)
  print(song_to_index)

  vectorizer = TfidfVectorizer(stop_words = 'english', min_df = 2)

  #code from 4300 class demo
  word_splitter = re.compile(r"""
    (\w+)
    """, re.VERBOSE)
  
  stemmer = PorterStemmer()

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
    all_words = [w.lower() for w in word_splitter.findall(lyric_str)]
    stemmed_words = [stemmer.stem(w) for w in all_words]
    #all_words = getwords(lyric_str)
    lyrics_list.append(" ".join(stemmed_words))

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
  np.save('cosine_matrix_stem', cos_sim)

def evaluate_stem(not_stemmed, stemmed):
  """
  Evaluates the effect of stemming on the cosine similarities
  not_stemmed: np.array
  stemmed: np.array
  Returns: int, int
  """
  ns_avgs = [] #avg cosine sims for non-stemmed words
  s_avgs = [] #avg cosine sims for stemmed words
  size_ns = np.shape(not_stemmed)
  print(size_ns)
  size_ns = size_ns[0]
  random_nums = []
  #look at 50 random songs
  while len(random_nums) < 51:
    random_num = random.randint(0, size_ns-1) 
    if not random_num in random_nums:
      random_nums.append(random_num)
  
  for i in random_nums:
    #get cosine sims for stemmed and not stemmed and then sort
    cs_not_stemmed = not_stemmed[i]
    cs_stemmed = stemmed[i]
    cs_not_stemmed = cs_not_stemmed[::-1]
    cs_stemmed = cs_stemmed[::-1]
    not_stemmed_avg = 0
    stemmed_avg = 0
    j = 0
    #compute the average cosine sim for the top 10 songs
    while j < 10:
      not_stemmed_avg += cs_not_stemmed[j]
      stemmed_avg += cs_stemmed[j]
      j += 1
    not_stemmed_avg = not_stemmed_avg/10
    stemmed_avg = stemmed_avg/10
    ns_avgs.append(not_stemmed_avg)
    s_avgs.append(stemmed_avg)
  return ns_avgs, s_avgs

def printDifferences(ns_avgs, s_avgs):
  """
  Prints the average differences between not stemmed and stemmed
  ns_avgs: list
  s_avgs: list
  """
  i = 0
  difference = []
  while i < len(ns_avgs):
    diff = s_avgs[i] - ns_avgs[i]
    difference.append(diff)
    i += 1
  print("Stemming improvements")
  print(difference)
  difference.sort()
  print("worst:")
  print(difference[0])
  print("best:")
  print(difference[-1])
  sum_diff = 0
  j = 0
  while j < len(difference):
    sum_diff += difference[j]
    j += 1
  sum_diff = sum_diff/len(difference)
  print("Average improvement")
  print(sum_diff)

if __name__ == '__main__':
  #stemming()
  not_stemmed = np.array(np.load('cosine_matrix.npy'))
  stemmed = np.array(np.load('cosine_matrix_stem.npy'))
  ns_avgs, s_avgs = evaluate_stem(not_stemmed, stemmed)
  print("Averages without stemming")
  print(ns_avgs)
  print()
  print("Averages with stemming")
  print(s_avgs)
  print()
  printDifferences(ns_avgs, s_avgs)