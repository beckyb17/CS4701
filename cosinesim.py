import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import PorterStemmer

#open dataset and convert into a dictionary
df = pd.read_csv('final_taylor_swift_lyrics.tsv', sep='\t')
df_dict = df.to_dict(orient = 'records')

#song to index maps song titles to their index
#index dic maps song index to a list of its lyrics
song_to_index = {}
original_index = {}
index_dic = {}
current_song = "Lover" #first song in dataset
index = 0
#create the index dic
for i in df_dict:
  #song lyrics span multiple entries (combine here)
  if i['song_title'].lower().strip() != current_song.lower().strip():
      index += 1
      current_song = i['song_title']
  lyric = i['lyric']
  if index in index_dic:
      index_dic[index].append(lyric)
  else:
      index_dic[index] = [lyric]
      title = i['song_title'].lower().strip()
      song_to_index[title] = index 
      original_index[i['song_title'].strip()] = index

index_to_song = {index:song for song, index in song_to_index.items()}
index_to_song_org = {index:song for song, index in original_index.items()} #https://dev.to/petercour/swap-keys-and-values-in-a-python-dictionary-1njn
num_songs = len(song_to_index)

#create the vectorizer object
vectorizer = TfidfVectorizer(stop_words = 'english', min_df = 2)

#code from 4300 class demo
word_splitter = re.compile(r"""
  (\w+)
  """, re.VERBOSE)

stemmer = PorterStemmer()

#create a list of the lyrics for each song
lyrics_list = []
for i in index_dic:
  lyric = index_dic[i]
  lyric_str = ""
  for l in lyric:
      l.lower()
      lyric_str += " "
      lyric_str += l
  all_words = [w.lower() for w in word_splitter.findall(lyric_str)] #code from 4300 class demo
  stemmed_words = [stemmer.stem(w) for w in all_words]
  lyrics_list.append(" ".join(all_words))

#create the tf-idf matrix
tfidf_vec = vectorizer.fit_transform(lyrics_list).toarray()

#create a cos sim matrix initialized with zeros
cos_sim = np.zeros((num_songs,num_songs))

#compute the cosine similarity between all of the songs
i = 0
while i < num_songs:
  j = 0
  while j < num_songs:
    #compute the cosine similarity
    song1 = tfidf_vec[i]
    song2 = tfidf_vec[j]
    song1_norm = np.linalg.norm(tfidf_vec[i])
    song2_norm = np.linalg.norm(tfidf_vec[j])
    numerator = np.dot(song1, song2)
    denominator = song1_norm * song2_norm
    cosine_similarity = numerator/denominator
    #add cosine similarity to the matrix
    cos_sim[i][j] = cosine_similarity
    j += 1
  i += 1

np.save('cosine_matrix', cos_sim)


