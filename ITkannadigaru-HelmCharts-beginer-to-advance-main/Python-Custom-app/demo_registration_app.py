# demo_registration_app.py

import streamlit as st
from datetime import date
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Demo Registration Form",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Welcome!")
st.sidebar.info(
    """
    This is a **Demo Registration Form** built with Streamlit.
    
    - Fill in your details
    - Upload a profile picture
    - See your info displayed dynamically
    """
)

# Title
st.title("📝 Registration Form Demo")
st.markdown("Please fill in the details below:")

# --- Registration Form ---
with st.form(key="registration_form"):
    # Name Inputs
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
    with col2:
        last_name = st.text_input("Last Name")
    
    # Email & Password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    # Gender Selection
    gender = st.radio("Gender", ("Male", "Female", "Other"))
    
    # Date of Birth
    dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())
    
    # Country Selection
    country = st.selectbox(
        "Country",
        ("India", "USA", "UK", "Germany", "Other")
    )
    
    # Interests
    interests = st.multiselect(
        "Select your interests",
        ["Python", "Machine Learning", "Data Science", "DevOps", "Web Development"]
    )
    
    # Upload Profile Picture
    profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
    
    # Terms & Conditions
    agree = st.checkbox("I agree to the Terms & Conditions")
    
    # Submit button
    submit_button = st.form_submit_button(label="Register")

# --- Form Handling ---
if submit_button:
    # Validation
    if not first_name or not last_name or not email or not password or not confirm_password:
        st.error("Please fill in all required fields!")
    elif password != confirm_password:
        st.error("Passwords do not match!")
    elif not agree:
        st.warning("You must agree to the Terms & Conditions")
    else:
        st.success(f"🎉 Registration Successful! Welcome, {first_name} {last_name}")
        
        # Display info
        st.markdown("### Your Information:")
        st.write(f"**Full Name:** {first_name} {last_name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Date of Birth:** {dob.strftime('%d-%b-%Y')}")
        st.write(f"**Country:** {country}")
        st.write(f"**Interests:** {', '.join(interests) if interests else 'N/A'}")
        
        # Display profile picture
        if profile_pic:
            image = Image.open(profile_pic)
            st.image(image, caption="Profile Picture", use_column_width=True)
        else:
            st.write("No profile picture uploaded.")
            