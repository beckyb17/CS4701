import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import PorterStemmer
import random

def getVectorizer(df, stop_words):
  """
  Returns a tf-idf vectorizer with the corresponding parameters
  df: int (minimum docuent frequency)
  stop_words: boolean (whether to eliminate english stop words)
  returns: tf-idf vectorizer
  """
  if stop_words:
    return TfidfVectorizer(stop_words = 'english', min_df = df)
  else:
    return TfidfVectorizer( min_df = df)

#original code from cosinesim.py (edited here to add stemming)
def stemming(doc_freq, english):
  """
  Computes the cosine similarity matrix using stemmed words
  doc_freq: int (minimum document frequency)
  english: boolean
  Returns: np array (cosine similarity matrix)
  """
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
  vectorizer = getVectorizer(doc_freq, english)

  #code from 4300 class demo
  word_splitter = re.compile(r"""
    (\w+)
    """, re.VERBOSE)
  
  stemmer = PorterStemmer()

  #create a list of the lyrics in each song and stem them
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
    lyrics_list.append(" ".join(stemmed_words))

  #create the tf-idf matrix
  tfidf_vec = vectorizer.fit_transform(lyrics_list).toarray()

  #compute the cosine similarity between all of the songs
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
    cos_sim = cos_sim[i]
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

def evaluateTopTen(cos_sim, set_matrix, cos_constant, set_constant, random_nums):
  """
  Computes the average score for the top 10 words for the songs in random_nums
  cos_sim: np array
  set_matrix: np array
  cos_constant: int
  set_constant: int
  random_nums: list
  Returns: int
  """
  avg_sims = []
  #loop through all of the cities
  j = 0
  while j < 10:
    #loop through all of the songs
    for i in random_nums:
      new_cos_sim = cos_sim[i]
      new_set_sim = set_matrix[j]
      #remove current song
      new_cos_sim = np.delete(new_cos_sim, i)
      new_set_sim = np.delete(new_set_sim, i)
      k = 0
      sims_dic = {}
      #combine the cosine sim and jaccard sim and sort from highest to smallest
      while k < len(new_cos_sim):
        cosine_similarity = new_cos_sim[k]
        jaccard_similarity = new_set_sim[k]
        sims_dic[k] = cosine_similarity*cos_constant + jaccard_similarity*set_constant
        k += 1
      total_sims_sorted = sorted(sims_dic.items(), key = lambda pair:pair[1], reverse = True)
      avg_top_10 = 0
      count = 0
      #compute the average score of the top 10
      while count < 10:
        avg_top_10 += total_sims_sorted[count][1]
        count += 1
      avg_sims.append(avg_top_10/10)
    j += 1
  avg_total = 0
  #compute the average of all of the scores
  for num in avg_sims:
    avg_total += num

  return avg_total/len(avg_sims)


if __name__ == '__main__':
  #call first if haven't stemmed the matrix before
  #stemming()
  #compute the effects of stemming
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

  #compute the effects of changing the doc frequency
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

  #originally: looked at how the cosine similarity changed among the top 10
  #songs (evaluate top ten later changed to measure jaccard similarity)
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

  #compute the effects of adding the jaccard similarity
  cs_matrix = np.load('cosine_matrix.npy')
  set_matrix = np.load('set_matrix.npy')
  random_nums = []
  cs_shape = np.shape(cs_matrix)
  cs_size = cs_shape[0]
  #get 50 random songs
  while len(random_nums) < 51:
    random_num = random.randint(0, cs_size-1) 
    if not random_num in random_nums:
      random_nums.append(random_num)
  
  #change the cosine sim and jaccard sim weights
  cs_weight = 100
  set_weight = 0
  while set_weight <= 100:
    print("cs weight " + str(cs_weight))
    print("set weight " + str(set_weight))
    top_avg = evaluateTopTen(cs_matrix, set_matrix, cs_weight, set_weight, random_nums)
    cs_weight -= 10
    set_weight += 10
    print("top 10 average is " + str(top_avg))