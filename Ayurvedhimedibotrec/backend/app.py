import streamlit as st
import requests
import json
from PIL import Image
import base64
from io import BytesIO

# Configuration
API_URL = "http://localhost:8000"  # Change this if your API is hosted elsewhere

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'welcome'
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Updated get_medicine_recommendation function
def get_medicine_recommendation(indications):
    try:
        if not indications.strip():
            st.warning("Please enter some symptoms to search")
            return None
            
        encoded_indications = requests.utils.quote(indications)
        response = requests.get(f"{API_URL}/search?query={encoded_indications}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                st.warning(f"No remedies found for: '{indications}'. Try different keywords.")
                return None
                
            return results
            
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not reach the Ayurvedic API. {str(e)}")
        return None

# Updated format_medicine_info function
def format_medicine_info(medicine):
    info = []
    info.append(f"**Medicine:** {medicine['medicine']}")
    info.append(f"**Indications:** {medicine['indications']}")
    info.append(f"**Dose:** {medicine['dose']}")
    info.append("**Ingredients:**")
    info.extend([f"- {ingredient}" for ingredient in medicine['ingredients']])
    info.append(f"**Precautions:** {medicine['precautions']}")
    info.append(f"**Side Effects:** {medicine['side_effects']}")
    return "\n\n".join(info)

#format medicine information
def format_medicine_info(medicine):
    ingredients_list = '\n'.join([f'- {ingredient}' for ingredient in medicine['ingredients']])
    return f"""
**Medicine:** {medicine['medicine']}

**Indications:** {medicine['indications']}

**Recommended Dose:** {medicine['dose']}

**Key Ingredients:**
{ingredients_list}

**Precautions:** {medicine['precautions']}

**Possible Side Effects:** {medicine['side_effects']}
"""

# Streamlit app configuration
st.set_page_config(page_title="Ayurvedha - Ancient Healing Wisdom", layout="wide")

# Theme management
ms = st.session_state
if "themes" not in ms:
    ms.themes = {
    "current_theme": "light",
    "refreshed": True,
    "light": {
        "theme.base": "dark",
        "theme.backgroundColor": "#C1B7D3",  # Soft lavender
        "theme.primaryColor": "#9A86B3",      # Deeper lavender (for contrast)
        "theme.secondaryBackgroundColor": "#E2DFEB",  # Very light lavender
        "theme.textColor": "#130b42",         # Dark gray for readability
        "button_face": "🌜"
    },
    "dark": {
        "theme.base": "light",
        "theme.backgroundColor": "#E35336",   # Vibrant red-orange
        "theme.primaryColor": "#FF6B4D",      # Brighter orange (accent)
        "theme.secondaryBackgroundColor": "#EC8D77",  # Soft coral
        "theme.textColor": "#FFFFFF",         # White text
        "button_face": "🌞"
    }
}

def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark": ms.themes["current_theme"] = "light"
    elif previous_theme == "light": ms.themes["current_theme"] = "dark"

btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
st.sidebar.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()

# CSS for styling
st.markdown("""
    <style>
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .user-message {
        background-color: #e8f5e9;
        color: #000;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        max-width: 60%;
        text-align: right;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #c8e6c9;
        color: #000;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        max-width: 60%;
        text-align: left;
        float: left;
        clear: both;
        border: 1px solid #a5d6a7;
    }
    .medicine-card {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #2e7d32;
    }
    .stTextArea textarea {
        min-height: 100px;
    }
    </style>
""", unsafe_allow_html=True)

#Welcome page

def welcome_page():
    st.markdown("""
        <style>
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }
        .image-container {
            width: 250px;
            height: 250px;
            background-color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: center; font-size: 48px; font-weight: bold; color: #130b42;'>
        Welcome to AyurBot!
    </h1>
    """, unsafe_allow_html=True)

    try:
        # Load your actual image
        img = Image.open("D:/Ayurvedhimedibotrec/frontend/IMAGES/Ayur.jpg")  # Change to your image path
        img.thumbnail((250, 250))  # Resize while maintaining aspect ratio
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Display image in the green container
        st.markdown(f"""
            <div class="image-container">
                <img src="data:image/png;base64,{img_str}" 
                     style="max-width: 100%; max-height: 100%; object-fit: contain;">
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading image: {e}")
        # Fallback to green box if image fails
        st.markdown('<div class="image-container"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; font-size: 18px; margin: 20px 0;">
        <p><strong>Nurturing Wellness Through Nature and Routine.</strong></p>
        <p>Let food be thy medicine, and herbs your daily companion.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Ayurvedha Insight", type="primary", use_container_width=True):
            st.session_state['page'] = 'chatbot'
            st.rerun()

# Chatbot Page
def chatbot_page():
    st.title("Ayurvedha - Ancient Healing Wisdom")
    
    # Sidebar for chat history
    with st.sidebar:
        st.header("Herbal Solution History")
        if st.session_state['chat_history']:
            for i, (role, text) in enumerate(st.session_state['chat_history']):
                with st.expander(f"{role}: {text[:30]}...", expanded=False):
                    st.write(text)
        else:
            st.write("No History Yet.")
        
        if st.button("Clear History"):
            st.session_state['chat_history'] = []
            st.rerun()

    # Main chat interface
    with st.form(key="input_form", clear_on_submit=True):
        user_input = st.text_area(
            "Describe Your Symptoms", 
            height=100,
            placeholder="E.G. Digestive Issues, Fatigue, Headache..."
        )
        submitted = st.form_submit_button("Get Herbal Solutions")
    
    if submitted and user_input:
        st.session_state['chat_history'].append(("You", user_input))
        
        with st.spinner('Consulting Ayurvedic texts...'):
            medicines = get_medicine_recommendation(user_input)
            
            if medicines:
                for medicine in medicines:
                    response = format_medicine_info(medicine)
                    st.session_state['chat_history'].append(("Ayurvedha", response))
            else:
                st.session_state['chat_history'].append(("Ayurvedha", 
                    "No matching Ayurvedic remedy found. Please try different symptoms."))
        
        st.rerun()

    # Display current conversation
    st.subheader("Herbal Solutions")
    for role, message in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
        else:
            if "Medicine:" in message:
                st.markdown(f'<div class="medicine-card">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message}</div>', unsafe_allow_html=True)

    st.markdown("<div style='clear:both;'></div>", unsafe_allow_html=True)

# Main app logic
if st.session_state['page'] == 'welcome':
    welcome_page()
else:
    chatbot_page() 
