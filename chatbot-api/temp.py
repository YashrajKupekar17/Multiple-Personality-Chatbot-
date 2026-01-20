import streamlit as st

st.set_page_config(page_title="Simple Form App", layout="centered")

st.title("📝 Simple Input Form")

with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    message = st.text_area("Message")

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Form submitted successfully!")
        st.write("### 📋 Submitted Information")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Age:** {age}")
        st.write(f"**Message:** {message}")
