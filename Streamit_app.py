# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

title = st.text_input("**write a name**")
#st.write("The current movie title is", title)


st.write(
    """**choose the fruit to customize your smoothie!**
    """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


Ingredients_list = st.multiselect("choose upto 5 ingrediants :"
                                  ,my_dataframe
                                  ,max_selections = 5)

if Ingredients_list:
    #st.write(Ingredients_list)
    #st.text(Ingredients_list)
    
    
    ingredients_string = ' '

    for fruit in Ingredients_list:
        ingredients_string += fruit +' '
    #st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
                   VALUES ('{}', '{}')""".format(ingredients_string, title)

   # st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
