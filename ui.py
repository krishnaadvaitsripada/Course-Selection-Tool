import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Interactive Course Builder', page_icon='📊')
st.title('📊 Interactive Course Builder')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This application helps ease the process of planning university courses by selecting the most suitable courses based on your academic/career goals in IT.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, simply select your IT area(s) of interest from the available options.')

st.subheader('What will your university courses look like?')


# Genres selection
# Input widgets
## Genres selection
default_genres = ['Software Development', 'Artificial Intelligence/Machine Learning', 'Cybersecurity', 'Business', 'Robotics', 'Data Science', 'Networks and Telecommunications', 'Cloud Computing']
genres_selection = st.multiselect('Select your area of interest', default_genres, default_genres)
## Year selection
year_selection = st.slider('Select year duration', 1986, 2006, (2000, 2016))
year_selection_list = list(np.arange(year_selection[0], year_selection[1] + 1))

# Dummy DataFrame to simulate data
# You can replace this with your actual data if needed
df = pd.DataFrame({
    'year': np.random.randint(1986, 2006, size=100),
    'genre': np.random.choice(default_genres, size=100),
    'gross': np.random.randint(10000, 1000000, size=100)
})

df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)

# Display DataFrame
df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                           column_config={"year": st.column_config.TextColumn("Year")},
                           num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
    x=alt.X('year:N', title='Year'),
    y=alt.Y('gross:Q', title='Gross earnings ($)'),
    color='genre:N'
).properties(height=320)
st.altair_chart(chart, use_container_width=True)
