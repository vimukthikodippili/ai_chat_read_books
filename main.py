import streamlit as st
import requests
import time

# Backend configuration
BACKEND = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="📚 PDF Chat + Reader", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("📚 PDF Chat + Real-Time Reader")
st.markdown("Upload a PDF and interact with it through text-to-speech and Q&A!")

# Check backend connection
def check_backend():
    try:
        response = requests.get(f"{BACKEND}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Backend status check
if not check_backend():
    st.error("🚨 Backend server is not running! Please start the backend first.")
    st.markdown("""
    **To start the backend:**
    1. Open a new terminal/command prompt
    2. Navigate to your project directory
    3. Run: `python backend.py`
    4. Wait for "PDF Reader API Server started successfully!" message
    5. Then refresh this page
    """)
    st.stop()

st.success("✅ Backend server is running!")

# Initialize session state
if "file_id" not in st.session_state:
    st.session_state.file_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. PDF Upload Section
st.header("📄 Step 1: Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if st.button("Upload PDF", type="primary"):
        with st.spinner("Uploading and processing PDF..."):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{BACKEND}/api/upload", files={"file": uploaded_file})
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.file_id = result["file_id"]
                    st.success(f"✅ PDF uploaded successfully!")
                    st.info(f"**File ID:** `{result['file_id']}`")
                    
                    # Show preview
                    with st.expander("📖 Content Preview"):
                        st.text(result.get("preview", "No preview available"))
                else:
                    st.error(f"❌ Upload failed: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure it's running!")
            except Exception as e:
                st.error(f"❌ Upload error: {str(e)}")

# Show features only if PDF is uploaded
if st.session_state.file_id:
    st.divider()
    
    # 2. Reading Controls Section
    st.header("🗣️ Step 2: Text-to-Speech Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start Reading Whole PDF", type="primary"):
            with st.spinner("Starting text-to-speech..."):
                try:
                    response = requests.post(f"{BACKEND}/api/read/start/{st.session_state.file_id}")
                    if response.status_code == 200:
                        st.success("🗣️ Reading started! Check your audio.")
                    else:
                        st.error("❌ Failed to start reading")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("⏹️ Stop Reading"):
            try:
                response = requests.post(f"{BACKEND}/api/read/stop")
                if response.status_code == 200:
                    st.success("🔇 Reading stopped.")
                else:
                    st.error("❌ Failed to stop reading")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # 3. Chat/Q&A Section
    st.header("💬 Step 3: Ask Questions About Your PDF")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{BACKEND}/api/chat", json={
                        "file_id": st.session_state.file_id,
                        "message": prompt
                    })
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result["answer"]
                        st.write(answer)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        
                        # Option to speak the answer
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("🔊 Speak Answer", key=f"speak_{len(st.session_state.messages)}"):
                                try:
                                    # Stop any current reading first
                                    requests.post(f"{BACKEND}/api/read/stop")
                                    time.sleep(0.5)
                                    # Speak the answer
                                    requests.post(f"{BACKEND}/api/speak", params={"text": answer})
                                    st.success("🗣️ Speaking answer...")
                                except Exception as e:
                                    st.error(f"❌ Speech error: {str(e)}")
                    else:
                        st.error("❌ Failed to get answer")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Sidebar with instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload PDF**: Choose and upload your PDF file
    2. **Start Reading**: Click to hear the entire PDF read aloud
    3. **Stop Reading**: Stop the text-to-speech at any time
    4. **Ask Questions**: Type questions about your PDF content
    5. **Speak Answers**: Click 🔊 to hear answers aloud
    
    **Tips:**
    - Make sure your audio is turned on
    - Ask specific questions for better answers
    - You can stop and start reading at any time
    """)
    
    st.header("🔧 Technical Info")
    if st.session_state.file_id:
        st.success("✅ PDF Loaded")
        st.text(f"File ID: {st.session_state.file_id[:8]}...")
    else:
        st.info("No PDF loaded yet")
    
    # Backend status
    if check_backend():
        st.success("✅ Backend Online")
    else:
        st.error("❌ Backend Offline")