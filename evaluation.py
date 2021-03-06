import decisiontree
import random

#output_file = open("output.txt", 'w')
def getResult(node, test, question_to_yes_answers, question_to_index):
  """
  Returns the city classification (integer) for an entry in the dataset
  node: tree node of the decision tree
  test: one entry in the test subset (list)
  question_to_yes_answers: dic
  question_to_index: dic
  Returns: int
  """
  if node.yes == None and node.no == None:
    return node.num
  #process the question and the entry's answer
  question_num = node.num
  question_index = question_to_index[question_num]
  ans = test[question_index]
  yes_option = question_to_yes_answers[question_num]
  #check the test's answer
  if ans == yes_option:
    return getResult(node.yes, test, question_to_yes_answers, question_to_index)
  else:
    return getResult(node.no, test, question_to_yes_answers, question_to_index)

#function to run the test set. node = tree, test = test set
def testSet(node, test, question_to_yes_answers, question_to_index):
  """
  Run the test set and determine the accuracy
  node: decision tree node
  test: subset of the dataset (list of lists)
  question_to_yes_answers: dic
  question_to_index: dic
  Returns: int
  """
  num_correct = 0
  wrong_tests = []
  #loop through every entry in the test set
  for t in test:
    result = getResult(node, t, question_to_yes_answers, question_to_index)
    #if result is correct
    if result == t[-1]:
      num_correct += 1
    else:
      wrong_tests.append(t)
  correct_percent = num_correct/len(test)
  return correct_percent, wrong_tests

def firstTraining():
  """
  Runs the evaluation for the first dataset and prints the accuracy statistics
  """
  #output_file.write("Test 1 \n")
  city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 3:"Burlington", 4:"Austin",
  5:"Charlotte", 6:"San Francisco", 7:"Los Angeles", 8:"Seattle", 9:"Miami"}

  questions_to_num = {1: "Would you like a big population?", 
  2:"Would you like a big population density?", 
  3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
  5:"Are you working in tech?", 6:"Are you working in business?",
  7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
  10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
  13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
  16:"Do you like barbecque?", 
  17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
  20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
  23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
  26:"Do you prefer to take the metro?", 27:"Do you like to ski?"}

  industry_to_num = {0:"Finance", 1:"Tech", 2:"Business", 3:"Medicine", 4:"Education",
  5:"Entertainment", 6:"Music", 6:"Skiing"}

  food_to_num = {0:"Italian", 1:"Mexican", 2:"Seafood", 3:"Vegetarian", 4:"Fried food", 5:"Barbecque"}

  activity_to_num = {0:"Sports", 1:"Museums", 2:"Bars", 3:"Hiking", 4:"Beach", 5:"Shopping"}

  transportation = {0:"Drive", 1:"Walk", 2:"Bus", 3:"Metro"}

  size_to_num = {0:"Small", 1:"Big"}

  pop_density_to_num = {0:"Small", 1:"Big"}

  cost_living_to_num = {0:"Low", 1:"High"}

  question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
  15:4,16:4,17:5,18:5, 19:5,20:5,21:5,22:5,23:6,24:6,25:6,26:6, 27:5}

  question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
  17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3, 27:6}

  #dataset takes shape of
  #size | pop density | cost of living | industry | food | activity | |transporation | label
  dataset = [[1,1,1,0,0,1,2,0], [1,1,1,1,0,2,1,0], [1,1,1,3,5,6,1,0], [1,1,1,2,0,2,3,0],
  [1,1,1,3,0,0,3,1],[1,1,1,4,0,1,1,1],[1,1,1,1,2,3,3,1],[1,1,1,3,2,0,1,1],
  [0,0,0,4,3,3,2,2],[0,0,0,4,0,5,0,2],[0,0,0,3,3,3,0,2],[0,0,0,3,4,6,2,2],
  [0,0,0,3,2,3,0,3],[0,0,0,4,0,5,2,3],[0,0,0,3,0,3,0,3],[0,0,0,4,2,5,2,3],
  [0,0,0,2,4,5,0,4],[0,0,0,1,2,0,0,4],[0,0,0,1,5,3,0,4],[0,0,0,4,4,2,2,4],
  [0,0,0,0,4,0,0,5],[0,0,0,0,5,3,0,5],[0,0,0,2,3,3,2,5],[0,0,0,3,3,5,0,5],
  [0,1,1,1,1,1,0,6],[0,1,1,1,2,4,3,6],[0,1,1,0,3,5,2,6],[0,1,1,0,3,1,1,6],
  [1,1,0,5,1,4,0,7],[1,1,0,5,3,2,2,7],[1,1,0,5,1,3,0,7],[1,1,0,6,1,5,0,7],
  [0,0,1,1,0,5,0,8],[0,0,1,1,3,1,1,8],[0,0,1,1,2,5,3,8],[0,0,1,2,0,3,3,8],
  [0,0,0,0,3,4,0,9],[0,0,0,2,3,4,2,9],[0,0,0,0,5,4,2,9],[0,0,0,2,0,5,0,9],
  [0,0,0,7,0,3,0,3], [0,0,0,4,2,3,0,3], [1,1,1,0,0,2,3,0], [1,1,1,3,0,0,3,1],
  [0,0,0,1,5,5,0,4], [0,1,1,1,3,3,2,6]]
  
  k = 0
  while k < 10:
    percent_correct = 0
    j = 0
    total = 0
    train_rows = []
    while j < 100:
      total = range(len(dataset))
      #divide into training and test set
      train_rows = random.sample(total, int(.8*len(dataset)))
      test_set = []
      train_set = []
      for i in total:
        if i in train_rows:
          train_set.append(dataset[i])
        else:
          test_set.append(dataset[i])
      #create the tree on this training dataset
      questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
      createtree = decisiontree.create_Tree(train_set, 2, questions, question_to_index, question_to_yes_answers)
      #test the test set
      percent, wrong = testSet(createtree, test_set, question_to_yes_answers, question_to_index)
      percent_correct += percent
      j += 1
    percent_correct = percent_correct/100
    #print(percent_correct)
    k += 1
  print()

def secondTraining():
  """
  Runs the evaluation for the second dataset and prints the accuracy statistics
  """
  #output_file.write("Test 2 \n")
  print("test 2")
  city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 3:"Burlington", 4:"Austin",
  5:"Charlotte", 6:"San Francisco", 7:"Los Angeles", 8:"Seattle", 9:"Miami"}

  questions_to_num = {1: "Would you like a big population?", 
  2:"Would you like a big population density?", 
  3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
  5:"Are you working in tech?", 6:"Are you working in business?",
  7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
  10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
  13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
  16:"Do you like barbecque?", 
  17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
  20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
  23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
  26:"Do you prefer to take the metro?", 27:"Do you like to ski?"}

  industry_to_num = {0:"Finance", 1:"Tech", 2:"Business", 3:"Medicine", 4:"Education",
  5:"Entertainment", 6:"Music", 6:"Skiing"}

  food_to_num = {0:"Italian", 1:"Mexican", 2:"Seafood", 3:"Vegetarian", 4:"Fried food", 5:"Barbecque"}

  activity_to_num = {0:"Sports", 1:"Museums", 2:"Bars", 3:"Hiking", 4:"Beach", 5:"Shopping"}

  transportation = {0:"Drive", 1:"Walk", 2:"Bus", 3:"Metro"}

  size_to_num = {0:"Small", 1:"Big"}

  pop_density_to_num = {0:"Small", 1:"Big"}

  cost_living_to_num = {0:"Low", 1:"High"}

  question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
  15:4,16:4,17:5,18:5, 19:5,20:5,21:5,22:5,23:6,24:6,25:6,26:6, 27:5}

  question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
  17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3, 27:6}

  #dataset takes shape of
  #size | pop density | cost of living | industry | food | activity |transporation | label
  dataset = [[1,1,1,0,0,1,2,0], [1,1,1,1,0,2,1,0], [1,1,1,3,5,6,1,0], [1,1,1,2,0,2,3,0],
  [1,1,1,0,0,2,3,0],[1,1,1,0,1,1,0],
  [1,1,1,3,0,0,3,1],[1,1,1,4,0,1,1,1],[1,1,1,1,2,3,3,1],[1,1,1,3,2,0,1,1],
  [0,1,1,3,0,1,2,1],[0,1,1,1,2,5,3,1],
  [0,0,0,4,3,3,2,2],[0,0,0,4,0,5,0,2],[0,0,0,3,3,3,0,2],[0,0,0,3,4,6,2,2],
  [0,0,0,4,3,3,0,2], [0,0,0,4,0,5,0,2],
  [0,0,0,3,2,3,0,3],[0,0,0,4,0,5,2,3],[0,0,0,3,0,3,0,3],[0,0,0,4,2,5,2,3],
  [0,0,0,3,2,3,2,3],[0,0,0,4,0,3,0,3],
  [0,0,0,2,4,5,0,4],[0,0,0,1,2,0,0,4],[0,0,0,1,5,3,0,4],[0,0,0,4,4,2,2,4],
  [0,0,0,1,4,4,0,4], [0,0,0,1,5,5,0,4],
  [0,0,0,0,4,0,0,5],[0,0,0,0,5,3,0,5],[0,0,0,2,3,3,2,5],[0,0,0,3,3,5,0,5],
  [0,0,0,3,5,0,0,5], [0,0,0,3,4,2,0,5], 
  [0,1,1,1,1,1,0,6],[0,1,1,1,2,4,3,6],[0,1,1,0,3,5,2,6],[0,1,1,0,3,1,1,6],
  [1,1,1,1,3,3,2,6],[1,1,1,3,1,4,2,6],
  [1,1,0,5,1,4,0,7],[1,1,0,5,3,2,2,7],[1,1,0,5,1,3,0,7],[1,1,0,6,1,5,0,7],
  [1,1,0,5,3,3,0,7],[1,1,0,5,1,3,0,7],
  [0,0,1,1,0,5,0,8],[0,0,1,1,3,1,1,8],[0,0,1,1,2,5,3,8],[0,0,1,2,0,3,3,8],
  [0,0,1,1,2,3,0,8], [0,0,1,1,3,3,0,8],
  [0,0,0,0,3,4,0,9],[0,0,0,2,3,4,2,9],[0,0,0,0,5,4,2,9],[0,0,0,2,0,5,0,9],
  [0,0,0,2,1,0,0,9], [0,0,0,2,4,4,0,9], 
  [0,0,0,3,0,3,0,3], [0,0,0,4,2,3,0,3], [1,1,1,0,0,2,3,0], [1,1,1,3,0,0,3,1],
  [0,0,0,1,5,5,0,4], [0,1,1,1,3,3,2,6]]

  k = 0
  while k < 10:
    #Separate into training and testing data
    total = range(len(dataset))
    train_rows = random.sample(total, int(.8*len(dataset)))
    test_set = []
    train_set = []
    for i in total:
      if i in train_rows:
        train_set.append(dataset[i])
      else:
        test_set.append(dataset[i])
    
    questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

    percent_correct = 0
    j = 0
    while j < 100:
    #create the tree on this dataset
      questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
      create_tree = decisiontree.create_Tree(train_set, 2, questions, question_to_index, question_to_yes_answers)
      #test the test set
      percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
      percent_correct += percent
      j += 1
    percent_correct = percent_correct/100
    #output_file.write("Percent correct: " + str(percent_correct) + " \n")
    print("percent correct is " + str(percent_correct))
    #print("wrong tests are " + str(wrong))
    print()
    k += 1


def thirdTraining():
  """
  Runs the evaluation for the third dataset and prints the accuracy statistics
  """
  #output_file.write("Test 3 \n")
  print("test 3")
  city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 4:"Austin",
  5:"Charlotte", 6:"San Francisco", 7:"Los Angeles", 8:"Seattle", 9:"Miami"}

  questions_to_num = {1: "Would you like a big population?", 
  2:"Would you like a big population density?", 
  3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
  5:"Are you working in tech?", 6:"Are you working in business?",
  7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
  10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
  13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
  16:"Do you like barbecque?", 
  17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
  20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
  23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
  26:"Do you prefer to take the metro?", 27:"Do you like to ski?",
  28: "Do you mind snow?", 29:"Do you mind rain?", 30:"I want the sun!",
  31:"Do you want to live in an apartment?", 32:"Do you want to live in a cotage?", 33:"Do you want to live in a big house?",
  34:"Do you speak more than 1 language?",
  35:"Do you prefer liberal neighborhood?", 36:"Do you prefer conservative neighborhood?",
  37:"Cloudy weather doesn't bother me!",38:"I prefer chill summer than hot summer."}

  size_to_num = {0:"Small", 1:"Big"}

  pop_density_to_num = {0:"Small", 1:"Big"}

  cost_living_to_num = {0:"Low", 1:"High"}

  industry_to_num = {0:"Finance", 1:"Tech", 2:"Business", 3:"Medicine", 4:"Education",
  5:"Entertainment", 6:"Music"}

  food_to_num = {0:"Italian", 1:"Mexican", 2:"Seafood", 3:"Vegetarian", 4:"Fried food", 5:"Barbecque"}

  activity_to_num = {0:"Sports", 1:"Museums", 2:"Bars", 3:"Hiking", 4:"Beach", 5:"Shopping",6:"Skiing"}

  transportation = {0:"Drive", 1:"Walk", 2:"Bus", 3:"Metro"}

  weather_and_temp = {0:"snow", 1:"rain", 2:"sunny", 3:"cloudy",4:"chill"}

  type_of_house = {0:"apartment", 1:"cotage", 2:"house"}

  speak_multiple_language = {0:"No", 1:"Yes"}

  politics = {0:"liberal", 1:"conservative"}

  question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
  15:4,16:4,17:5,18:5,19:5,20:5,21:5,22:5,23:6,24:6,25:6,26:6,27:5,
  28:7,29:7,30:7,31:8,32:8,33:8,34:9,35:10,36:10,37:7,38:7}

  question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
  17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3,27:6,28:0,29:1,30:2,31:0,32:1,33:2,34:1,35:0,36:1,37:3,38:4}

  #dataset takes shape of
  #size|pop density|cost of living|industry|food|activity|transporation|weather|house|language|politics| label
  dataset = [[1,1,1,0,0,1,2,0,0,1,0,0], [1,1,1,1,0,2,1,0,0,1,0,0], [1,1,1,3,0,6,1,2,0,1,0,0], [1,1,1,2,0,2,3,0,0,1,0,0],
  [1,1,1,0,0,2,3,0,0,1,0,0],[1,1,1,0,1,1,2,0,1,0,0],
  [0,1,1,3,0,0,3,0,0,1,0,1],[1,1,1,4,0,1,1,2,0,1,0,1],[1,1,1,1,2,3,3,0,2,1,0,1],[0,1,1,3,2,0,1,4,2,1,0,1],
  [0,1,1,3,0,1,2,4,0,1,0,1],[0,1,1,1,2,5,3,0,0,1,0,1],
  [0,0,0,4,3,3,2,0,2,0,0,2],[1,0,0,4,0,5,0,0,2,0,0,2],[0,0,0,3,3,3,0,0,0,0,0,2],[0,0,0,3,4,6,2,0,2,0,1,2],
  [0,0,0,4,3,3,0,4,0,0,0,2], [0,0,0,4,0,5,0,4,2,0,1,2],
  [0,0,0,2,4,5,0,2,2,0,1,4],[0,0,0,1,2,0,0,2,2,1,1,4],[1,0,0,1,5,3,0,2,2,1,1,4],[0,0,0,4,4,2,2,3,2,0,1,4],
  [0,0,0,1,4,4,0,2,2,1,1,4], [0,0,0,1,5,5,0,2,0,1,0,4],
  [0,0,0,0,4,0,0,3,2,0,0,5],[0,0,0,0,5,3,0,3,2,0,0,5],[0,0,0,2,3,3,2,2,2,1,0,5],[0,0,0,3,3,5,0,3,2,0,1,5],
  [0,0,0,3,5,0,0,1,2,0,0,5], [0,0,0,3,4,2,0,2,0,1,1,5], 
  [0,1,1,1,1,1,0,4,0,1,0,6],[0,1,1,1,2,4,3,4,0,1,0,6],[0,1,1,0,3,5,2,1,0,1,0,6],[0,1,1,0,3,1,1,2,0,1,0,6],
  [1,1,1,1,3,3,2,4,0,1,0,6],[1,1,1,3,1,4,2,4,0,1,0,6],
  [1,1,0,5,1,4,0,2,0,1,0,7],[1,1,0,5,3,2,2,2,0,1,0,7],[1,1,0,5,1,3,0,2,2,1,0,7],[1,1,0,6,1,5,0,2,2,1,0,7],
  [1,1,0,5,3,3,0,2,0,1,0,7],[1,1,0,5,1,3,0,3,0,1,0,7],
  [0,0,1,1,0,5,0,1,0,1,0,8],[0,0,1,1,3,1,1,1,2,1,0,8],[0,0,1,1,2,5,3,1,0,1,0,8],[0,0,1,2,0,3,3,1,2,0,0,8],
  [1,0,1,1,2,3,0,3,2,0,0,8], [1,0,1,1,3,3,0,3,2,1,0,8],
  [0,0,0,0,3,4,0,2,1,1,0,9],[0,0,0,2,3,4,2,2,1,1,1,9],[0,0,0,0,5,4,2,2,2,0,0,9],[0,0,0,2,0,5,0,2,2,0,1,9],
  [0,0,0,2,1,0,0,1,2,1,1,9], [0,0,0,2,4,4,0,2,0,0,0,9]]

  test_set = [[1,1,1,0,0,1,3,0,0,1,0,0],[1,0,1,3,2,5,2,4,0,1,0,1],[0,0,1,4,3,6,0,0,2,0,1,2],[0,0,0,4,4,6,0,0,2,0,0,3],
  [0,0,0,2,5,0,0,2,2,1,1,4],[0,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,0,1,5,1,4,0,2,0,1,0,7],
  [1,0,1,1,0,1,0,1,2,1,0,8],[1,0,0,2,5,4,0,2,1,1,1,9],
  [1,1,1,0,0,2,3,0,0,1,0,0],[1,0,1,3,2,5,2,4,0,1,0,1],[0,0,1,4,3,6,0,0,2,0,1,2],[0,0,0,4,4,6,0,0,2,0,0,3],
  [0,0,0,1,5,3,0,2,2,1,1,4],[0,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,1,0,5,3,2,2,2,0,1,0,7],
  [1,0,1,1,0,1,0,1,2,1,0,8],[0,0,0,2,4,4,0,2,0,0,0,9]]
  [[0,0,0,2,1,0,0,1,2,1,1,9], [0,0,0,2,4,4,0,2,0,0,0,9], 
  [1,1,1,0,0,1,3,0,0,1,0,0],[1,1,1,3,2,5,2,4,0,1,0,1],[0,0,0,4,3,6,0,0,2,0,1,2],
  [0,0,0,2,5,0,0,2,2,1,1,4],[0,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,0,1,5,1,4,0,2,0,1,0,7],
  [1,0,1,1,0,1,0,1,2,1,0,8],[0,0,0,2,5,4,0,2,1,1,1,9],
  [1,1,1,0,0,2,3,0,0,1,0,0],[1,0,1,3,2,5,2,4,0,1,0,1],[0,0,1,4,3,6,0,0,2,0,1,2],
  [0,0,0,1,5,3,0,2,2,1,1,4],[0,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,1,0,5,3,2,2,2,0,1,0,7],
  [1,0,1,1,0,3,0,1,2,1,0,8],[0,0,0,2,4,4,0,2,0,0,0,9]]

  k = 0
  while k < 10:
    total = list(range(len(dataset)))
    train_rows = random.sample(total, int(.8*len(dataset)))
    test_set = []
    train_set = []
    for i in total:
      if i in train_rows:
        train_set.append(dataset[i])
      else:
        test_set.append(dataset[i])
    
    questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]

    percent_correct = 0
    j = 0
    while j < 100:
    #create the tree on this dataset
      questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]
      create_tree = decisiontree.create_Tree(train_set, 2, questions, question_to_index, question_to_yes_answers)
      #test the test set
      percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
      percent_correct += percent
      j += 1
    percent_correct = percent_correct/100
    #output_file.write("Percent correct: " + str(percent_correct) + " \n")
    print("percent correct is " + str(percent_correct))
    #print("wrong tests are " + str(wrong))
    print()
    k += 1

def fourthTraining():
  """
  Runs the evaluation for the fourth dataset and prints the accuracy statistics
  Note: this dataset was also used for the pre-processing evaluation
  """
  #output_file.write("Test 4 \n")
  city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 3:"Austin",
  4:"Charlotte", 5:"San Francisco", 6:"Los Angeles", 7:"Seattle", 8:"Miami",
  9:"Nashville", 10:"Chicago"}

  questions_to_num = {1: "Would you like a big population?", 
  2:"Would you like a big population density?", 
  3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
  5:"Are you working in tech?", 6:"Are you working in business?",
  7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
  10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
  13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
  16:"Do you like barbecque?", 
  17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
  20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
  23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
  26:"Do you prefer to take the metro?", 27:"Do you like to ski?",
  28: "Are you okay with snow in the winter?", 29:"Are you okay with rain?", 
  30:"Do you want sunny weather year-round?",
  31:"Would you rather live in an apartment than a big house?", 
  32:"Do you prefer a liberal neighborhood over a conservative one?", 
  33:"Are you okay with humid summers?"}

  size_to_num = {0:"Small", 1:"Big"}

  pop_density_to_num = {0:"Small", 1:"Big"}

  cost_living_to_num = {0:"Low", 1:"High"}

  industry_to_num = {0:"Finance", 1:"Tech", 2:"Business", 3:"Medicine", 4:"Education",
  5:"Entertainment", 6:"Music"}

  food_to_num = {0:"Italian", 1:"Mexican", 2:"Seafood", 3:"Vegetarian", 4:"Fried food", 5:"Barbecque"}

  activity_to_num = {0:"Sports", 1:"Museums", 2:"Bars", 3:"Hiking", 4:"Beach", 5:"Shopping",6:"Skiing"}

  transportation = {0:"Drive", 1:"Walk", 2:"Bus", 3:"Metro"}

  weather_and_temp = {0:"Snow", 1:"Sunny", 2:"Moderate", 3:"Humid", 4:"Rain", 5:"Dry"}

  type_of_house = {0:"Apartment", 1:"House"}

  #speak_multiple_language = {0:"No", 1:"Yes"}

  politics = {0:"liberal", 1:"conservative"}

  question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
  15:4,16:4,17:5,18:5,19:5,20:5,21:5,22:5,23:6,24:6,25:6,26:6,27:5,
  28:7,29:8,30:7,31:9,32:10,33:8}

  question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
  17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3,27:6,28:0,29:4,30:1,31:0,32:0,33:3}

  #dataset takes shape of
  #size|pop density|cost of living|industry|food|activity|transporation|winter weather|
  #|summer weather|house|politics| label
  dataset = [[1,1,1,0,1,1,3,0,3,0,0,0],
  [1,1,1,0,0,2,1,0,3,0,0,0],
  [1,1,1,2,0,2,1,0,3,0,0,0],
  [1,1,1,2,0,2,3,0,3,0,0,0],
  [1,1,1,0,0,2,3,0,4,0,0,0],
  [1,1,1,1,0,2,3,0,4,0,0,0],
  [1,1,1,0,1,1,1,0,3,0,0,0],
  [0,1,1,1,0,0,2,0,3,0,0,1],
  [1,1,1,4,0,1,2,0,3,0,0,1],
  [1,1,1,3,2,3,3,0,4,1,0,1],
  [0,1,1,3,2,6,1,0,3,1,0,1],
  [0,1,1,3,0,3,2,0,4,0,0,1],
  [0,1,1,1,2,5,3,0,3,0,0,1],
  [0,0,0,4,3,3,2,0,3,1,0,2],
  [0,0,0,4,0,6,0,0,3,1,0,2],
  [0,0,0,3,3,3,0,0,3,1,0,2],
  [0,0,0,3,2,6,0,0,3,1,0,2],
  [0,0,0,4,3,3,0,0,3,1,0,2],
  [0,0,0,4,0,5,0,0,3,1,0,2],
  [0,0,0,1,4,5,0,1,5,1,1,3],
  [0,0,0,1,2,0,0,1,5,1,1,3],
  [0,0,0,1,5,2,0,1,5,1,1,3],
  [0,0,0,4,4,2,2,1,5,0,1,3],
  [0,0,0,1,4,4,0,1,5,1,1,3],
  [0,0,0,1,5,5,0,1,5,1,0,3],
  [0,0,0,0,4,0,0,2,5,1,1,4],
  [0,0,0,0,5,0,0,2,5,1,0,4],
  [0,0,0,2,4,3,2,2,5,1,0,4],
  [0,0,0,3,5,5,0,2,5,1,1,4],
  [0,0,0,3,5,2,0,2,5,1,1,4],
  [0,0,0,3,4,2,0,2,5,0,1,4],
  [0,1,1,1,1,2,0,2,5,0,0,5],
  [0,1,1,1,2,4,3,2,5,0,0,5],
  [0,1,1,1,3,3,0,2,5,0,0,5],
  [1,1,1,0,3,4,2,2,5,0,0,5],
  [1,1,1,1,3,3,2,2,5,0,0,5],
  [1,1,1,1,1,4,2,2,5,0,0,5],
  [1,1,0,5,1,4,0,1,5,0,0,6],
  [1,1,0,5,3,2,2,1,5,0,0,6],
  [1,1,0,5,1,3,0,1,5,1,0,6],
  [1,1,0,6,1,4,0,1,5,1,0,6],
  [1,1,0,5,3,3,0,1,5,0,0,6],
  [1,1,0,5,1,3,0,1,5,0,0,6],
  [0,0,1,1,0,6,0,0,4,0,0,7],
  [0,0,1,1,3,3,1,0,4,1,0,7],
  [0,0,1,1,2,6,3,0,4,0,0,7],
  [0,0,1,2,0,3,3,0,4,1,0,7],
  [0,0,1,1,2,3,0,0,4,1,0,7],
  [0,0,1,1,3,6,0,0,4,1,0,7],
  [0,0,0,0,5,4,0,1,3,1,0,8],
  [0,0,0,2,1,4,2,1,3,0,1,8],
  [0,0,0,0,5,4,2,1,3,1,0,8],
  [0,0,0,2,5,0,0,1,3,1,1,8],
  [0,0,0,2,1,0,0,1,3,1,1,8],
  [0,0,0,2,4,4,0,1,3,0,0,8],
  [0,0,0,6,4,1,0,1,3,1,1,9],
  [0,0,0,6,5,3,0,1,3,1,1,9],
  [0,0,0,5,4,1,1,1,3,0,1,9],
  [0,0,0,6,5,5,1,1,3,1,1,9],
  [0,0,0,5,5,1,0,1,3,0,1,9],
  [0,0,0,6,4,3,0,1,3,1,1,9],
  [1,1,1,2,5,5,2,0,5,0,0,10],
  [1,1,1,1,0,5,1,0,5,0,0,10],
  [1,1,1,2,5,2,0,0,4,1,0,10],
  [1,1,1,1,4,2,0,0,4,1,0,10],
  [1,1,1,2,4,5,0,0,4,0,0,10],
  [1,1,1,1,4,5,2,0,5,1,0,10]] 
  k = 0
  avg_correct = 0
  while k < 10:
    total = list(range(len(dataset)))
    train_rows = random.sample(total, int(.8*len(dataset)))
    test_set = []
    train_set = []
    for i in total:
      if i in train_rows:
        train_set.append(dataset[i])
      else:
        test_set.append(dataset[i])

    questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]

    percent_correct = 0
    j = 0
    while j < 100:
    #create the tree on this dataset
      questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
      create_tree = decisiontree.create_Tree(train_set, 2, questions, question_to_index, question_to_yes_answers)
      #test the test set
      percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
      percent_correct += percent
      j += 1
    percent_correct = percent_correct/100
    avg_correct += percent_correct
    #output_file.write("Percent correct: " + str(percent_correct) + " \n")
    print("percent correct is " + str(percent_correct))
    #print("wrong tests are " + str(wrong))
    print()
    k += 1
  avg_correct = avg_correct/10
  print("average correct is " + str(avg_correct))

def learningCurve():
  """
  Runs the evaluation for the learning curve and prints the accuracy statistics
  """
  city_to_num = {0: "New York", 1:"Boston", 2:"Ithaca", 3:"Austin",
  4:"Charlotte", 5:"San Francisco", 6:"Los Angeles", 7:"Seattle", 8:"Miami",
  9:"Nashville", 10:"Chicago"}

  questions_to_num = {1: "Would you like a big population?", 
  2:"Would you like a big population density?", 
  3:"Do you mind a high cost of living?", 4:"Are you working in finance?",
  5:"Are you working in tech?", 6:"Are you working in business?",
  7: "Are you working in medicine?", 8:"Are you working in education?", 9:"Are you working in entertainment?",
  10:"Are you working in music?", 11:"Do you like Italian food?", 12: "Do you like Mexican food?",
  13:"Do you like seafood?", 14:"Are you vegetarian?", 15:"Do you like fried food?", 
  16:"Do you like barbecque?", 
  17:"Do you like watching sport games?", 18:"Do you like going to museums?", 19:"Do you like going to bars?",
  20: "Do you like hiking?", 21: "Do you like the beach?", 22:"Do you like shopping?",
  23:"Do you prefer to drive?", 24:"Do you prefer to walk?", 25:"Do you prefer to take the bus?",
  26:"Do you prefer to take the metro?", 27:"Do you like to ski?",
  28: "Are you okay with snow in the winter?", 29:"Are you okay with rain?", 
  30:"Do you want sunny weather year-round?",
  31:"Would you rather live in an apartment than a big house?", 
  32:"Do you prefer a liberal neighborhood over a conservative one?", 
  33:"Are you okay with humid summers?"}

  politics = {0:"liberal", 1:"conservative"}

  question_to_index = {1:0,2:1,3:2,4:3,5:3,6:3,7:3,8:3,9:3,10:3,11:4,12:4,13:4,14:4,
  15:4,16:4,17:5,18:5,19:5,20:5,21:5,22:5,23:6,24:6,25:6,26:6,27:5,
  28:7,29:8,30:7,31:9,32:10,33:8}

  question_to_yes_answers = {1:1,2:1,3:0,4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:0,12:1,13:2,14:3,15:4,16:5,
  17:0,18:1,19:2,20:3,21:4,22:5,23:0,24:1,25:2,26:3,27:6,28:0,29:4,30:1,31:0,32:0,33:3}

  #dataset takes shape of
  #size|pop density|cost of living|industry|food|activity|transporation|winter weather|
  #|summer weather|house|politics| label
  dataset = [[1,1,1,0,1,1,3,0,3,0,0,0],
  [1,1,1,0,0,2,1,0,3,0,0,0],
  [1,1,1,2,0,2,1,0,3,0,0,0],
  [1,1,1,2,0,2,3,0,3,0,0,0],
  [1,1,1,0,0,2,3,0,4,0,0,0],
  [1,1,1,1,0,2,3,0,4,0,0,0],
  [1,1,1,0,1,1,1,0,3,0,0,0],
  [0,1,1,1,0,0,2,0,3,0,0,1],
  [1,1,1,4,0,1,2,0,3,0,0,1],
  [1,1,1,3,2,3,3,0,4,1,0,1],
  [0,1,1,3,2,6,1,0,3,1,0,1],
  [0,1,1,3,0,3,2,0,4,0,0,1],
  [0,1,1,1,2,5,3,0,3,0,0,1],
  [0,0,0,4,3,3,2,0,3,1,0,2],
  [0,0,0,4,0,6,0,0,3,1,0,2],
  [0,0,0,3,3,3,0,0,3,1,0,2],
  [0,0,0,3,2,6,0,0,3,1,0,2],
  [0,0,0,4,3,3,0,0,3,1,0,2],
  [0,0,0,4,0,5,0,0,3,1,0,2],
  [0,0,0,1,4,5,0,1,5,1,1,3],
  [0,0,0,1,2,0,0,1,5,1,1,3],
  [0,0,0,1,5,2,0,1,5,1,1,3],
  [0,0,0,4,4,2,2,1,5,0,1,3],
  [0,0,0,1,4,4,0,1,5,1,1,3],
  [0,0,0,1,5,5,0,1,5,1,0,3],
  [0,0,0,0,4,0,0,2,5,1,1,4],
  [0,0,0,0,5,0,0,2,5,1,0,4],
  [0,0,0,2,4,3,2,2,5,1,0,4],
  [0,0,0,3,5,5,0,2,5,1,1,4],
  [0,0,0,3,5,2,0,2,5,1,1,4],
  [0,0,0,3,4,2,0,2,5,0,1,4],
  [0,1,1,1,1,2,0,2,5,0,0,5],
  [0,1,1,1,2,4,3,2,5,0,0,5],
  [0,1,1,1,3,3,0,2,5,0,0,5],
  [1,1,1,0,3,4,2,2,5,0,0,5],
  [1,1,1,1,3,3,2,2,5,0,0,5],
  [1,1,1,1,1,4,2,2,5,0,0,5],
  [1,1,0,5,1,4,0,1,5,0,0,6],
  [1,1,0,5,3,2,2,1,5,0,0,6],
  [1,1,0,5,1,3,0,1,5,1,0,6],
  [1,1,0,6,1,4,0,1,5,1,0,6],
  [1,1,0,5,3,3,0,1,5,0,0,6],
  [1,1,0,5,1,3,0,1,5,0,0,6],
  [0,0,1,1,0,6,0,0,4,0,0,7],
  [0,0,1,1,3,3,1,0,4,1,0,7],
  [0,0,1,1,2,6,3,0,4,0,0,7],
  [0,0,1,2,0,3,3,0,4,1,0,7],
  [0,0,1,1,2,3,0,0,4,1,0,7],
  [0,0,1,1,3,6,0,0,4,1,0,7],
  [0,0,0,0,5,4,0,1,3,1,0,8],
  [0,0,0,2,1,4,2,1,3,0,1,8],
  [0,0,0,0,5,4,2,1,3,1,0,8],
  [0,0,0,2,5,0,0,1,3,1,1,8],
  [0,0,0,2,1,0,0,1,3,1,1,8],
  [0,0,0,2,4,4,0,1,3,0,0,8],
  [0,0,0,6,4,1,0,1,3,1,1,9],
  [0,0,0,6,5,3,0,1,3,1,1,9],
  [0,0,0,5,4,1,1,1,3,0,1,9],
  [0,0,0,6,5,5,1,1,3,1,1,9],
  [0,0,0,5,5,1,0,1,3,0,1,9],
  [0,0,0,6,4,3,0,1,3,1,1,9],
  [1,1,1,2,5,5,2,0,5,0,0,10],
  [1,1,1,1,0,5,1,0,5,0,0,10],
  [1,1,1,2,5,2,0,0,4,1,0,10],
  [1,1,1,1,4,2,0,0,4,1,0,10],
  [1,1,1,2,4,5,0,0,4,0,0,10],
  [1,1,1,1,4,5,2,0,5,1,0,10]] 

  #output = open('learningcurve.txt', 'w')
  i = 1
  while i < 11:
    total = range(len(dataset))
    #change the sizes of the training set
    train_rows = random.sample(total, int((i/10)*len(dataset)))
    train_set = []
    for k in total:
      if k in train_rows:
        train_set.append(dataset[k])
    
    #create a separate (consistent) test set for the learning curve
    test_set = [[1,1,1,0,0,5,3,0,3,0,0,0], [1,1,1,0,0,2,1,0,3,0,0,0], 
    [0,1,1,3,2,3,3,0,3,0,0,1],[1,1,1,3,2,3,3,0,3,1,0,1],
    [0,0,0,4,3,6,0,0,3,1,0,2],[0,0,0,3,2,3,0,0,3,1,0,2],
    [0,0,0,1,4,2,0,1,5,1,1,3],[0,0,0,1,5,5,0,1,5,1,0,3],
    [0,0,0,3,5,0,0,2,3,1,1,4],[0,0,0,3,5,5,0,2,5,1,1,4],
    [1,1,1,1,1,3,2,2,5,0,0,5],[1,1,1,1,3,3,2,2,5,0,0,5],
    [1,1,0,5,3,4,0,1,5,1,0,6],[1,1,0,5,3,3,0,1,5,0,0,6],
    [0,0,1,1,2,6,0,0,4,0,0,7],[0,0,1,1,0,3,0,0,4,0,0,7],
    [0,0,0,2,1,4,0,1,3,1,1,8],[0,0,0,2,1,0,2,1,3,1,1,8],
    [0,0,0,6,4,1,0,2,5,1,1,9],[0,0,0,5,4,3,0,1,3,1,1,9],
    [1,1,1,2,0,2,2,0,5,0,0,10],[1,1,1,1,0,5,1,0,5,0,0,10]]
    questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]

    percent_correct_test = 0
    j = 0
    while j < 1000:
    #create the tree on this dataset
      questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
      create_tree = decisiontree.create_Tree(train_set, 2, questions, question_to_index, question_to_yes_answers)
      #test the test set
      percent_test, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
      percent_correct_test += percent_test
      j += 1
    
    percent_correct_test = percent_correct_test/1000
    #output.write(str(i) + " percent correct: " + str(percent_correct) + " \n")
    print("percent correct test is " + str(percent_correct_test))
    #print("wrong tests are " + str(wrong))
    print()
    i += 1
  #output.close()

if __name__ == '__main__':
  """
  Run the evaluations
  """
  learningCurve()
  #firstTraining()
  #secondTraining()
  #thirdTraining()
  #fourthTraining()
  #i += 1

#output_file.close()


