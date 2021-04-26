class TreeNode {
  int num;
  TreeNode yes;
  TreeNode no;

  def __init__(self, num, yes, no):
    self.num = num
    self.yes = yes
    self.no = no
}

city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 3:"Burlington", 4:"Austin",
5:"Charlotte", 6:"San Francisco", 7:"Los Angeles", 8:"Seattle", 9:"Miami"}

questions_to_num = {1: "Would you like a big population?", 
2:"Would you like a big population density?", 
3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
5:"Are you working in tech?", 6:"Are you working in business?"
7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
16:"Do you like barbecque?", 
17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
26:"Do you prefer to take the metro?"}

industry_to_num = {0:"Finance", 1:"Tech", 2:"Business", 3:"Medicine", 4:"Education",
5:"Entertainment", 6:"Music"}

food_to_num = {0:"Italian", 1:"Mexican", 2:"Seafood", 3:"Vegetarian", 4:"Fried food", 5:"Barbecque"}

activity_to_num = {0:"Sports", 1:"Museums", 2:"Bars", 3:"Hiking", 4:"Beach", 5:"Shopping"}

transportation = {0:"Drive", 1:"Walk", 2:"Bus", 3:"Metro"}

size_to_num = {0:"Small", 1:"Big"}

pop_density_to_num = {0:"Small", 1:"Big"}

cost_living_to_num = {0:"Low", 1:"High"}

question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
15:4,16:4,17:5,18:5, 19:5,20:5,21:5,22:5,23:6,24:6,25:6}

question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3}

#dataset takes shape of
#size | pop density | cost of living | industry | food | activity | |transporation | label
train_set = [[1,1,0,0,0,1,2,0], [1,1,0,1,0,2,1,0], [1,1,0,0,3,5,6,0], [1,1,0,2,0,2,3,0],
[1,1,0,3,0,0,3,1],[1,1,0,4,0,1,1,1],[1,1,0,1,2,3,3,1],[1,1,0,3,2,0,1,1],
[0,0,0,4,3,3,2,2],[0,0,0,4,0,5,0,2],[0,0,0,3,3,3,0,2],
[0,0,0,3,2,3,0,3],[0,0,0,4,0,5,2,3],[0,0,0,3,0,3,0,3]]

#given a question, breaks the set into "yes" answers and "no" answers
def breakInputs(question_num, set_remaining):
  true = []
  false = []
  index = question_to_index[question_num]:
  for lst in set_remaining:
    answer = lst[index]
    if answer in question_to_yes_answers[question_num]:
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
    prob = class_freq[cl]/len(class_freq) #frequency for that class/total num of classes
    gini_sum += prob * (1-prob)
  return gini_sum

def infoGain(parent_infogain, true_input, false_input, gini_true, gini_false):
  avg_gini = (true_length * gini_true)/len(true_input) + (false_length * gini_false)/len(false_input)
  return parent_infogain - avg_gini

#determines the correct question
def get_question(parent_infogain, dataset, possible_questions):
  best_q = 0
  highest_ig = 0
  true_set = []
  false_set = []
  for qu in possible_questions:
    true_data, false_data = breakInputs(qu, dataset) #get true and false sets
    true_gini = computeGini(true_data)
    false_gini = computeGini(false_data)
    info_gain = infoGain(parent_infogain, true_data, false_data, true_gini, false_gini)
    if info_gain > highest_ig:
      highest_ig = info_gain
      best_q = qu
      true_set = true_data
      false_set = false_data
  return best_q, highest_ig, true_set, false_set

def create_Tree(dataset, prev_info_gain, questions):
  #base cases
  if len(dataset) == 0:
    return TreeNode(0, None, None) #if nothing left in the dataset, return default of New York
  
  #check if they're all the same class--if so create leaf node
  r = 0
  class_seen = -1
  all_same = True
  for i in dataset:
    #if first round,
    if r = 0:
      class_seen = dataset[i][-1]
      r = 1
    else:
      if not class_seen == dataset[i][-1]:
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
  best_q, highest_ig, true_set, false_set = get_question(dataset, parent_infogain, questions)
  questions.remove(best_q)
  true_side = create_Tree(true_set, highest_ig, questions)
  false_side = create_Tree(false_set, highest_ig, questions)

  return TreeNode(best_q, true_side, false_side)

def main():
  questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
  tree = createTree(dataset, 1, questions)