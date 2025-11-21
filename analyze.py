# Welcome User
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get username
def getUserName():
    # Print message prompting user to input their name
    usernameFromInput = input("\nTo get started, please enter your name:\n")
    
    if len(usernameFromInput) < 5 or not usernameFromInput.isIdentifier():
        print("Your username must be at least 5 characters long, alphanumeric only(a-z/A-Z/0-9), have no spaces, and cannot start with a number! ")
        print("Assigning username instead...")
        return generate_username() [0]

    return usernameFromInput

# Greet the user
def greetUser(name):
    print("Hello, " + name)

welcomeUser()
username = getUserName()
greetUser(username)

