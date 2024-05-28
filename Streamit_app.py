# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

title = st.text_input("**write a name**")
#st.write("The current movie title is", title)


st.write(
    """**choose the fruit to customize your smoothie!**
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()


Ingredients_list = st.multiselect("choose upto 5 ingrediants :"
                                  ,my_dataframe
                                  ,max_selections = 5)

if Ingredients_list:
    ingredients_string = ' '

    for fruit in Ingredients_list:
        ingredients_string += fruit +' '
        st.subheader(fruit + ' Neutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        fv_df = st.dataframe(fruityvice_response.json(), use_container_width = True)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
                   VALUES ('{}', '{}')""".format(ingredients_string, title)

   # st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        

        
