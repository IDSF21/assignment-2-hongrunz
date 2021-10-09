## Description

Have you ever heard someone say \"Music was better back then\"?

As someone who really enjoys listening to contemporary popular music, I decided to dive into a dataset
containing 22.7k reviews on music from 2000 to 2017 featured in the music music-centric online magazine.
To satisfy my own curiosity, I analyzed the dataset to explore the following questions:

- Are we as music consumers more critical to certain genres than others?
- Do we generally view music from the past as better than those released relatively recently?
- How are my personal favorite musicians perceived by the general public? Are their music considered good by reviewers? Do review scores for these artists improve over time or go down?

## Rationale

I used different visual encodings and interactions for the three parts of my project.

####Part I focuses on the relationship between genres and scores.
**Visual encoding**: I used a distribution plot to represent the score distributions and used different hues to represent different genres. I consider the distribution plot is a good format because it shows the percentage of scores in each bucket neatly and provides insight on the averages, max/min values as well as distribution.
**Interaction**: I used a multi-selector to enable the users to pass in only the genres that they are interested, instead of overlaying all the data for all the genres. This has two benefits -- it increases user engagement, and it keeps the chart from getting too crowded.

####2. Part II explores the relationship between years and scores.
**Visual encoding**: The selected visual encoding is a 2d density plot. This is especially helpful to identify how scores are distributed across the years. Initially, I used a distplot, but I found that the 2d density plot works better because it is more simplistic and it captures the characteristics of the data better, e.g. it better shows that it's less common to see really high/low scores as the years progresses.
**Interaction**: A slider is in place to let the user explore the score distribution for each year. I initially wanted to use a range selector, but decided that a discrete slider across the different years is simpler and might take off some cognitive load on the users' side.

####3. Part III explores a particular artist.
**Visual encoding**: I used a scatter plot to represent [score, year] data of a particular artist. This is an intuitive choice as the goal here is to show the progression of the scores across the years.
**Interaction**: I utilized the function to display the title of this data point upon hovering. This is really great when a user sees a particular data point and wants to know which work maps to this data point. 
Additionally, I implemented a search function using a search bar to print out all the reviews available for the particular artist. I think this might be of interest to the user, since the user searched for this artist, they probably have a great interest in all the details. 

## Development Process

This is a solo project. I spent around 6 hours developing this application.
Around .5 hour is spent on researching how to run sqlite3 queries on sqlite3 datasets in streamlit.
Around .5 hour is spent on researching the different plots available.
Around 5 hours are spent coding up the application.