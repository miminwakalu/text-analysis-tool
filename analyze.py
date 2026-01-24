import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from random_username.generate import generate_username

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
nltk.download('omw-1.4')

# Initialize lemmatizer
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()


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
        prompt = "\nTo get started, please enter your name:\n" if attempts == 0 else "\nPlease try again:\n"
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
posToWordnetTag = {
    'J': 'a',  # adjective
    'V': 'v',  # verb
    'N': 'n',  # noun
    'R': 'r'   # adverb
}

def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    return 'n'  # default to noun

def cleanseWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = r"[^a-zA-Z-+]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleanedWord = word.replace(".", "").lower()
        if not re.search(invalidWordPattern, cleanedWord) and len(cleanedWord) > 1 and cleanedWord not in stopWords:
            lemma = wordLemmatizer.lemmatize(cleanedWord, treebankPosToWordnetPos(pos))
            cleansedWords.append(lemma)
    return cleansedWords

# =========================
# MAIN EXECUTION
# =========================

welcomeUser()
username = getUserName()
greetUser(username)

articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Sentence analytics
stockSearchPattern = r"[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# POS tagging and cleansing
wordsPosTagged = nltk.pos_tag(articleWords)
articleWordsCleansed = cleanseWordList(wordsPosTagged)

# Generate word cloud
separator = " "
wordcloud = WordCloud(width = 1000, height = 700, \
                      background_color="white", colormap="Set3", collocations=False).generate(separator.join(articleWordsCleansed))
wordcloud.to_file("results/wordcloud.png")

# Run sentiment analysis
sentimentResult = sentimentAnalyzer.polarity_scores(articleTextRaw)

# =========================
# OUTPUT
# =========================
print(sentimentResult)
