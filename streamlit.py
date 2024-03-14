import main as lch
import streamlit as st
import textwrap

st.title("Summarizer Bot")

with st.sidebar:
    with st.form(key='my_form'):
        url = st.sidebar.text_area(
            label="What is the URL?",
            max_chars=250
            )
        number = st.sidebar.text_area(
            label="What is the phone number?",
            max_chars=250
            )

if url:
    docs = lch.create_db_from_url(url)
    response = lch.generate_summary(docs)
    st.write(response)
    if number:
      lch.send_summary(number, response)
      st.info("Summary sent to the your phone number")