from decisiontree import TreeNode, questions_to_num, city_to_num

def getResult(node):
  if node.yes == None and node.no == None:
    city_result = city_to_num(node.num)
    return city_result
  question_num = node.num
  user_response = input(questions_to_num[question_num])
  valid = False
  while not valid:
    if user_response.lower() != 'y' or user_response.lower() != 'n':
      user_response = ("Please enter a valid answer. 'y' for yes and 'n' for no. >>")
    else:
      valid = True
  if user_response.lower() == 'y':
    getResult(node.yes)
  else:
    getResult(node.no)


