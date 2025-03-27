import streamlit as st
import openai_api

IMG_MODELS = ['dall-e-2', 'dall-e-3']

if "image" not in st.session_state:
    st.session_state["image"] = None
    st.session_state["image_model"] = IMG_MODELS[1]


input_container = st.container()
img_container = st.container()

with input_container:
    if prompt := st.chat_input("Type your image prompt here."):
        try:
            img = openai_api.generate_image(prompt, size="1024x1024", model= st.session_state["image_model"])
            st.session_state["image"] = img
        except Exception as e:
            print(e)



with img_container:
    if st.session_state["image"]:
        st.image(st.session_state["image"])


