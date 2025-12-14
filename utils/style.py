import base64
import streamlit as st
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_style():
    # Attempt to load local image
    bin_str = ""
    try:
        if os.path.exists("library_bg.jpg"):
            bin_str = get_base64_of_bin_file("library_bg.jpg")
    except:
        pass
    
    background_style = ""
    if bin_str:
        # Dimmed Background: Stronger Cream overlay to improve text readability
        background_style = f"""
        background-image: linear-gradient(rgba(255, 252, 245, 0.8), rgba(255, 252, 245, 0.8)), 
                          url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        """
    else:
        background_style = "background-color: #FFF8E1;"

    # GLASSMORPHISM CSS - STRICT WARM HARMONY
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');

    /* Global App */
    .stApp {{
        {background_style}
        background-attachment: fixed;
        color: #3E2723; /* Primary Text: Dark Brown */
        font-family: 'Poppins', sans-serif;
    }}

    /* Sidebar - Premium Warm Beige */
    [data-testid="stSidebar"] {{
        background: rgba(245, 240, 230, 0.9); /* Opaque enough to be legible, distinct beige */
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(121, 85, 72, 0.2);
        box-shadow: 4px 0 15px rgba(62, 39, 35, 0.05);
    }}
    
    [data-testid="stSidebar"] * {{
        color: #3E2723 !important;
    }}
    
    /* Active Sidebar Item */
    .stButton button:focus {{
        box-shadow: 0 0 0 2px rgba(121, 85, 72, 0.4);
    }}

    /* GLASS CARDS - High Contrast & Visibility */
    /* Applied to Dataframes, Forms, and Generic Containers */
    [data-testid="stDataFrame"], [data-testid="stForm"], div.stMarkdown > div > div > div {{
        background-color: rgba(255, 255, 255, 0.85); /* Light Base for readability */
        backdrop-filter: blur(20px); /* Strong blur */
        border-radius: 12px;
        border: 1px solid rgba(141, 110, 99, 0.3); /* Defined border */
        box-shadow: 0 6px 20px rgba(62, 39, 35, 0.08); /* Soft but visible shadow */
    }}

    /* Inputs - Clean & Accessible */
    /* Inputs - Clean & Accessible */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stTextArea {{
        background-color: #FFFFFF !important;
        border: 1px solid #BCAAA4 !important; /* Soft Brown Border */
        color: #3E2723 !important;
        border-radius: 6px;
        font-weight: 500;
    }}
    
    .stTextInput input:focus {{
        border-color: #795548 !important;
        box-shadow: 0 0 0 2px rgba(121, 85, 72, 0.2);
    }}
    
    /* Input Labels (The text above the box) */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label, .stRadio label {{
        color: #3E2723 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}
    
    /* Placeholders */
    ::placeholder {{
        color: #8D6E63 !important; /* Lighter Brown for placeholder */
        opacity: 0.8 !important;
    }}
    
    /* General Text Body */
    .stMarkdown p, .stMarkdown li {{
        color: #3E2723 !important;
    }}
    
    /* Dataframe Text */
    div[data-testid="stDataFrame"] * {{
        color: #3E2723 !important;
    }}

    /* BUTTONS - Consistent Warm Palette */
    
    .stButton > button {{
        background-color: #795548; /* Primary: Warm Medium Brown */
        color: #FFF8E1 !important; /* Cream Text for Contrast */
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(62, 39, 35, 0.2);
    }}
    
    .stButton > button:hover {{
        background-color: #8D6E63; /* Lighter on Hover */
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(62, 39, 35, 0.3);
    }}
    
    .stButton > button:active, .stButton > button[kind="primary"] {{
        background-color: #5D4037 !important; /* Darker/Rich for Active/Primary */
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: #3E2723;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    /* Muted Text / Captions */
    .stCaption {{
        color: #6D4C41 !important; /* Muted Brown */
        font-size: 0.9rem;
    }}

    /* Tabs */
    .stTabs [aria-selected="true"] {{
        color: #5D4037;
        border-bottom-color: #5D4037;
    }}

    /* Metrics */
    [data-testid="stMetricLabel"] {{
        color: #6D4C41;
    }}
    [data-testid="stMetricValue"] {{
        color: #3E2723;
        font-weight: 700;
    }}

    </style>
    """, unsafe_allow_html=True)
