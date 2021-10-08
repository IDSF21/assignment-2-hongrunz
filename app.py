import streamlit as st
import sqlite3
import seaborn as sns
import numpy as np

con = sqlite3.connect("database.sqlite")
cur = con.cursor()

sns.set_theme()

st.set_option('deprecation.showPyplotGlobalUse', False)

# TODO: change layout
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("Pitchfork Reviews from Jan 5, 1999 to Jan 8, 2017")

with row1_2:
    st.write("Examining how music review scores vary across genres and across years")

row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))

with row2_1:
    # TODO: Add different genres to the same plot with different hues
    option = st.selectbox(
      "What genre would you like to see?",
      ("rap", "electronic", "rock", "experimental", "metal", "jazz", "pop/r&b", "folk/country", "")
    )
    x = []
    query = "SELECT score FROM reviews INNER JOIN genres ON reviews.reviewid = genres.reviewid WHERE genre IS \"" + option + "\";"
    for row in cur.execute(query):
      x.append(float(row[0]))

    ax = sns.histplot(x)
    st.pyplot()

# TODO: Add different years

# TODO: Add artist search/timeline

con.close()