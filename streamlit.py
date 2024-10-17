import streamlit as st
import requests
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="TokenScore AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Professional Custom CSS with consistent text styling
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa, #ffffff);
    }
    
    /* Card styling with minimal spacing */
    .chat-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 0.6rem;
        margin: 0.4rem 0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    
    /* Message content styling */
    .message-content {
        margin-top: 0.2rem;
        line-height: 1.3;
    }
    
    /* User message styling */
    .user-message {
        background-color: #f8f9fa;
        border-left: 3px solid #0366d6;
    }
    
    /* Bot message styling */
    .bot-message {
        background-color: #ffffff;
        border-left: 3px solid #28a745;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.65rem;
        color: #6b7280;
        margin-bottom: 0.1rem;
    }
    
    /* Analysis text styling with consistent formatting */
    .analysis-text {
        color: #1a1f36;
        font-family: Arial, sans-serif;
        font-size: 0.85rem;
    }
    
    /* Override any italic styling in the analysis text */
    .analysis-text em,
    .analysis-text i {
        font-style: normal !important;
    }
    
    /* Reduce spacing after headings and bullet points */
    .analysis-text h1, .analysis-text h2, .analysis-text h3, 
    .analysis-text h4, .analysis-text h5, .analysis-text h6 {
        margin-top: 0.5em;
        margin-bottom: 0.2em;
        font-weight: normal;
    }
    
    .analysis-text ul, .analysis-text ol {
        margin-top: 0.2em;
        margin-bottom: 0.2em;
        padding-left: 1.2em;
    }
    
    .analysis-text li {
        margin-bottom: 0.1em;
    }
    
    .analysis-text p {
        margin-bottom: 0.3em;
    }
    
    /* Coins list styling */
    .coins-list {
        color: #6b7280;
        font-size: 0.75rem;
        margin-left: 0.2rem;
    }
    
    /* Remove extra padding from Streamlit containers */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stButton {
        margin-top: 0.2rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 0.3rem 0.6rem;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0366d6;
        color: #ffffff;
        border-radius: 6px;
        padding: 0.3rem 1.2rem;
        font-weight: 500;
        border: none;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
        padding: 0.6rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 0.6rem 0;
        color: #6b7280;
        border-top: 1px solid #e9ecef;
        margin-top: 0.6rem;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://156.67.111.168:5000"

class CryptoAnalyst:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_analysis(self, query):
        try:
            response = requests.post(
                f"{self.api_url}/crypto-chat",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")

# Initialize API client
analyst = CryptoAnalyst(API_URL)

# Sidebar
with st.sidebar:
    st.title("📊 TokenScore AI")
    st.markdown("<div style='height: 1px; background: #e9ecef; margin: 0.4rem 0;'></div>", unsafe_allow_html=True)
    
    # st.markdown("""
    # <div style='background-color: #f8f9fa; padding: 0.6rem; border-radius: 6px; margin-bottom: 0.6rem;'>
    #     <h4 style='color: #1a1f36; margin: 0 0 0.3rem 0;'>How to Use</h4>
    #     <ol style='color: #4a5568; margin: 0 0 0 1rem; padding-left: 0.8rem;'>
    #         <li>Enter your cryptocurrency question</li>
    #         <li>Include specific coin names</li>
    #         <li>Get AI-powered analysis</li>
    #     </ol>
    # </div>
    # """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #1a1f36; margin: 0.4rem 0;'>Example Queries</h4>", unsafe_allow_html=True)
    example_queries = [
        "Compare Bitcoin and Ethereum technical indicators",
        "Should I invest in Solana and Cardano?",
        "Analyze BTC market trends"
    ]
    for query in example_queries:
        if st.button(f"🔍 {query}", key=f"example_{query}"):
            st.session_state.query = query

# Main content area
st.title("Crypto Market Analysis")

# Query input
query = st.text_input(
    "Ask your question:",
    placeholder="e.g., Compare Bitcoin and Ethereum fundamentals",
    key="query"
)

# Analysis button
if st.button("Analyze", type="primary"):
    if query:
        with st.spinner("Analyzing cryptocurrencies..."):
            try:
                response = analyst.get_analysis(query)
                st.session_state.chat_history.append({
                    "query": query,
                    "response": response,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")
    else:
        st.warning("Please enter a question about specific cryptocurrencies.")

# Display chat history
for chat in reversed(st.session_state.chat_history):
    # User message
    st.markdown(f"""
    <div class='chat-card user-message'>
        <div class='timestamp'>You • {chat['timestamp']}</div>
        <div class='message-content'>{chat['query']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bot response
    analysis_text = chat['response']['analysis'].strip()
    coins_analyzed = ', '.join(chat['response']['coins']).upper()
    
    st.markdown(f"""
    <div class='chat-card bot-message'>
        <div class='timestamp'>
            CryptoAnalyst AI • {chat['timestamp']}
            <span class='coins-list'>• Analyzing: {coins_analyzed}</span>
        </div>
        <div class='analysis-text'>{analysis_text}</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <p>Powered by TokenScore • Real-time Crypto Analysis</p>
</div>
""", unsafe_allow_html=True)