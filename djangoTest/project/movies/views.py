from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
from django.views.decorators.csrf import csrf_exempt

###########################################
# code for movie recommendation system core
###########################################
#############################
### import some dependencies
#############################
import pandas as pd
import numpy as np
import ast 
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD, evaluate
import os

import warnings; warnings.simplefilter('ignore')

#############################
### load dataset
#############################
currentPath = os.path.dirname(__file__)

credits = pd.read_csv(os.path.join(currentPath, 'input_data/movie_dataset/credits.csv'))
keywords = pd.read_csv(os.path.join(currentPath, './input_data/movie_dataset/keywords.csv'))
links_small = pd.read_csv(os.path.join(currentPath, './input_data/movie_dataset/links_small.csv'))
md = pd.read_csv(os.path.join(currentPath, './input_data/movie_dataset/movies_metadata.csv'))
ratings = pd.read_csv(os.path.join(currentPath, './input_data/movie_dataset/ratings_small.csv'))

#############################
### init content based recommender
#############################
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan
md['id'] = md['id'].apply(convert_int)
md[md['id'].isnull()]
md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')
smd = md[md['id'].isin(links_small)]
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])
def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

###########################################
# code for tweets-based recommendation system core
###########################################

from movies.TweetsMatch import Matcher
matcher = Matcher()

###########################################
# code for django views
###########################################
# Create your views here.
def index(request):
    htmlStr = "haha <br/>"
    # try:
    #     data = json.loads(request.body)
    #     name = data["name"]
    #     des = data["des"]
    #     htmlStr += "Name: " + name + "; des: " + des
    # except:
    #     return HttpResponse(500)
    # obj = {"receipt": "#1 receipt"}
    # return HttpResponse(htmlStr)
    # return HttpResponse(htmlStr)
    return render(request, 'index.html')


## home page
def home(request):
    return render(request, 'home.html')

## processing "/api/recommendation/" request
def recommendation(request):
    twitterId = None
    movies = None
    recommendationList = []
    try:
        requestData = json.loads(request.body)
        twitterId = requestData['twitterId'] + ""
        print(twitterId)
        movies = requestData['movies']
        print(movies)
    except:
        return HttpResponse(400)
    for movie in movies:
        try:
            partialResults1 = get_recommendations(movie).head(5).tolist()
            recommendationList += partialResults1
            
        except:
            continue
    rawPartialResults2 = matcher.GetRecommendation(twitterId)
    partialResults2Set = set()
    for k in rawPartialResults2:
        partialResults2Set.add(k)
    partialResults2 = list(partialResults2Set)[:5]
    print("======")
    print(partialResults2)
    print("======")
    recommendationList += partialResults2
    return JsonResponse({'twitterId': twitterId, 'data': recommendationList})

# def some_api(request):
#     resultData = {'msg': 'hello, world!', 'data': '(no data)'}
#     try:
#         data = json.loads(request.body)
#         dataStr = json.dumps(data)
#         resultData['data'] = dataStr
#     except:
#         return JsonResponse(resultData)
#     return JsonResponse(resultData)