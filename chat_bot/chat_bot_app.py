import json

import requests
import streamlit as st

# Description
st.set_page_config(layout="wide", page_title="distilgpt2")
st.markdown(
    "<h1 style='text-align: center; color: coral;'>DistilGPT-2!</h1>",
    unsafe_allow_html=True,
)

st.write("##### *Description:*")
st.write(
    """
    DistilGPT-2, a distilled version of OpenAI's GPT-2 model,
was introduced as a response to concerns regarding the computational resources
required to train and deploy large-scale language models.
Developed by Victor Sanh, Lysandre Debut, Julien Chaumond,
and Thomas Wolf at Hugging Face,
DistilGPT-2 aimed to retain the core capabilities of GPT-2
while significantly reducing its size and computational cost.
"""
)

with open("distilgpt2_inference.zip", "rb") as zipfile:
    st.download_button(
        "Download inference .ipynb",
        zipfile,
        mime="application/zip",
        help="Here is the inference process of the neural network",
    )

with open("distilgpt2_train.zip", "rb") as zipfile:
    st.download_button(
        "Download training .ipynb",
        zipfile,
        mime="application/zip",
        help="Here is the training process of the neural network",
    )

st.markdown(
    "<h3 style='text-align: center; color: coral;'>Echo ChatBot</h1>",
    unsafe_allow_html=True,
)


# Bot
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter your message to the Bot")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    req = requests.post(
        "http://backend_engine:5000/predict",
        data=json.dumps({"text": prompt})
    )
    result = req.json()["predictions"]

    st.session_state.messages.append({"role": "assistant", "content": result})

    with st.chat_message("assistant"):
        st.markdown(result)
