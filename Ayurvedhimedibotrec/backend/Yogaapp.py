# ====== NON-STREAMLIT IMPORTS ======
# At the top of yogaapp.py
import streamlit as st
import json
from PIL import Image
import os

def yoga_page():
    st.title("🧘 Yoga for Wellness")

    # Load data
    try:
        with open("Yoga_Data/yoga_data.json") as f:
            yoga_data = json.load(f)
    except:
        st.error("Could not load yoga data.")
        return

    # Search bar
    search = st.text_input("Enter symptom or category (e.g. stress, digestion, pain):").lower()

    matches = []
    for pose in yoga_data["poses"]:
        if search in pose["benefits"].lower() or search in pose["name"].lower():
            matches.append(pose)

    if matches:
        for pose in matches:
            st.subheader(pose["name"])
            st.write(f"**Benefits:** {pose['benefits']}")
            st.write(f"**Instructions:** {pose['description']}")
            image_path = f"Yoga_Images/{pose['image']}"
            if os.path.exists(image_path):
                st.image(image_path, width=400)
            else:
                st.warning("Image not found.")
    else:
        if search:
            st.info("No matching poses found. Try another symptom.")

import requests
import json
from PIL import Image
import base64
from io import BytesIO
import os

# ====== STREAMLIT CONFIGURATION (MUST BE FIRST) ======
import streamlit as st
st.set_page_config(
    page_title="Yoga Pose Recommender",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== CONSTANTS ======
API_URL = "http://localhost:8000"

# ====== THEME CONFIGURATION ======
def setup_theme():
    if "themes" not in st.session_state:
        st.session_state.themes = {
            "current_theme": "light",
            "light": {
                "theme.base": "light",
                "theme.backgroundColor": "#FFE5AB",  # Soft peach
                "theme.primaryColor": "#FFB347",     # Warm orange
                "theme.secondaryBackgroundColor": "#FFF4E5",  # Light cream
                "theme.textColor": "#002244",       # Dark blue
                "button_face": "🌞"
            },
            "dark": {
                "theme.base": "dark",
                "theme.backgroundColor": "#002244",  # Deep blue
                "theme.primaryColor": "#FFB347",     # Same warm accent
                "theme.secondaryBackgroundColor": "#334455",  # Muted blue
                "theme.textColor": "#FFE5AB",       # Light peach
                "button_face": "🌙"
            }
        }

    def change_theme():
        previous_theme = st.session_state.themes["current_theme"]
        new_theme = "dark" if previous_theme == "light" else "light"
        st.session_state.themes["current_theme"] = new_theme
        
        # Update theme config
        theme = st.session_state.themes[new_theme]
        for key, value in theme.items():
            if key.startswith("theme"):
                st._config.set_option(key, value)
        
        st.rerun()

    # Theme toggle button
    with st.sidebar:
        current_theme = st.session_state.themes["current_theme"]
        btn_face = st.session_state.themes[current_theme]["button_face"]
        st.button(btn_face, on_click=change_theme)

setup_theme()

# ====== SESSION STATE INIT ======
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ====== CUSTOM CSS ======
st.markdown("""
    <style>
    .stApp {
        background-color: #FFE5AB;
    }
    .user-message {
        background-color: #FFB347;
        color: #002244;
        border-radius: 15px 15px 0 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
    }
    .bot-message {
        background-color: #FFF4E5;
        color: #002244;
        border-radius: 15px 15px 15px 0;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        border: 1px solid #FFB347;
    }
    .pose-card {
        background-color: #FFF4E5;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #FFB347;
    }
    .stButton>button {
        background-color: #FFB347;
        color: #002244;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FFA726;
    }
    </style>
""", unsafe_allow_html=True)

# ====== YOGA FUNCTIONS ======
def get_yoga_recommendation(query):
    try:
        response = requests.get(f"{API_URL}/search?query={query}", timeout=10)
        if response.status_code == 200:
            return response.json().get("results", [])
        st.error(f"API Error {response.status_code}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
    return None

def format_pose_info(pose):
    # Construct the full image URL
    image_url = f"http://localhost:8000/static/{pose['image_url']}"
    
    return f"""
<div style="margin: 20px 0; padding: 15px; border-radius: 10px; background: #FFF4E5;">
    <h3>{pose['pose_name']} ({pose['sanskrit_name']})</h3>
    <p><strong>Best for:</strong> {pose['indication']}</p>
    <p><strong>Benefits:</strong> {pose['purpose']}</p>
    <p><strong>How to do it:</strong> {pose['description']}</p>
    <img src="{image_url}" style="max-width: 300px; border-radius: 8px; margin-top: 10px;">
</div>
"""

# ====== PAGE FUNCTIONS ======
def welcome_page():
    st.markdown("""
        <style>
        .image-container {
            width: 250px;
            height: 250px;
            background-color: #FFF4E5;
            margin: 0 auto;
            border-radius: 50%;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 3px solid #FFB347;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: center; color: #002244;'>
        Welcome to YogaBot!
    </h1>
    """, unsafe_allow_html=True)

    try:
        img = Image.open("D:\Yoga\IMAGES\Yoga.jpg")
        img.thumbnail((250, 250))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(f"""
            <div class="image-container">
                <img src="data:image/png;base64,{img_str}" 
                     style="max-width: 100%; max-height: 100%; object-fit: cover;">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <p><strong>Find balance and strength through yoga</strong></p>
        <p>Try searching for: <i>stress relief, back pain, flexibility</i></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Begin Yoga Journey", type="primary", use_container_width=True):
        st.session_state.page = 'chatbot'
        st.rerun()

def chatbot_page():
    all_poses = requests.get(f"{API_URL}/poses").json()
    for pose in all_poses["poses"]:
        image_path = f"D:/YOGA/IMAGES/{pose['image_url']}"
        exists = "✅" if os.path.exists(image_path) else "❌"
    st.title("Yoga Pose Recommender")
    
    with st.form(key="yoga_form"):
        user_input = st.text_area(
            "What do you need help with?",
            placeholder="e.g. calm mind, back pain, improve flexibility",
            height=100
        )
        submitted = st.form_submit_button("Find Poses")
    
    if submitted and user_input:
        with st.spinner('Finding yoga poses...'):
            poses = get_yoga_recommendation(user_input)
            
            if poses:
                for pose in poses:
                    # Use markdown with unsafe_allow_html
                    st.markdown(
                        format_pose_info(pose), 
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No matching poses found")
# ====== MAIN APP LOGIC ======
if st.session_state.page == 'welcome':
    welcome_page()
else:
    chatbot_page()