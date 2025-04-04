import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import io
import ast

# Streamlit app setup
st.set_page_config(page_title="AI-Powered Data Analysis", layout="wide")
universal_prompt=""

# API Key Input
st.sidebar.header("Please Enter API Key Configuration of Gemini Model : 2.0-flash")
#gemini_api_key ="AIzaSyAYar5hv8_MKmojNJ-7In8Ev61-ModNihw"
gemini_api_key = st.sidebar.text_input("Enter your Gemini API key And Hit Enter:", type="password")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    st.sidebar.success("API Key Configured Successfully!")

# Tabs
tab1, tab2, tab3 ,tab4 = st.tabs(["Upload & Analyze", "Data Insights & Preprocessing", "Data Visualization","AI Chat with Dataset"])

def load_data(file):
    df = pd.read_csv(file)
    return df

with tab1:
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.success("File uploaded successfully!")
        
        if st.button("Analyze Dataset"):
            # Data overview
            st.subheader("Dataset Preview")
            st.dataframe(df.head())
            
            st.subheader("Data Info")
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            st.text(info_str)
            
            st.subheader("Descriptive Statistics")
            st.write(df.describe())
            
            # Extract unique values
            unique_values = {col: df[col].unique().tolist() for col in df.columns}
            
            # AI prompt
            universal_prompt= f"Data overview: {df.head().to_dict()}\nInfo: {info_str}\nDescribe: {df.describe().to_dict()}\nUnique Values: {unique_values}"
            ai_prompt = f"Data overview: {df.head().to_dict()}\nInfo: {info_str}\nDescribe: {df.describe().to_dict()}\nUnique Values: {unique_values}   . I have provided you dataset head with data.info , data.describe and each columns unique values . Study data i have provided to you and Pleases tell me 1)How can i use this dataset like for what application 2) Which feature i should foucus and consider for perticular application 3)Tell me detail steps of preprocessing to each feature and entire dataset as per"
            
            # Store for AI chat
            st.session_state['ai_prompt'] = ai_prompt
        
with tab2:
    st.header("Data Insights & Preprocessing")
    if 'ai_prompt' in st.session_state and gemini_api_key:
        if st.button("Get Response"):
            
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([st.session_state['ai_prompt']])
            st.write(response.text)

with tab3:
    st.header("Data Visualization")
    if uploaded_file is not None:

        st.subheader("Generated Charts from AI")
        
        if 'ai_prompt' in st.session_state and gemini_api_key:
            if st.button("Get Response",key="abc"):
                prop=universal_prompt+"please only return/write python code (no any words like ok, here below and other stuff) code must consist  1)from given data of dataset list of fetures to plot againts each other in  X/Y plane2)pei chart anaylse features 3)bar chart features "
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content([prop])
             
                st.write(response.text)


        if st.button("Generated Charts from data ",key="AAA"):
            num_cols = df.select_dtypes(include=['number']).columns
            for col in num_cols:
                fig, ax = plt.subplots()
                df[col].hist(ax=ax, bins=20)
                ax.set_title(f"Distribution of {col}")
                st.pyplot(fig)

with tab4:
    st.header("Data Insights & Preprocessing")
    st.subheader("Before Asking quetion Please Mensioned dataset and Any Important Information. (eg Real estate , House Price Prediction , Car Price Prediction ,etc)")
    user_ask = st.text_input("Enter your question or description:")

    if 'ai_prompt' in st.session_state and gemini_api_key:
        if st.button("Get Response",key="cd"):
            pr=universal_prompt+" "+user_ask
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([pr])
            st.write(response.text)
