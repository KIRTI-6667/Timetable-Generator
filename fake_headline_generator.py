
# 1- immport the random module
import random

# 2- create subjects
subjects = [
    "A cat",
    "An elephant",
    "A lion",
    "A baby",
    "A group of monkeys",
    "A potato",
    "Varun"
]

actions = [ 
    "rides the bike",
    "run in the marthon",
    "is great actor",
    "beautiful",
    "eats banana",
    "dances with",
    "orders food"
]

places_or_things = [
    "at Mumbai",
    "in Mumabi Local Train",
    "at Ganga Ghat",
    "at India Gate",
    "during IPL Match",
    "at Red Fort",
    "a plate of samosa"
]

# 3- start the headline generation loop
while True:
    subject = random.choice(subjects)
    action = random.choice(actions)
    place_or_thing = random.choice(places_or_things)

    headline = f" BREAKING NEWS: {subject} {action} {place_or_thing} "
    print("\n" + headline)

    user_input = input("\n Do you want another headline? (yes/no)".strip())
    if user_input == "no":
        break

# 4- print goodbye message
print("\n Thanks for using the Fake News Headline Generator. Have a fun day")