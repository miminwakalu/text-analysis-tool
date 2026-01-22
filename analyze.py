import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

text = "Python is amazing"
print(word_tokenize(text))

from random_username.generate import generate_username

# Welcome User
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get username
def getUserName():
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        if attempts == 0:
            inputPrompt = "\nTo get started, please enter your name:\n"
        else:
            inputPrompt = "\nPlease try again:\n"

        usernameFromInput = input(inputPrompt).strip()

        # Validate username
        if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
            print(
                "Your username must be at least 5 characters long, "
                "contain only letters/numbers/underscores, "
                "have no spaces, and not start with a number!"
            )
        else:
            return usernameFromInput

        attempts += 1

    print(f"\nExhausted all {maxAttempts} attempts, assigning username instead...")
    return generate_username()

# Greet the user
def greetUser(name):
    print("Hello, " + name)

# Get text from file
def getArticleText():
    with open("files/article.txt", "r") as f:
        rawText = f.read()
    return rawText.replace("\n", " ").replace("\r", " ")

# Extract sentences from raw text body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

# Extract words from list of sentences
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

# Get the key sentences based on search patter of key words
def extractkeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        # If sentence matches desired pattern, and to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

# Get the average words per sentence, excluding punction
def getWordsPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(""))
    return totalWords / len(sentences)

# Filter raw tokenized words list to only include
# valid english words
def cleanseWordList(words):
    cleansedWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for word in words:
        cleansedWord = word.replace(".", "").lower()
        if not re.search(invalidWordPattern, cleansedWord):
            cleansedWords.append(cleansedWord)
    return cleansedWords

# Get User Details
# welcomeUser()
# username = getUserName()
# greetUser(username)

# Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Get Sentence Analytics
stockSearchPattern = "0-9] | [%$€£] |thousand|million|billion|trillion|profit|loss"
keySentences = extractkeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Get Word Analytics
articleWordsClensed = cleanseWordList(articleWords)

# Print for testing
print("GOT:")
print(articleWordsClensed)

