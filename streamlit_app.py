import streamlit
import pandas as pd
import requests

streamlit.title('Streamlit tutorial')

streamlit.header('A diner menu')
streamlit.text('🎂 Birthday cake!')
streamlit.text('🍊 Orange')
streamlit.text('🍔 Beefburger')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load fruit CSV
df = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set fruit as index
df = df.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(df.index), ['Apple'])
fruits_to_show = df.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Fruity request
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())

# Load data to df
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display df
streamlit.dataframe(fruityvice_normalized)