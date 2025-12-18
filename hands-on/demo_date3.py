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


