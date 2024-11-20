# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(" :cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """ 
)

#Adding the order's name
import streamlit as st

name_on_order  = st.text_input("Name on Smoothie", "")
st.write("The name on your Smoothie will be", name_on_order )    


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

ingredients_list=st.multiselect('Choose up to 5 ingredients:'
                               ,my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
     ingredients_string += fruit_chosen + ' '
        
    st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

#st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')

# Si el botón es presionado y hay ingredientes
if time_to_insert:
    if ingredients_string:
        session.sql(my_insert_stmt).collect() 
        st.success('Your Smoothie is ordered!', icon="✅")
    else:
        st.warning('Please select your ingredients before submitting.')  # Aviso si no hay ingredientes
        

st.write(my_insert_stmt)
st.stop()
