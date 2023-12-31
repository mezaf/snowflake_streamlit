
import streamlit
import pandas as pd

streamlit.title("My Parents New healthy Dinner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruit_list  = (
  pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
  .set_index("Fruit")
)

fruits_selected = streamlit.multiselect("Pick some fruits: ", list(fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)

fruit_choice = None
fruit_choice = streamlit.text_input('What fruit would you like to add')
try:
  if fruit_choice:
    my_cur.execute(f"insert into fruit_load_list values ('{fruit_choice}')")
    my_cur.execute("commit")
except Exception as e:
  raise e
streamlit.write(f'Thanks for adding ', fruit_choice)
