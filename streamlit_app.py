import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My Parents New Healthy Diner")
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑Hard-Boiled Free-Range Egg🍞')
   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','watermelon')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

add_my_fruit = streamlit.text_input('What fruit would you like information about?','watermelon')
streamlit.write('The user entered ', add_my_fruit)
try:
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT * FROM fruit_load_list")
    my_data_rows = my_cur.fetchall()

    if my_data_rows:
        streamlit.text("The fruit load list contains:")
        for row in my_data_rows:
            streamlit.text(row)
    else:
        streamlit.text("No data found in fruit_load_list.")

except Exception as e:
    streamlit.error(f"An error occurred: {e}")
