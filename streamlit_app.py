import streamlit as st

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe)
if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
    
    #st.write(ingredients_string)
    
    
    import requests
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    #st.text(smoothiefroot_response).json()
    sf_df = st.dataframe(data = smoothiefroot_response.json(), user_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

# New section to display
