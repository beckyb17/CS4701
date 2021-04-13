#gets the user's answer for each question and stores in the "answers" list
def get_input(qo_dic):
  answers = []
  for key in qo_dic:
    print(key)
    print("Your options are:")
    for val in qo_dic[key]:
      print(val)
    response = input("Enter your answer >>>")
    answers.append(response.lower())
  return answers

def main():
  #questions to ask the user
  q1 = "What is your ideal city size?"
  q2 = "What is your ideal city's population density?"
  q3 = "How important is a low cost of living? '1' is not important, '2' is somewhat important, and '3' is very important."
  q4 = "What industry are you most interested in?"
  q5 = "What is your preferred mode of transportation?"
  q6 = "How much nightlife are you looking for? Please rank from the options below. '1' is little to none and '5' is a lot."
  q7 = "What is your favorite food?"
  q8 = "What is your favorite dessert?"
  q9 = "What is your favorite daytime activity?"
  q10 = "What is your favorite nighttime activity?"

  #options for each question
  size = ["Big", "Medium", "Small"]
  cost = ["1", "2", "3"]
  industries = ["Finance", "Tech", "Business", "Theatre", "Medicine", "Education", 
  "Research", "Entertainment", "Music"]
  transportation = ["Subway", "Uber", "Bus", "Walk", "Cable car", "Bike"]
  nightlife = ["1", "2", "3", "4", "5"]
  foods = ["Bagels", "Pasta", "Pizza", "Pretzels", "Clam chowder", "Sandwiches", 
  "Lobster", "Burgers", "Maple syrup", "Fried chicken", "Queso", "Burritos", "Fries"
  "Tacos", "Seafood", "Salads", "Avocados", "Pho", "Coffee", "Empanadas"]
  desserts = ["Cheesecake", "Italian ice", "Cookie dough", "Ice cream", "Cannoli", 
  "Cupcake", "Crepe", "Hot chocolate", "Pecan pie", "Cake", "Custard", "Fruit parfait",
  "Chocolate"]
  day = ["Visit a museum", "Shopping spree", "Watch a sports game", "Go sight-seeing", 
  "Boating", "Have a picnic","Go on a hike", "Skiing", "Swimming", "Visit a beach",
  "Visit an amusement park"]
  night = ["Go to a bar", "Go clubbing", "Watch a Broadway show", "Sleep", "Visit a brewery", 
  "Watch a movie", "Have a bonfire", "Go to a concert"]

  #add questions and options to the q_o dic
  q_o = {}
  q_o[q1] = size
  q_o[q2] = size
  q_o[q3] = cost
  q_o[q4] = industries
  q_o[q5] = transportation
  q_o[q6] = nightlife
  q_o[q7] = foods
  q_o[q8] = desserts
  q_o[q9] = day
  q_o[q10] = night
    
  responses = get_input(q_o)
  print(responses)

if __name__ == "__main__":
  main()

