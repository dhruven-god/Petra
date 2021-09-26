
import pandas as pd
import numpy as np
final_df = pd.read_csv("movies.csv")
df_meta = pd.read_csv("test_movies.csv")

final_df = final_df[["title","summary"]]   # Grabbing only required columns


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000,stop_words='english')


df_meta = df_meta.set_index("id")


df_meta[df_meta["title"] == "Aquaman"].index[0]


count_matrix = cv.fit_transform(final_df['summary']).toarray()



from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(count_matrix)


import requests
import requests



def recommend_movie(movie):
    
    try:

        index = final_df[final_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(cosine_sim[index])),reverse=True,key = lambda x: x[1])
        
        myfile = open('recommendations.txt', 'w',encoding="utf-8")
        
        for i in distances[1:16]:
            myfile.write("%s\n" % final_df.iloc[i[0]].title.capitalize())
            
        myfile.close()
                
    except IndexError:


        url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{}".format(movie)

        headers = {
            'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
            'x-rapidapi-key': "a114896f16mshb4a8322f5deb807p1443d6jsn6d197fdd2a80"
            }

        response = requests.request("GET", url, headers=headers)

        imdb_id = response.json()["id"]

        url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"

        querystring = {"tconst":"{}".format(imdb_id),"currentCountry":"US","purchaseCountry":"US"}

        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': "e3b57ed72emsh103d618464887c3p1aeae3jsn26c988347666"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        movies_list = response.json()
        movies_list = [s.replace("/title/", "") for s in movies_list]
        movies_list = [s.replace("/", "") for s in movies_list]
        
        myfile = open('recommendations.txt', 'w',encoding="utf-8")
        
        for i in range(len(movies_list)-10):
            
            url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{}".format(movies_list[i])
            
            headers = {
            'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
            'x-rapidapi-key': "a114896f16mshb4a8322f5deb807p1443d6jsn6d197fdd2a80"
            }
            
            response = requests.request("GET", url, headers=headers)
            
            myfile.write("%s\n" % response.json()["title"])
            
        myfile.close()




import pickle
pickle.dump(final_df,open('movies.pkl','wb'))
pickle.dump(cosine_sim,open('model.pkl','wb'))
