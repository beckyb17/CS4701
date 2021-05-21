import math

class TreeNode:
  def __init__(self, num, yes, no):
    self.num = num
    self.yes = yes
    self.no = no

def breakInputs(question_num, set_remaining, question_to_index, question_to_yes_answers):
  """
  Breaks the set into "yes" answers and "no" answers for a specific question
  question_num: int
  set_remaining: list
  question_to_index: dic
  question_to_yes_answers: dic
  Returns: list, list
  """
  true = []
  false = []
  index = question_to_index[question_num]
  for lst in set_remaining:
    answer = lst[index]
    if answer == question_to_yes_answers[question_num]:
      true.append(lst)
    else:
      false.append(lst)
  return true, false

#returns the frequency of the class for a specific question
def numOfClasses(lst):
  """
  Returns the frequency of each class for a specific question
  lst: list 
  Returns: dic
  """
  freqs = {}
  for inp in lst:
    cl = inp[-1]  #class is the last entry
    if cl in freqs:
      freqs[cl] += 1
    else:
      freqs[cl] = 1
  return freqs

#computes the gini impurity for a specific list of either true/false answers
def computeGini(lst):
  """
  Computes the gini impurity for a specific list of either true or false answers
  lst: list
  Returns: int
  """
  class_freq = numOfClasses(lst)
  gini_sum = 0
  for cl in class_freq:
    prob = class_freq[cl]/len(lst) #frequency for that class/total num of classes
    gini_sum += prob * (1-prob)
  return gini_sum

def avgGini(true_input, false_input, gini_true, gini_false):
  """
  Computes the average of the true and false gini impurities for a specific node
  true_input: list
  false_input: list
  gini_true: int
  gini_false: int
  Returns: int
  """
  total_length = len(true_input) + len(false_input)
  avg_gini = (len(true_input) * gini_true)/total_length + (len(false_input) * gini_false)/total_length
  return avg_gini

#determines the correct question
def get_question(dataset, possible_questions, question_to_index, question_to_yes_answers):
  """
  Determines the best question to split the data at a specific node
  dataset: list of lists
  possible_questions: list
  question_to_index: dic
  question_to_yes_answers: dic
  Returns: string, int, list, list
  """
  best_q = 0
  best_gi = 2
  true_set = []
  false_set = []
  for qu in possible_questions:
    true_data, false_data = breakInputs(qu, dataset, question_to_index, question_to_yes_answers) #get true and false sets
    true_gini = computeGini(true_data)
    false_gini = computeGini(false_data)
    avg_gini = avgGini(true_data, false_data, true_gini, false_gini)
    if avg_gini < best_gi:
      best_gi = avg_gini
      best_q = qu
      true_set = true_data
      false_set = false_data
  return best_q, best_gi, true_set, false_set

def highestFrequency(dataset):
  """
  Returns the city with the highest frequency out of the remaining dataset
  datset: list of lists
  Returns: tree node
  """
  city_frequency = numOfClasses(dataset)
  most_common_city = -1
  highest_freq = 0
  for city in city_frequency:
    if city_frequency[city] > highest_freq:
      most_common_city = city
      highest_freq = city_frequency[city]
  return TreeNode(most_common_city, None, None)

def create_Tree(dataset, parent_gi, questions, question_to_index, question_to_yes_answers):
  """
  Creates the decision tree
  dataset: list of lists
  questions: list
  question_to_index: dic
  question_to_yes_answers: dic
  """
  
  #base cases
  if len(dataset) == 0:
    return TreeNode(0, None, None) #if nothing left in the dataset, return default of New York

  #check if they're all the same class--if so create leaf node
  r = 0
  class_seen = -1
  all_same = True
  for i in dataset:
    #if first round
    if r == 0:
      class_seen = i[-1]
      r = 1
    else:
      if not class_seen == i[-1]:
        all_same = False
  if all_same:
    return TreeNode(class_seen, None, None) #leaf node where the number is the city
  
  #check if there's no more questions left--if so return city with highest freq
  if len(questions) == 0:
    return highestFrequency(dataset)

  #not base case
  best_q, best_gi, true_set, false_set = get_question(dataset, questions, question_to_index, question_to_yes_answers)
  questions.remove(best_q)

  #pre pruning: if the new gi isn't a significant improvement, don't break (becomes a leaf)
  if abs(parent_gi - best_gi) < .01:
    return highestFrequency(dataset)

  true_side = create_Tree(true_set, best_gi, questions, question_to_index, question_to_yes_answers)
  false_side = create_Tree(false_set, best_gi, questions, question_to_index, question_to_yes_answers)

  return TreeNode(best_q, true_side, false_side)