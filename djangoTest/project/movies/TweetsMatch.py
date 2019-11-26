import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk import FreqDist
import pickle
from movies.TwitterApiRelated import oauth_login, GetTweetsInList
MAX_DIST = 200



class Matcher:
    def __init__(self):
        self.twitter_api = oauth_login()
        with open('movies/tweets_data/top-words.pkl', 'rb') as f:
            self.topWords = pickle.load(f)
        with open('movies/tweets_data/id-to-movies.pkl', 'rb') as f:
            self.idToMoviesDict = pickle.load(f)
        with open('movies/tweets_data/user-vector.pkl', 'rb') as f:
            self.userVecs = pickle.load(f)
    def GetDist(self, vec1, vec2):
        dist = 0
        for i in range(len(vec1)):
            if vec1[i] != vec2[i]:
                dist += 1
        return dist

    def ComputeVector(self, content, topWords):
        ''' get feature vector for input content
            - content: input string
            - topWords: the vocabulary list
            Returns feature vector as a list
        '''
        result = []
        currentWordSet = self.GetAllWords(content)
        for word, _ in topWords:
            if word in currentWordSet:
                result.append(1)
            else:
                result.append(0)
        return result

    def GetAllWords(self, content):
        ''' get all words appear in content
            - content: input string
            - Returns a set of all words
        '''
        rawTokens = nltk.word_tokenize(content)

        alphabeticalTokens = [w for w in rawTokens if w.isalpha()]
        del rawTokens
        lowerTokens = [w.lower() for w in alphabeticalTokens]
        del alphabeticalTokens
        stopwords = nltk.corpus.stopwords.words('english')
        tokens = [w for w in lowerTokens if w not in stopwords]

        del lowerTokens
        del stopwords

        lemmatizer = nltk.WordNetLemmatizer()
        lemmatizedTokens = [lemmatizer.lemmatize(t) for t in tokens]

        tokenDist = FreqDist(lemmatizedTokens)
        allWords = set(tokenDist.keys())
        if allWords == None:
            return set()
        return allWords

    def TopKMatch(self, vec0, userVecs, K):
        ''' return list of K most similar users' internal IDs of top matches
            - vec0: new user's feature vector
            - userVecs: dict of all archived users' feature vectors
            - Returns list of users' internal IDs of top matches
            (Warning: non-scalable)
        '''
        result = []
        idDistPairList = []
        for idString in userVecs:
            currentDist = self.GetDist(vec0, userVecs[idString])
            idDistPairList.append((idString, currentDist))
        sorted(idDistPairList, key = lambda p : p[1])
        K = min(K, len(userVecs))
        for i in range(K):
            result.append(idDistPairList[i][1])
        return result

    def GetTweets(self, twitterId):
        ''' return all (or most recent 200) tweets of specified user
            - twitterId : external twitter ID (in str)
            - Returns all tweets in str
        '''
        if twitterId == '0':
            return 'dummy message for testing tweets based recommendation'
        tweetsList = GetTweetsInList(self.twitter_api, twitterId)
        content = ''
        for tw in tweetsList:
            content += tw['text'] + ' \n '
        return content
        

    def FindKSimilar(self, twitterId, K=3):
        content = self.GetTweets(twitterId)
        vec0 = self.ComputeVector(content, self.topWords)
        idList = self.TopKMatch(vec0, self.userVecs, K)
        return idList

    def RecommendFromIds(self, idList):
        result = []
        for id in idList:
            idStr = str(id)
            for movie in self.idToMoviesDict[idStr]:
                result.append(movie)
        return result
    
    def GetRecommendation(self, twitterId):
        if len(twitterId) == 0 or not twitterId.isdigit():
            return []
        idList = self.FindKSimilar(twitterId)
        result = self.RecommendFromIds(idList)
        return result

if __name__ == "__main__":
    matcher = Matcher()
    twitterId = "1299745795"
    # tweetsBasedRecommendation = matcher.GetRecommendation(twitterId)
    # tempFile = open("tempFile.pkl", "wb")
    # pickle.dump(tweetsBasedRecommendation, tempFile)
    print(matcher.GetTweets(twitterId))
