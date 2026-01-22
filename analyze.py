import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from random_username.generate import generate_username
wordLemmatizer = WordNetLemmatizer()

# =========================
# TEST TOKENIZATION
# =========================
text = "Python is amazing"
print(word_tokenize(text))


# =========================
# USER INTERACTION
# =========================

def welcomeUser():
    print(
        "\nWelcome to the text analysis tool. "
        "I will mine and analyze a body of text from a file you give me!"
    )


def getUserName():
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        prompt = (
            "\nTo get started, please enter your name:\n"
            if attempts == 0
            else "\nPlease try again:\n"
        )

        usernameFromInput = input(prompt).strip()

        if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
            print(
                "Your username must be at least 5 characters long, "
                "contain only letters, numbers, or underscores, "
                "have no spaces, and not start with a number!"
            )
        else:
            return usernameFromInput

        attempts += 1

    print(f"\nExhausted all {maxAttempts} attempts, assigning username instead...")
    return generate_username()


def greetUser(name):
    print("Hello, " + name)


# =========================
# FILE HANDLING
# =========================

def getArticleText():
    with open("files/article.txt", "r", encoding="utf-8") as f:
        rawText = f.read()
    return rawText.replace("\n", " ").replace("\r", " ")


# =========================
# TOKENIZATION
# =========================

def tokenizeSentences(rawText):
    return sent_tokenize(rawText)


def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words


# =========================
# SENTENCE ANALYTICS
# =========================

def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences


def getWordsPerSentence(sentences):
    if not sentences:
        return 0

    totalWords = 0
    for sentence in sentences:
        totalWords += len(word_tokenize(sentence))

    return totalWords / len(sentences)


# =========================
# WORD ANALYTICS
# =========================

def cleanseWordList(words):
    cleansedWords = []
    invalidWordPattern = r"[^a-zA-Z-+]"

    for word in words:
        cleaned = word.replace(".", "").lower()
        if not re.search(invalidWordPattern, cleaned) and len(cleaned) > 1:
            cleansedWords.append(wordLemmatizer.lemmatize(cleaned))

    return cleansedWords

# Get user details
welcomeUser()
username = getUserName()
greetUser(username)

articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Regex fixed and cleaned
stockSearchPattern = r"[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"

keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

articleWordsCleansed = cleanseWordList(articleWords)

# =========================
# OUTPUT (TESTING)
# =========================

print("\nGOT:")
print(articleWordsCleansed)
print("\nAverage words per sentence:", wordsPerSentence)
print("\nKey Sentences:")
for sentence in keySentences:
    print("-", sentence)
