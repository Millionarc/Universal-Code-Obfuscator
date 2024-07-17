import os
import re
import requests
import streamlit as st

def get_obfuscated_code(api_key, code):
    # USE PROMPT1 IF WORKING, RAN INTO ISSUES WITH CODESTRAL ISSUES WITH CODE NOT GENERATING/BEING RETURNED RIGHT BEFORE DEPLOYMENT 


    prompt1 = f"""
Obfuscate the following code by:
1. using a random combination of 10-12 letters for all variables.
2. Inlining smaller functions where possible.
3. Minimizing the code.
4. Removing comments.
5. Using complex control flow, such as adding random conditionals and other structures.
6. Randomizing the code to make function patterns less recognizable.
7. Encoding all strings except for links/endpoints that have a .com in it or start with wss, http, https.
8. Adding dummy code that doesn't affect the program flow.
9. Renaming functions to non-descriptive names.
Ensure that:
1. The code runs correctly on browsers, Windows, Linux, and macOS.
2. No variables are redeclared accidentally.
3. All variable names and strings use only alphanumeric characters and underscores.
4. Variable names are long and complex to further obfuscate the code.
5. The script runs the same and is structured the same, only reply in the text box with the obfuscated code and no other text.
6. LINKS ARE NOT ENCODED.
7. All variables and functions are used the same.
8. When importing other libraries, the string used to pull it in is left normal, however it can be assigned to a different variable name after import.
9. Only the obfuscated code is included inside the content parameter of the message, without any additional descriptions or text.
Here is the code:
{code}
"""

    
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
