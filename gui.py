import decisiontree
import tkinter as tk
from functools import partial

#information for the decision tree (dataset and helper functions)
#taken from one of the evaluation.py datasets for now
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
[0,0,0,2,1,0,0,9], [0,0,0,2,4,4,0,9]]

questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

tree = create_tree = decisiontree.create_Tree(dataset, 1, questions, question_to_index, question_to_yes_answers)

#trying the gui (not working yet)
window = tk.Tk()
start_message = tk.Label(master = window, text = "Welcome! The game will start shortly")
start_message.pack()

def getResult(node):
  print(node.num)
  global start_message
  if node.yes == None and node.no == None:
    city_result = city_to_num[node.num]
    start_message.configure(text = "You should move to " + city_result + "!")
  global tree
  tree = node 
  question_num = node.num
  question = questions_to_num[question_num]
  start_message.configure(text = question)

question = questions_to_num[tree.num]
start_message.configure(text = question)
yes_button = tk.Button(master = window, text = "Yes", command = partial(getResult, tree.yes))
yes_button.pack()
no_button = tk.Button(master = window, text = "No", command = partial(getResult, tree.no))
no_button.pack()

window.mainloop()

"""
#make the buttons
question_frame = tk.Frame(master=window, height=150, bg="red")
answer_frame = tk.Frame(master=window,height=25,bg="blue")
yes_button = tk.Button(master = answer_frame, text = "Yes")
no_button = tk.Button(master = answer_frame, text = "No")
yes_button.grid(row=0, column=0)
no_button.grid(row=0, column=1)
"""