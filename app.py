import streamlit as st
import sqlite3
import pandas as pd
import plotly.figure_factory as ff
from plotly.offline import iplot
import plotly.graph_objs as go
import numpy as np

con = sqlite3.connect("database.sqlite")
cur = con.cursor()

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Pitchfork Reviews from Jan 5, 1999 to Jan 8, 2017")
st.write("**Examining how music review scores vary across genres and across years**")

# Part I genre score distplot
st.header('Part I. Do music reviewers tend to give higher scores for certain genres?')
genres = st.multiselect(
  "What genre would you like to see? Use the multislector below to compare different score distribution across genres",
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
fig.update_layout(width=1000, height=800)
st.plotly_chart(fig)

# Part II Add different years
st.header('Part II. Are we becoming more or less critical towards music?')
year = st.slider("Select a year by sliding the slider", 1960, 2016)
query = "SELECT year, score FROM reviews INNER JOIN years ON reviews.reviewid = years.reviewid WHERE year IS \"" + str(year) + "\";"
years = []
scores = []
for row in cur.execute(query):
  years.append(row[0])
  scores.append(row[1])
year_fig = ff.create_2d_density(years, scores)
year_fig.update_layout(width=1000, height=800)
st.plotly_chart(year_fig)


# Part III. Add artist search
st.header('Part III. What are the scores given to your favorite artists?')
artist = st.text_input('Enter an artist', value="the beatles").lower()




query = "SELECT title, score, url, content FROM reviews INNER JOIN content ON reviews.reviewid = content.reviewid WHERE artist IS \"" + str(artist) + "\";"


c1, c2, c3 = st.columns((3))
cols = [c1, c2, c3]

count = 0

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

title = '**scores for '+artist+': hover over each data point to see what album each score is for**'
st.write(title)

layout = dict(
  title = "",
  xaxis = dict(title = 'year', ticklen = 5, zeroline=False),
  yaxis = dict(title = 'score', ticklen = 5, zeroline=False),
)
fig = dict(data = data, layout = layout)
st.plotly_chart(fig)

con.close()