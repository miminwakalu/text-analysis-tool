# Welcome User
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get username
def getUserName():
    # Print message prompting user to input their name
    usernameFromInput = input("\nTo get started, please enter your name:\n")
    return usernameFromInput

# Greet the user
def greetUser(name):
    print("Hello, " + name)


welcomeUser()
username = getUserName()
greetUser(username)

