import streamlit as st
from func_file import *


tk = 0
st.title('Hotel Recommendation System')

col1, col2 = st.columns(2)


# taking destination as input

with col1:
    destination = st.selectbox("Select city : ", city_list)   
        
            
# taking description as input

with col2:
    description = st.text_input('Enter description : ')
    if st.button('Recommend'):
        tk = 1

#st.dataframe(df.head())
if tk == 1:
    st.success('Recommending top 5 hotels in '+destination)
    rec = st.empty()
    rec = st.dataframe(recommendation(destination, description), width=1700, height=500)

#print(get_recommendations())