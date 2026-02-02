import re
import json
import os
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from random_username.generate import generate_username


# =========================
# NLTK DOWNLOADS
# =========================
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)
nltk.download('omw-1.4', quiet=True)


# =========================
# INITIALIZATIONS
# =========================
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
    file_path = "files/article.txt"

    if not os.path.exists(file_path):
        raise FileNotFoundError("files/article.txt was not found.")

    with open(file_path, "r", encoding="utf-8") as f:
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
    return posToWordnetTag.get(posFirstChar, 'n')


def cleanseWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = r"[^a-zA-Z-+]"

    for word, pos in posTaggedWordTuples:
        cleanedWord = word.replace(".", "").lower()

        if (
            not re.search(invalidWordPattern, cleanedWord)
            and len(cleanedWord) > 1
            and cleanedWord not in stopWords
        ):
            lemma = wordLemmatizer.lemmatize(
                cleanedWord,
                treebankPosToWordnetPos(pos)
            )
            cleansedWords.append(lemma)

    return cleansedWords


# =========================
# MAIN ANALYSIS
# =========================
def analyzeText(TextToAnalyze, username):
    articleSentences = tokenizeSentences(TextToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    # Sentence analytics
    stockSearchPattern = r"\b([0-9]+|[%$€£]|thousand|million|billion|trillion|profit|loss)\b"
    keySentences = extractKeySentences(articleSentences, stockSearchPattern)
    wordsPerSentence = getWordsPerSentence(articleSentences)

    # POS tagging and cleansing
    wordsPosTagged = nltk.pos_tag(articleWords)
    articleWordsCleansed = cleanseWordList(wordsPosTagged)

    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)

    # Generate word cloud
    wordCloudFilePath = "results/wordcloud.png"
    wordcloud = WordCloud(
        width=1000,
        height=700,
        background_color="white",
        colormap="Set3",
        collocations=False
    ).generate(" ".join(articleWordsCleansed))

    wordcloud.to_file(wordCloudFilePath)

    # Sentiment analysis
    sentimentResult = sentimentAnalyzer.polarity_scores(TextToAnalyze)

    # Final result
    finalResult = {
        "username": username,
        "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "wordCloudPath": wordCloudFilePath,
            "sentimentAnalysis": sentimentResult,
        },
        "metadata": {
            "sentencesAnalyzed": len(articleSentences),
            "wordsAnalyzed": len(articleWordsCleansed),
        }
    }

    return finalResult


# =========================
# PROGRAM ENTRY
# =========================
def runAsFile():
    welcomeUser()
    username = getUserName()
    greetUser(username)

    articleTextRaw = getArticleText()
    result = analyzeText(articleTextRaw, username)

    print("\nAnalysis Result:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    runAsFile()
