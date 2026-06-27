import streamlit as st
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load secret environment configurations securely
load_dotenv()

# ==========================================
# 1. MCP-STYLE RESOURCE & TOOL MANAGEMENT
# ==========================================
class SafeSpaceMCPServer:
    @staticmethod
    def secure_log_pattern(feeling: str, category: str) -> str:
        log_entry = f"Trend Logged -> Context: [{category}] | Vector: [{feeling}]\n"
        try:
            with open("journal.txt", "a", encoding="utf-8") as file:
                file.write(log_entry)
            return "Resource updated successfully: Trend appended securely."
        except Exception as e:
            return f"Resource Error: Unable to write to disk. Details: {str(e)}"

MCP_TOOLS = {"secure_log_pattern": SafeSpaceMCPServer.secure_log_pattern}

# ==========================================
# 2. SECURITY GUARDRAILS
# ==========================================
def security_privacy_scrub(text: str) -> str:
    # Scrubs out explicit high-risk personal data types (like account numbers)
    return re.sub(r'\b\d{4,}[-\s]?\d{4,}\b', '[REDACTED SENSITIVE DATA]', text)

# ==========================================
# 3. MULTI-AGENT ADK IMPLEMENTATION FOR WEB
# ==========================================
def run_safespace_agents(raw_user_input: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    clean_user_input = security_privacy_scrub(raw_user_input)
    
    # --- Agent 2: The Back-End Insight Analyst (Runs silently) ---
    analyst_instruction = (
        "You are SafeSpace Agent 2: The Back-End Insight Analyst. "
        "Review what the user expressed, determine the primary emotional vector "
        "and the topic cluster. You MUST execute this assessment by calling the 'secure_log_pattern' tool."
    )
    analyst_context = [
        types.Content(role="user", parts=[types.Part.from_text(text=f"Analyze this entry: {clean_user_input}")])
    ]
    
    # We don't display Agent 2's thoughts to the user, but we run it to trigger the tool
    analyst_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=analyst_context,
        config=types.GenerateContentConfig(
            system_instruction=analyst_instruction,
            tools=[SafeSpaceMCPServer.secure_log_pattern],
            temperature=0.1 
        )
    )
    
    if analyst_response.function_calls:
        for call in analyst_response.function_calls:
            tool_func = MCP_TOOLS[call.name]
            tool_func(**call.args) # Executes the silent logging

    # --- Agent 1: The Front-End Empathetic Listener (Talks to User) ---
    listener_instruction = (
        "You are SafeSpace Agent 1: The Front-End Empathetic Listener. "
        "Your sole core mission is active listening and deep emotional validation. "
        "CRITICAL RULES: Never give advice, never propose task frameworks. "
        "Mirror emotional pacing, show unconditional warmth, and acknowledge difficulties."
    )
    
    listener_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=clean_user_input,
        config=types.GenerateContentConfig(
            system_instruction=listener_instruction,
            temperature=0.7
        )
    )
    
    return listener_response.text

# ==========================================
# 4. STREAMLIT WEB UI
# ==========================================
st.set_page_config(page_title="SafeSpace", page_icon="🌿")

st.title("🌿 SafeSpace")
st.caption("A secure, multi-agent AI built to listen, validate, and track patterns without giving unprompted advice.")

# Initialize chat history in the browser's memory
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming first message from the agent
    st.session_state.messages.append({"role": "assistant", "content": "Hi. I'm here to listen. You can share whatever is on your mind—no advice, no judgment."})

# Display previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for the user to type something in the chat box
if prompt := st.chat_input("What is on your mind today?"):
    
    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show a loading spinner while the agents do their work
    with st.spinner("SafeSpace is listening and processing..."):
        agent_reply = run_safespace_agents(prompt)
        
    # Display the agent's empathetic response
    with st.chat_message("assistant"):
        st.markdown(agent_reply)
    st.session_state.messages.append({"role": "assistant", "content": agent_reply})