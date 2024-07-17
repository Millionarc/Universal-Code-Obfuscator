import os
import re
import requests
import streamlit as st

def get_obfuscated_code(api_key, code):
    #Find what works best for you, this was the only one that universally worked across multiple languages
    prompt = (
        "Obfuscate the following code using a random combination of 10-12 letters for all variables, on imports ensure the whole library is being imported to assign to variables without errors, making it extremely hard to view as a human "
        "splitting functions, minimizing, removing comments, encoding strings, and adding dummy code:\n"
        f"{code}"
    )
    response = requests.post(
        "https://codestral.mistral.ai/v1/fim/completions",
        json={
            "model": "codestral-latest",
            "prompt": prompt,
            "suffix": ""
        },
        headers={"Authorization": f"Bearer {api_key}"}
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Status code for api  {response.status_code}")
        return None

def clean_obfuscated_code(code):
    match = re.search(r'```(.*?)```', code, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return code.strip()

st.title("Multi Programming Language Code Obfuscator")

api_key = st.text_input("Enter your Codestral API key", type="password")

uploaded_files = st.file_uploader("Upload the code you want to obfuscate", accept_multiple_files=True)
if uploaded_files and api_key:
    for uploaded_file in uploaded_files:
        code = uploaded_file.read().decode('utf-8')
        obfuscated_code = get_obfuscated_code(api_key, code)
        if obfuscated_code:
            clean_code = clean_obfuscated_code(obfuscated_code)
            obfuscated_file_path = f"{os.path.splitext(uploaded_file.name)[0]}_obfuscated{os.path.splitext(uploaded_file.name)[1]}"
            st.download_button(
                label="Download obfuscated code",
                data=clean_code,
                file_name=obfuscated_file_path,
                mime='text/plain'
            )
else:
    st.info("Please upload at least one file to obfuscate and enter your API key.")
