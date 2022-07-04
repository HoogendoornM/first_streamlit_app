import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError 

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


def get_fruit_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
    # Load data to df
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


try: 
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please input a fruit")
    else:
        streamlit.write('The user entered ', fruit_choice)
        output = get_fruit_data(fruit_choice)
        # display df
        streamlit.dataframe(output)
        

except URLError as e:
    streamlit.error()

# Snowflake connection data
streamlit.header("Snowflake fruit data")

# Retrieve data function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()


# Button to trigger data retrieval
if streamlit.button("Get fruit data"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


# Insert data
def insert_row_snowflake(fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list (FRUIT_NAME) VALUES ('{}');".format(fruit))
        return "Added: " + fruit

add_my_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button("Input new fruit name"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    resp = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(resp)
