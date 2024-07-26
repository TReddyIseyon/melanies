# Import python packages

import streamlit as st

from snowflake.snowpark.functions import col

st.title("My Parents new healthy diet")
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie !
    """
)
name_on_order=st.text_input("Name on the smoothie:")
st.write('The name on your smoothie will be:',name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#


ingredients_list = st.multiselect(
    "Choose upto five ingridients:",
    my_dataframe , max_selections=5 )
if ingredients_list:
  
  ingredients_string=''  
  for fruit_chosen in ingredients_list:
      ingredients_string+=fruit_chosen + ' '
  st.write(ingredients_string)    
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
  
  #st.write(my_insert_stmt)
  if ingredients_string:
      
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")



my_dataframe2 = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe2)
submitted=st.button('Submit Order')

if submitted:
    
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
         og_dataset.merge(edited_dataset
                     , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
         st.success('Your Smoothie is ordered!', icon="✅")
    except:
        st.write("Something went Wrong")


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
