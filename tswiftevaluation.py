import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import PorterStemmer
import random

def getVectorizer(df, stop_words):
  if stop_words:
    return TfidfVectorizer(stop_words = 'english', min_df = df)
  else:
    return TfidfVectorizer( min_df = df)

#original code from cosinesim.py edited to add stemming
def stemming(doc_freq, english):
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
  #print(song_to_index)

  #print(type(df))
  vectorizer = getVectorizer(doc_freq, english)

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
  #np.save('cosine_matrix_stem', cos_sim)
  return cos_sim

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
    cs_not_stemmed = np.sort(cs_not_stemmed)
    cs_stemmed = np.sort(cs_stemmed)
    j = np.shape(cs_not_stemmed)
    j = j[0] - 2
    not_stemmed_avg = 0
    stemmed_avg = 0
    count = 0
    j = 0
    #compute the average cosine sim for the top 10 songs
    while count < 10:
      not_stemmed_avg += cs_not_stemmed[j]
      stemmed_avg += cs_stemmed[j]
      j = j - 1
      count += 1
    not_stemmed_avg = not_stemmed_avg/10
    stemmed_avg = stemmed_avg/10
    ns_avgs.append(not_stemmed_avg)
    s_avgs.append(stemmed_avg)
  return ns_avgs, s_avgs

def evaluateDF(cos_sim, random_nums):
  """
  Computes the mean of the average of the top 10 cosine similarities of all
  the song indices in random_nums
  cos_sim: np array
  random_nums: list
  Returns: int
  """
  avg_sims = []
  for i in random_nums:

    sim = cos_sim[i]
    sim = np.sort(sim)
    j = np.shape(sim)
    j = j[0] - 2 #don't want first b/c that is itself
    count = 0
    avg = 0
    while count < 10:
      avg += sim[j]
      j = j - 1
      count += 1
    avg_sims.append(avg/10)
  total_avg = 0
  for k in avg_sims:
    total_avg += k
  return total_avg/len(random_nums)


   

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

def evaluateTopTen(cos_sim, random_nums):
  avg_sims = []
  for i in random_nums:
    sim = cos_sim[i]
    #sim.sort(reverse=True)
    #sim = sim[::-1]
    #print(sim)
    sim = np.sort(sim)
    j = np.shape(sim)
    j = j[0] - 2 #don't want first b/c that is itself
    count = 0
    cossim = []
    while count < 10:
      cossim.append(sim[j])
      j = j - 1
      count += 1
    avg_sims.append(cossim)
    #cossim = []
    #while j < 10:
      #cossim.append(sim[j])
      #j += 1
    #avg_sims.append(cossim)
  print(avg_sims)
  top_avg = []
  k = 0
  current = 0
  while k < 10:
    for m in avg_sims:
      current += m[k]
    current = current / 50
    top_avg.append(current)
    k += 1
    current = 0
  return top_avg 



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
  
  """
  #original = np.array(np.load('cosine_matrix_stem.npy'))
  i = 1
  #get 50 random songs to look at
  #change the df each time up to 26
  random_nums = []
  while i < 26:
    print(type(i))
    cs_matrix = stemming(i, True)
    if i == 1:
      cs_shape = np.shape(cs_matrix)
      print(cs_shape)
      cs_size = cs_shape[0]
      while len(random_nums) < 51:
        random_num = random.randint(0, cs_size-1) 
        if not random_num in random_nums:
          random_nums.append(random_num)
    avg_cs = evaluateDF(cs_matrix, random_nums)
    print("df = " + str(i))
    print(avg_cs)
    i += 1
  """
  """
  cs_matrix = stemming(2, True)
  random_nums = []
  cs_shape = np.shape(cs_matrix)
  cs_size = cs_shape[0]
  while len(random_nums) < 51:
    random_num = random.randint(0, cs_size-1)
    if not random_num in random_nums:
      random_nums.append(random_num)
  top_avg = evaluateTopTen(cs_matrix, random_nums)
  print(top_avg)

"""
    