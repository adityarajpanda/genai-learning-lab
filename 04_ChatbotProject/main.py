# Inside this file, we need to import everything from the 'app' folder.

import streamlit as st
from app.chat_utils import get_chat_model, ask_chat_model
from app.pdf_utils import extract_text_from_pdf
from app.ui import pdf_uploader
from app.vectorstore_utils import create_faiss_index, retrieve_similar_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter # for breaking large documents into smaller, manageable chunks

import os
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True)) 

api_key=os.environ["EURI_API_KEY"]

# Creating streamlit page configuration which means to create streamlit UI configuration to interact
# Command to run a streamlit app: streamlit run main.py
# main.py is the entry point of the streamlit app. It is the first file that will be executed when we run the streamlit app.
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded")

# streamlit markdown is used to write HTML and CSS code in streamlit app. It is used to style the streamlit app.
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
        color: black;
    }
    .chat-message .avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .chat-message .message {
        flex: 1;
    }
    .chat-message .timestamp {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff3333;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# streamlit session state is used to store the state of the app.
if "messages" not in st.session_state: # if messages is not in session state, then create an empty list of messages in session state. This is used to store the chat history.
    st.session_state.messages = []
if "vectorstore" not in st.session_state: # if vectorstore is not in session state, then create an empty vectorstore in session state. This is used to store the vectorstore.
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state: # if chat_model is not in session state, then create a chat_model in session state. This is used to store the chat model.
    st.session_state.chat_model = None

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #ff4b4b; font-size: 3rem; margin-bottom: 0.5rem;">🏥 MediChat Pro</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent Medical Document Assistant</p>
</div>
""", unsafe_allow_html=True)

# streamlit sidebar is used to create a sidebar in streamlit app. It will be used to upload the medical documents and process them.
with st.sidebar:
    st.markdown("### 📁 Document Upload")
    st.markdown("Upload your medical documents to start chatting!")
    
    uploaded_files = pdf_uploader()
    
    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")
        
        # Process documents
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                # Extract text from all PDFs
                all_texts = []
                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    all_texts.append(text)
                
                # Split texts into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                
                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))
                
                # Create FAISS index
                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore
                
                # Initialize chat model
                chat_model = get_chat_model(api_key)
                st.session_state.chat_model = chat_model
                
                st.success("✅ Documents processed successfully!")
                st.balloons()

# Main chat interface
st.markdown("### 💬 Chat with Your Medical Documents")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Ask about your medical documents..."):
    # Add user message to chat history
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt, 
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    
    # Generate response
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                # Retrieve relevant documents
                relevant_docs = retrieve_similar_documents(st.session_state.vectorstore, prompt)
                
                # Create context from relevant documents
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                # Create prompt with context
                system_prompt = f"""You are MediChat Pro, an intelligent medical document assistant. 
                Based on the following medical documents, provide accurate and helpful answers. 
                If the information is not in the documents, clearly state that.

                Medical Documents:
                {context}

                User Question: {prompt}

                Answer:"""
                
                response = ask_chat_model(st.session_state.chat_model, system_prompt)
            
            st.markdown(response)
            st.caption(timestamp)
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response, 
                "timestamp": timestamp
            })
    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Please upload and process documents first!")
            st.caption(timestamp)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🤖 Powered by Euri AI & LangChain | 🏥 Medical Document Intelligence</p>
</div>
""", unsafe_allow_html=True)    