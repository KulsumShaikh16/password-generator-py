import streamlit as st
import random
import string

# Generate password based on user input
def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    # Ensure at least one digit and one special character if selected
    if use_digits and use_special:
        while True:
            password = ''.join(random.choice(characters) for _ in range(length))
            if (any(char.isdigit() for char in password) and 
                any(char in string.punctuation for char in password)):
                break
    else:
        password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Check password strength dynamically
def check_strength(password):
    length = len(password)
    if length >= 12 and any(char in string.punctuation for char in password) and any(char.isdigit() for char in password):
        return "🟢 Strong 💪"
    elif length >= 8:
        return "🟠 Moderate ⚖️"
    else:
        return "🔴 Weak 🚨"

st.title("🔒 Enhanced Password Generator")

# Session state to remember password
if "password" not in st.session_state:
    st.session_state.password = ""
if "password_strength" not in st.session_state:
    st.session_state.password_strength = ""

# Input controls
length = st.slider("Password Length", min_value=6, max_value=32, value=12)
use_digits = st.checkbox("Use Digits")
use_special = st.checkbox("Use Special Characters")

# Password generation and validation
if st.button("Generate Password"):
    if not (use_digits or use_special):
        st.error("Select at least one option: Digits or Special Characters!")
    else:
        st.session_state.password = generate_password(length, use_digits, use_special)
        st.session_state.password_strength = check_strength(st.session_state.password)

# Display generated password and strength
if st.session_state.password:
    st.markdown(f"**Strength:** {st.session_state.password_strength}")

    # Show password toggle
    show_password = st.checkbox("Show Password")
    if show_password:
        st.write(f"**Password:** `{st.session_state.password}`")
    else:
        st.write("**Password:** 🔒 (Hidden)")

    # Copy to clipboard using HTML + JavaScript
    copy_code = f"""
    <input type="text" value="{st.session_state.password}" id="passwordInput" style="display:none;">
    <button onclick="copyToClipboard()">📋 Copy to Clipboard</button>
    <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("passwordInput");
            copyText.style.display = "block";
            copyText.select();
            document.execCommand("copy");
            copyText.style.display = "none";
            alert("Password copied to clipboard! 📋");
        }}
    </script>
    """
    st.components.v1.html(copy_code, height=100)

# Style tweaks
st.markdown(
    """
    <style>
    .stSlider { margin-top: -20px; }
    .stCheckbox, .stButton { margin-top: -10px; }
    </style>
    """, 
    unsafe_allow_html=True
)
