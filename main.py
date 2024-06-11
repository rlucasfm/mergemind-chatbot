import streamlit as st
from openai import OpenAI
import time
from PIL import Image

client = OpenAI()
assistant_id = "asst_m71G67XOUmf8ZDQz2yZhlEfK"
thread = client.beta.threads.create()

image = Image.open('mm-logo2.png')

st.image(image)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Quer saber como usar IA na sua empresa? Fala comigo!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while run.status != 'completed':
        time.sleep(0.3)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve messages added by the assistant
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    response = messages.to_dict()

    msg = response.get('data')[0]['content'][0]['text']['value']
    msg = msg.split('【')[0]

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)