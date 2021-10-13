import streamlit as st
import sqlite3
import pandas as pd
import plotly.figure_factory as ff
from plotly.offline import iplot
import plotly.graph_objs as go
import numpy as np

st.set_page_config(layout="wide")

st.image('https://cdn.pitchfork.com/assets/misc/hp-og-image.jpg')

@st.cache(allow_output_mutation=True)
def get_con():
  return sqlite3.connect("database.sqlite", check_same_thread=False)

con = get_con()
cur = con.cursor()

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Pitchfork Reviews from Jan 5, 1999 to Jan 8, 2017")
st.subheader("Examining how music review scores vary across genres and across years.")
st.write(
  """
  ##

  Have you ever heard someone say \"Music was better back then\"?

  As someone who really enjoys listening to contemporary popular music, I decided to dive into a dataset
  containing 22.7k reviews on music from 2000 to 2017 featured in the music music-centric online magazine.

  To satisfy my own curiosity, I analyzed the dataset to explore the following questions

  1. Are we as music consumers more critical to certain genres than others?
  2. Do we generally view music from the past as better than those released relatively recently?
  3. How are my personal favorite musicians perceived by the general public? Are their music considered good by reviewers? Do review scores for these artists improve over time or go down?
  """)

st.image('https://cdn.shopify.com/s/files/1/0846/7942/files/JST_blogImages_difficultGenres_01.jpg?v=1550261261')


st.markdown('***')



# Part I genre score distplot
st.header('Part I. Do music reviewers tend to give higher scores for certain genres?')
st.markdown("**To begin with, let's see if there are certain genres that generally receive higher scores than others.**")
st.markdown("**What genre would you like to see? Use the multislector below to compare different score distribution across genres.**")
genres = st.multiselect(
  "",
  ("rap", "electronic", "rock", "experimental", "metal", "jazz", "pop/r&b", "folk/country", "global"),
  ["electronic"]
)
scores = []
for g in genres:
  query = "SELECT score FROM reviews INNER JOIN genres ON reviews.reviewid = genres.reviewid WHERE genre IS \"" + g + "\";"
  genre_scores = []
  for row in cur.execute(query):
    genre_scores.append(row[0])
  scores.append(genre_scores)
fig = ff.create_distplot(scores, genres, bin_size=.2)
fig.update_layout(width=800, height=600)
st.plotly_chart(fig)


st.markdown('***')


# Part II Add different years

st.header('Part II. Are we becoming more or less critical towards music?')
st.markdown("**Even though the dataset only contains music reviews from 2000 to 2017, the music that these reviews are evaluating range from the 1960s to 2016. Select a year by sliding the slider to see the density plot for the music made in a specific year. Slide across the slider to see how the density plot evolves across the years.**")
year = st.slider("", 1960, 2016)
query = "SELECT year, score FROM reviews INNER JOIN years ON reviews.reviewid = years.reviewid WHERE year IS \"" + str(year) + "\";"
years = []
scores = []
for row in cur.execute(query):
  years.append(row[0])
  scores.append(row[1])
year_fig = ff.create_2d_density(years, scores)
year_fig.update_layout(width=700, height=700)
st.plotly_chart(year_fig)



st.markdown('***')


# Part III. Add artist search
st.header('Part III. What are the scores given to your favorite artists?')
st.markdown("**Now, try to search for a specific artist by putting their name into the search bar below. Hit enter to see a scatter plot of the scores that this artist receives across the years. Are they getting better scores or lower scores?**")
st.markdown("**In addition, scroll down to see the individual reviews given to your favorite artist.**")
artist = st.text_input('', value="the beatles").lower()



query = "SELECT score, year, title FROM reviews INNER JOIN years ON reviews.reviewid = years.reviewid WHERE artist IS \"" + str(artist) + "\";"

st.write("")

years = []
scores = []
titles = []
for row in cur.execute(query):
  years.append(row[1])
  scores.append(row[0])
  titles.append(row[2])
data = [go.Scatter(x = years, y = scores, mode='markers', text = titles)]

title = '**Hover over each data point to see what album each score is for**'
st.markdown(title)

layout = dict(
  xaxis = dict(title = 'year', ticklen = 5, zeroline=False),
  yaxis = dict(title = 'score', ticklen = 5, zeroline=False),
  width = 800,
  height = 600
)
fig = dict(data = data, layout = layout)
st.plotly_chart(fig)



c1, c2, c3 = st.columns((3))
cols = [c1, c2, c3]

count = 0

query = "SELECT title, score, url, content FROM reviews INNER JOIN content ON reviews.reviewid = content.reviewid WHERE artist IS \"" + str(artist) + "\";"

result = cur.execute(query)

for row in result:
  with cols[count % 3]:
    st.title(row[1])
    st.subheader(row[0])
    st.write(row[2])
    text = row[3]
    if len(text) > 500:
      text = text[:500] + "..."
    st.write(text)
    count +=1

if count == 0:
  str = "Sorry, there is no available data for " + artist
  st.write(str)

