import streamlit as st
import requests

# Page title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")


# Get the name for the order
name_on_order = st.text_input("Name on Smoothie")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Get the active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()


# Get fruit options from Snowflake
fruit_query = """
SELECT fruit_name
FROM smoothies.public.fruit_options
"""

fruit_rows = session.sql(fruit_query).collect()

fruit_list = [
    row["FRUIT_NAME"]
    for row in fruit_rows
]


# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)


# Display nutrition information
if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string = (
            ingredients_string + fruit_chosen + " "
        )

        st.subheader(
            fruit_chosen + " Nutrition Information"
        )

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/"
            + fruit_chosen
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )


    # Display selected ingredients
    st.write(ingredients_string)


    # Submit Order button
    time_to_insert = st.button("Submit Order")


    if time_to_insert:

        my_insert_stmt = """
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
        """

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
