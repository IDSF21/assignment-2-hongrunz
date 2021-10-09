import streamlit as st
import sqlite3
import pandas as pd
import plotly.figure_factory as ff
import numpy as np

con = sqlite3.connect("database.sqlite")
cur = con.cursor()

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Pitchfork Reviews from Jan 5, 1999 to Jan 8, 2017")
st.write("Examining how music review scores vary across genres and across years")

# Part I genre score distplot
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
# score_genres = pd.read_sql_query('SELECT score, genre FROM reviews INNER JOIN genres ON reviews.reviewid = genres.reviewid', con)
fig = ff.create_distplot(scores, genres, bin_size=.2)
fig.update_layout(width=1300, height=800)
st.plotly_chart(fig)

# TODO: Add different years

# TODO: Add artist search/timeline

con.close()