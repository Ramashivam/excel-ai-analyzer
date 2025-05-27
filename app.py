import streamlit as st
import pandas as pd
import openai
import io

st.set_page_config(page_title="Excel Q&A with AI", layout="wide")

st.title("📊 Upload Excel & Ask Questions with AI")
st.markdown("Upload your Excel file, click Analyze, and ask anything about the data!")

# Step 1: OpenAI API Key Input
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Step 2: Upload Excel
uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx"])

if uploaded_file and openai_api_key:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded and data read successfully!")
    st.write("📄 Here's a preview of your data:", df.head())

    # Step 3: Ask Questions
    question = st.text_input("🤔 Ask a question about the data")

    if st.button("Analyze"):
        if question.strip() == "":
            st.warning("Please enter a question!")
        else:
            prompt = f"""You are a data analyst. Here is the data:\n{df.to_csv(index=False)}\n\nAnswer the following question based on this data:\n\n{question}"""
            try:
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )
                answer = response.choices[0].message["content"]
                st.success("🧠 AI Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error from OpenAI: {e}")
else:
    st.info("📥 Please upload a file and enter your OpenAI API key to continue.")
