#installs streamlit
#pip install streamlit
#uv ad streamlit
import streamlit as st
from datetime import datetime, date
import pandas as pd


import random
# ================
#  streamlit basic text and title

st.title("Welcome to our finance app") #run: uv run streamlit run hands-on/date3.py
st.header("This is section to display data")
# st.subheader("This is subheader")
# st.text("This is text")
# st.markdown("**This is bold markdown**")
# st.markdown("*This is italic markdown*")

st.subheader("Display today's date")

category = {
    "type": "Expense",
    "name": "Shopping",
    "amount": 150,
}
st.write("Category details:", category)

st.subheader("Display list")
collections = ['category', 'users', 'budgets']
st.write("Collections:", collections)

# display dataframe
st.subheader("Display dataframe")

data = []
for i in range(10):
    item = {
        "id": i,
        "sex": random.choice(['M', 'F']),
        "age": random.randint(3, 50),
         
    }
    data.append(item)

df = pd.DataFrame(data)

st.markdown("Dataframe below:")
st.dataframe(df) # interactive table

st.markdown("Static table below:")
st.table(df)     # static table


# =====
# user widget input
# ================

# text input
st.subheader("User Input Widget")

name = st.text_input("What is your name?", key="name_input", placeholder="Enter your name here")
if name: 
    st.write(f"Hello {name}!")
    
    
# NUmber input
st.subheader("Number input")
number = st.number_input("how old are you?", placeholder="Enter your age")
if number:
    st.write(f"You are {number} years old!")

# slider
st.subheader("Slider input")
my_slide = st.slider("select a current temperature", min_value=-10, max_value=50, value=20)
st.write(f"Current temperature is {my_slide} Celsius")


# options
option = st.selectbox("Choose your Domain",["Education", "Finance", "Health", "Technology"])
if option:
    st.write(f"You have selected {option} domain")
    
    
    
# ==============
# calculation app
# ===============

import streamlit as st


st.subheader("My Calculation App")

# number input
num1 = st.number_input("Enter first number", key="num1")
num2 = st.number_input("Enter second number", key="num2")

operation = st.selectbox("Choose operation", ['+', '-', '*', '/'])

# calculation
if operation == '+':
    result = num1 + num2
elif operation == '-':
    result = num1 - num2    
elif operation == '*':
    result = num1 * num2
elif operation == '/':
    if num2 != 0:
        result = num1 / num2
    else:
        result = "Error: Division by zero"
else:
    result = "Invalid operation"
st.write(f"The result of {num1} {operation} {num2} = {result}")



# ==============
# Buttons and actions
# ==============

st.subheader("Button and actions")

# divide page into three columns

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Say Hello"):
        st.write("Hello there!")
        st.balloons()# funny effect
with col2:
    if st.button("Show false"):
        st.write(f"button error!")
with col3:
    if st.button("Show success"):
        st.success("Operation was successful!")
        
        
st.divider()
        
