# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

# Importing modules

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer



# %%

# Assigning data sources to data frames

df1 = pd.read_csv("data/Datafiniti_API.csv")
df2 = pd.read_csv("data/Datafiniti_Hotel_Reviews.csv")
df3 = pd.read_csv("data/Datafiniti_Hotel_Reviews_Update.csv")
df4 = pd.read_csv('data/Hotel_details.csv')
df5 = pd.read_csv('data/hotelSF.csv', encoding = "ISO-8859-1")

# %% [markdown]

# Concatinating Datafiniti data to have single df

df = pd.concat([df1, df2, df3, df4, df5])
df.head()

# %%

# Keeping only the relevant df columns

df = df[['address', 'reviews.rating', 'name', 'reviews.text','city']]

# %% [markdown]

# Dropping the missing values

df = df.dropna(subset=['address', 'reviews.rating', 'reviews.text'])

city_list = df['city'].unique()
city_list = sorted(city_list)
# %% [markdown]

# getting rid of uppercases

df['city'] = df['city'].str.lower()
df['reviews.text'] = df['reviews.text'].str.lower()

# %%

# Updating the column names

df = df.rename(columns={'name': 'Hotel', 'address': 'Address', 'reviews.rating': 'Rating'})

# %% [markdown]

# Building the recommendation system

def recommendation(destination, description):
    description = description.lower()
    
    city = df[df['city']==destination.lower()]
    city = city.set_index('Hotel')
    review = city['reviews.text']
    review['input'] = description
    #print(review)
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2,2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(review)
    
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    #print(cosine_similarities)
    score_series = pd.Series(cosine_similarities[cosine_similarities.shape[0]-1])
    score_series = score_series[:(cosine_similarities.shape[0]-1)]
    city = city.reset_index()
    city['similarity'] = score_series
    
    similarity_list = city.groupby('Hotel')['similarity'].mean()
    city = city.drop('similarity',axis = 1)
    similarity_score = similarity_list.to_frame()
    similarity_score = similarity_score.reset_index()
    rating_list = city.groupby('Hotel')['Rating'].mean()
    city = city.drop('Rating',axis = 1)
    rating_score = rating_list.to_frame()
    rating_score = rating_score.reset_index()
    city = city.merge(similarity_score,on = 'Hotel')
    city = city.merge(rating_score,on = 'Hotel')
    city = city.sort_values(by='similarity', ascending=False)
    city.drop_duplicates(subset='Hotel', keep='first', inplace=True)
    city = city.iloc[:10,:]
    city.sort_values('Rating', ascending=False, inplace=True)
    city.reset_index(inplace=True)
    city['Rating'] = city['Rating'].astype(int)
    return city[["Hotel", "Address", "Rating"]].head()

# %% [markdown]

recommendation('New York', 'Im going to New York for business trip')

# %%
recommendation('Chicago','location is good')
# %%
recommendation('London','I prefer a family hotel')
# %% [markdown]

# %% [markdown]
# Now, let's find books similar to "Algorithms" book based on the description:

# %%