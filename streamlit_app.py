import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe)
if ingredients_list:

    ingredients_string = ''

    
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', each_fruit,' is ', search_on, '.')
        
        st.subheader(each_fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    
    


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")


