import streamlit
import pandas as pd
import requests
import snowflake.connector

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

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Load data to df
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display df
streamlit.dataframe(fruityvice_normalized)

# Connector data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit list:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like add?')
streamlit.write(my_cur.execute("INSERT INTO fruit_load_list (FRUIT_NAME) VALUES ({});".format(add_my_fruit)))
