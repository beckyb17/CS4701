class TreeNode:
  def __init__(self, num, yes, no):
    self.num = num
    self.yes = yes
    self.no = no

#given a question, breaks the set into "yes" answers and "no" answers
def breakInputs(question_num, set_remaining, question_to_index, question_to_yes_answers):
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
  class_freq = numOfClasses(lst)
  gini_sum = 0
  for cl in class_freq:
    prob = class_freq[cl]/len(lst) #frequency for that class/total num of classes
    gini_sum += prob * (1-prob)
  return gini_sum

def infoGain(parent_infogain, true_input, false_input, gini_true, gini_false):
  total_length = len(true_input) + len(false_input)
  avg_gini = (len(true_input) * gini_true)/total_length + (len(false_input) * gini_false)/total_length
  return avg_gini
  #return parent_infogain - avg_gini

#determines the correct question
def get_question(parent_infogain, dataset, possible_questions, question_to_index, question_to_yes_answers):
  best_q = 0
  highest_gi = 2
  #highest_ig = 0
  true_set = []
  false_set = []
  for qu in possible_questions:
    true_data, false_data = breakInputs(qu, dataset, question_to_index, question_to_yes_answers) #get true and false sets
    true_gini = computeGini(true_data)
    false_gini = computeGini(false_data)
    #right now just using the highest gini impurity--can play around with
    #other types (info gain (related to gi) and entropy) to see which is best
    info_gain = infoGain(parent_infogain, true_data, false_data, true_gini, false_gini)
    if info_gain < highest_gi:
      highest_gi = info_gain
      best_q = qu
      true_set = true_data
      false_set = false_data
  return best_q, highest_gi, true_set, false_set

def create_Tree(dataset, prev_info_gain, questions, question_to_index, question_to_yes_answers):
  #base cases
  if len(dataset) == 0:
    return TreeNode(0, None, None) #if nothing left in the dataset, return default of New York
  
  #check if they're all the same class--if so create leaf node
  r = 0
  class_seen = -1
  all_same = True
  for i in dataset:
    #if first round,
    if r == 0:
      print(i,class_seen)
      class_seen = i[-1]
      r = 1
    else:
      print(i,class_seen)
      if not class_seen == i[-1]:
        all_same = False
  if all_same:
    return TreeNode(class_seen, None, None) #leaf node where the number is the city
  
  #check if there's no more questions left--if so return city with highest freq
  if len(questions) == 0:
    city_frequency = numOfClasses(dataset)
    most_common_city = -1
    highest_freq = 0
    for city in city_frequency:
      if city_frequency[city] > highest_freq:
        most_common_city = city
        highest_freq = city_frequency[city]
    return TreeNode(most_common_city, None, None)
  
  #not base case
  best_q, highest_ig, true_set, false_set = get_question(prev_info_gain, dataset, questions, question_to_index, question_to_yes_answers)

  questions.remove(best_q)
  true_side = create_Tree(true_set, highest_ig, questions, question_to_index, question_to_yes_answers)
  false_side = create_Tree(false_set, highest_ig, questions, question_to_index, question_to_yes_answers)

  return TreeNode(best_q, true_side, false_side)


def getResult(node):
  if node.yes == None and node.no == None:
    city_result = city_to_num[node.num]
    return city_result
  question_num = node.num
  user_response = input(questions_to_num[question_num]) #need to input y or n--will be different with the gui
  valid = False
  if user_response.lower() == 'y':
    return getResult(node.yes)
  else:
    return getResult(node.no)


"""
def main():
  print("in main")
  questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
  tree = create_Tree(train_set, 1, questions)
  result = getResult(tree)
  print(result)

if __name__ == '__main__':
  main()
"""