import decisiontree
#gets the result for a specific test response
def getResult(node, test, question_to_yes_answers, question_to_index):
  if node.yes == None and node.no == None:
    return node.num
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
  num_correct = 0
  wrong_tests = []
  for t in test:
    result = getResult(node, t, question_to_yes_answers, question_to_index)
    print("result is " + str(result) + " " + "test answer is " + str(t[-1]))
    #if result is correct
    if result == t[-1]:
      num_correct += 1
    else:
      wrong_tests.append(t)
  correct_percent = num_correct/len(test)
  return correct_percent, wrong_tests

#50% correct
def firstTraining():
  print("test 1")
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
  train_set = [[1,1,1,0,0,1,2,0], [1,1,1,1,0,2,1,0], [1,1,1,3,5,6,1,0], [1,1,1,2,0,2,3,0],
  [1,1,1,3,0,0,3,1],[1,1,1,4,0,1,1,1],[1,1,1,1,2,3,3,1],[1,1,1,3,2,0,1,1],
  [0,0,0,4,3,3,2,2],[0,0,0,4,0,5,0,2],[0,0,0,3,3,3,0,2],[0,0,0,3,4,6,2,2],
  [0,0,0,3,2,3,0,3],[0,0,0,4,0,5,2,3],[0,0,0,3,0,3,0,3],[0,0,0,4,2,5,2,3],
  [0,0,0,2,4,5,0,4],[0,0,0,1,2,0,0,4],[0,0,0,1,5,3,0,4],[0,0,0,4,4,2,2,4],
  [0,0,0,0,4,0,0,5],[0,0,0,0,5,3,0,5],[0,0,0,2,3,3,2,5],[0,0,0,3,3,5,0,5],
  [0,1,1,1,1,1,0,6],[0,1,1,1,2,4,3,6],[0,1,1,0,3,5,2,6],[0,1,1,0,3,1,1,6],
  [1,1,0,5,1,4,0,7],[1,1,0,5,3,2,2,7],[1,1,0,5,1,3,0,7],[1,1,0,6,1,5,0,7],
  [0,0,1,1,0,5,0,8],[0,0,1,1,3,1,1,8],[0,0,1,1,2,5,3,8],[0,0,1,2,0,3,3,8],
  [0,0,0,0,3,4,0,9],[0,0,0,2,3,4,2,9],[0,0,0,0,5,4,2,9],[0,0,0,2,0,5,0,9]]

  test_set = [[0,0,0,7,0,3,0,3], [0,0,0,4,2,3,0,3], [1,1,1,0,0,2,3,0], [1,1,1,3,0,0,3,1],
  [0,0,0,1,5,5,0,4], [0,1,1,1,3,3,2,6]]
  
  questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

  #create the tree on this dataset
  create_tree = decisiontree.create_Tree(train_set, 1, questions, question_to_index, question_to_yes_answers)

  #test the test set
  percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
  print("percent correct is " + str(percent))
  print("wrong tests are " + str(wrong))
  print()

#expanding first dataset with 50% more entries
#67% correct
def secondTraining():
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
  train_set = [[1,1,1,0,0,1,2,0], [1,1,1,1,0,2,1,0], [1,1,1,3,5,6,1,0], [1,1,1,2,0,2,3,0],
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
  [0,0,0,2,1,0,0,9], [0,0,0,2,4,4,0,9]]

  test_set = [[0,0,0,7,0,3,0,3], [0,0,0,4,2,3,0,3], [1,1,1,0,0,2,3,0], [1,1,1,3,0,0,3,1],
  [0,0,0,1,5,5,0,4], [0,1,1,1,3,3,2,6],  ]
  
  questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

  create_tree = decisiontree.create_Tree(train_set, 1, questions, question_to_index, question_to_yes_answers)

  #test the test set
  percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
  print("percent correct is " + str(percent))
  print("wrong tests are " + str(wrong))


def thirdTraining():
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
  train_set = [[1,1,1,0,0,1,2,0,0,1,0,0], [1,1,1,1,0,2,1,0,0,1,0,0], [1,1,1,3,5,6,1,2,0,1,0,0], [1,1,1,2,0,2,3,0,0,1,0,0],
  [1,1,1,0,0,2,3,0,0,1,0,0],[1,1,1,0,1,1,2,0,1,0,0],
  [1,1,1,3,0,0,3,0,0,1,0,1],[1,1,1,4,0,1,1,2,0,1,0,1],[1,1,1,1,2,3,3,0,2,1,0,1],[1,1,1,3,2,0,1,4,2,1,0,1],
  [0,1,1,3,0,1,2,4,0,1,0,1],[0,1,1,1,2,5,3,0,0,1,0,1],
  [0,0,0,4,3,3,2,0,2,0,0,2],[0,0,0,4,0,5,0,0,2,0,0,2],[0,0,0,3,3,3,0,0,0,0,0,2],[0,0,0,3,4,6,2,0,2,0,1,2],
  [0,0,0,4,3,3,0,4,0,0,1,2], [0,0,0,4,0,5,0,4,0,0,1,2],
  [0,0,0,3,2,3,0,4,0,0,0,3],[0,0,0,4,0,5,2,0,0,0,0,3],[0,0,0,3,0,3,0,4,0,0,0,3],[0,0,0,4,2,5,2,0,0,0,0,3],
  [0,0,0,3,2,3,2,0,0,0,0,3],[0,0,0,4,0,3,0,0,0,0,0,3],
  [0,0,0,2,4,5,0,2,2,0,1,4],[0,0,0,1,2,0,0,2,2,1,1,4],[0,0,0,1,5,3,0,2,2,1,1,4],[0,0,0,4,4,2,2,3,2,0,1,4],
  [0,0,0,1,4,4,0,2,2,1,1,4], [0,0,0,1,5,5,0,2,0,1,0,4],
  [0,0,0,0,4,0,0,3,2,0,0,5],[0,0,0,0,5,3,0,3,2,0,0,5],[0,0,0,2,3,3,2,2,2,1,0,5],[0,0,0,3,3,5,0,3,2,0,1,5],
  [0,0,0,3,5,0,0,1,2,0,0,5], [0,0,0,3,4,2,0,2,0,1,1,5], 
  [0,1,1,1,1,1,0,4,0,1,0,6],[0,1,1,1,2,4,3,4,0,1,0,6],[0,1,1,0,3,5,2,1,0,1,0,6],[0,1,1,0,3,1,1,2,0,1,0,6],
  [1,1,1,1,3,3,2,4,0,1,0,6],[1,1,1,3,1,4,2,4,0,1,0,6],
  [1,1,0,5,1,4,0,2,0,1,0,7],[1,1,0,5,3,2,2,2,0,1,0,7],[1,1,0,5,1,3,0,2,2,1,0,7],[1,1,0,6,1,5,0,2,2,1,0,7],
  [1,1,0,5,3,3,0,2,0,1,0,7],[1,1,0,5,1,3,0,3,0,1,0,7],
  [0,0,1,1,0,5,0,1,0,1,0,8],[0,0,1,1,3,1,1,1,2,1,0,8],[0,0,1,1,2,5,3,1,0,1,0,8],[0,0,1,2,0,3,3,1,2,0,0,8],
  [0,0,1,1,2,3,0,3,2,0,0,8], [0,0,1,1,3,3,0,3,2,1,0,8],
  [0,0,0,0,3,4,0,2,1,1,0,9],[0,0,0,2,3,4,2,2,1,1,1,9],[0,0,0,0,5,4,2,2,2,0,0,9],[0,0,0,2,0,5,0,2,2,0,1,9],
  [0,0,0,2,1,0,0,1,2,1,1,9], [0,0,0,2,4,4,0,2,0,0,0,9]]

  test_set = [[1,1,1,0,0,1,3,0,0,1,0,0],[1,0,1,3,2,5,2,4,0,1,0,1],[0,0,1,4,3,6,0,0,2,0,1,2],[0,0,0,4,4,6,0,0,2,0,0,3],
  [1,0,0,2,5,0,0,2,2,1,1,4],[1,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,0,1,5,1,4,0,2,0,1,0,7],
  [1,0,1,1,0,1,0,1,2,1,0,8],[1,0,0,2,5,4,0,2,1,1,1,9],
  [1,1,1,0,0,2,3,0,0,1,0,0],[1,0,1,3,2,5,2,4,0,1,0,1],[0,0,1,4,3,6,0,0,2,0,1,2],[0,0,0,4,4,6,0,0,2,0,0,3],
  [0,0,0,1,5,3,0,2,2,1,1,4],[1,0,0,1,4,5,0,3,2,0,0,5],[1,1,1,2,3,5,2,0,1,0,6],[1,1,0,5,3,2,2,2,0,1,0,7],
  [1,0,1,1,0,1,0,1,2,1,0,8],[0,0,0,2,4,4,0,2,0,0,0,9]]
  
  questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]

  create_tree = decisiontree.create_Tree(train_set, 1, questions, question_to_index, question_to_yes_answers)

  #test the test set
  percent, wrong = testSet(create_tree, test_set, question_to_yes_answers, question_to_index)
  print("percent correct is " + str(percent))
  print("wrong tests are " + str(wrong))



if __name__ == '__main__':
  firstTraining()
  secondTraining()
  thirdTraining()



