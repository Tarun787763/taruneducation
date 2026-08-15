import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIGURATION & PREMIUM DESIGN (CSS) ---
st.set_page_config(page_title="Information with Tarun", page_icon="🎓", layout="wide")

# CSS: Custom rules to hide Streamlit default menu, deployment buttons, and protect data
st.markdown("""
    <style>
    .stApp { background-color: #F3F4F6; }
    
    /* Hide Streamlit MainMenu, Deploy Button, and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    
    /* Security: Prevent text selection and copying */
    body, .stApp {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    .main-title {
        color: #1E3A8A;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sub-title {
        color: #6B7280;
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .vacancy-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #3B82F6;
        margin-bottom: 25px;
    }
    .vacancy-title {
        color: #1E3A8A;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .scroll-chat-box {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        background-color: #FFFFFF;
        margin-bottom: 15px;
    }
    
    .chat-bubble-user {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 12px;
        border-radius: 12px 12px 0px 12px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-bubble-admin {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 12px;
        border-radius: 12px 12px 12px 0px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    
    .login-container {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 0 auto;
    }

    /* Blank page layout on print preview */
    @media print {
        html, body {
            display: none !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript: Disables right click and basic developer keys/shortcuts
st.components.v1.html("""
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault());

    document.onkeydown = function(e) {
        if(e.keyCode == 123) { return false; }
        if(e.ctrlKey && e.shiftKey && (e.keyCode == 'I'.charCodeAt(0) || e.keyCode == 'J'.charCodeAt(0))) { return false; }
        if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) { return false; }
        if(e.ctrlKey && e.keyCode == 'P'.charCodeAt(0)) { 
            alert("Screenshots / Printing not allowed!");
            return false; 
        }
        if(e.ctrlKey && e.keyCode == 'S'.charCodeAt(0)) { return false; }
    };
    </script>
""", height=0, width=0)

# --- 2. INITIALIZE SESSION STATES ---
if "users" not in st.session_state:
    st.session_state.users = {"admin": {"password": "admin123", "role": "Admin"}}
if "vacancies" not in st.session_state:
    st.session_state.vacancies = [
        {
            "id": 1,
            "title": "SSC CGL Recruitment 2026",
            "last_date": "2026-09-15",
            "docs": "Aadhar Card, 10th & Graduation Marksheet, Photo, Signature",
            "syllabus": "Tier 1: Maths, Reasoning, English, GK. Tier 2: Descriptive Paper.",
            "link": "https://ssc.gov.in",
            "pamphlet": None
        }
    ]
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"user": "Rahul", "msg": "Sir, CGL form ki last date kya hai?", "role": "Student"},
        {"user": "Admin (Tarun)", "msg": "Rahul, 15 September se pehle bhar dena.", "role": "Admin"}
    ]
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# --- 3. MAIN APP INTERFACE ---
st.markdown("<div class='main-title'>Information with Tarun</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Latest Vacancies, Syllabus & Smart Support Panel</div>", unsafe_allow_html=True)

if st.session_state.logged_in_user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>🔐 Welcome! Please Login</h3>", unsafe_allow_html=True)
        
        auth_mode = st.selectbox("Choose Action", ["Login", "Register"], label_visibility="collapsed")
        
        if auth_mode == "Login":
            login_user = st.text_input("Username", key="main_log_u").strip()
            login_pass = st.text_input("Password", type="password", key="main_log_p")
            
            if st.button("Login Now", type="primary", use_container_width=True):
                if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                    st.session_state.logged_in_user = {
                        "username": login_user,
                        "role": st.session_state.users[login_user]["role"]
                    }
                    st.rerun()
                else:
                    st.error("Invalid Username or Password!")
                    
        elif auth_mode == "Register":
            reg_user = st.text_input("Choose Username", key="main_reg_u").strip()
            reg_pass = st.text_input("Choose Password", type="password", key="main_reg_p")
            reg_role = st.selectbox("Join As", ["Student", "Admin"])
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if reg_user and reg_pass:
                    if reg_user in st.session_state.users:
                        st.error("Username already exists!")
                    else:
                        st.session_state.users[reg_user] = {"password": reg_pass, "role": reg_role}
                        st.success("Registration Successful! Switch to 'Login' to enter.")
                else:
                    st.warning("Please fill all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. POST-LOGIN INTERFACE ---
else:
    user_role = st.session_state.logged_in_user["role"]
    
    st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A;'>👤 My Profile</h2>", unsafe_allow_html=True)
    st.sidebar.success(f"User: *{st.session_state.logged_in_user['username']}\n\nRole: *{user_role}**")
    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        st.session_state.logged_in_user = None
        st.rerun()

    # 🛠️ टैब इंडेक्स एरर्स को पूरी तरह फ़िक्स किया गया है
    if user_role == "Admin":
        tabs = st.tabs(["📋 Vacancy & Student View", "⚙️ Admin Control Panel", "💬 Doubt Chatbox"])
    else:
        tabs = st.tabs(["📋 Vacancies & Information", "💬 Doubt Chatbox"])

    # --- TAB 1: STUDENT VIEW ---
    with tabs[0]:
        st.subheader("🔍 All Active Job Openings")
        search_query = st.text_input("Search Job Title...", "")
        
        filtered_vacancies = [v for v in st.session_state.vacancies if search_query.lower() in v["title"].lower()]
        
        if not filtered_vacancies:
            st.warning("No vacancies found.")
        
        for idx, vac in enumerate(filtered_vacancies):
            st.markdown(f"""
                <div class='vacancy-card'>
                    <div class='vacancy-title'>📌 {vac['title']}</div>
                    <p style='color: #EF4444; font-weight: 600;'>📅 Last Date to Apply: {vac['last_date']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.expander("📄 Required Documents"):
                    st.write(vac["docs"])
            with col2:
                with st.expander("📚 Syllabus"):
                    st.write(vac["syllabus"])
            with col3:
                with st.expander("🖼️ Pamphlet"):
                    if vac["pamphlet"] is not None:
                        st.image(vac["pamphlet"], use_container_width=True)
                    else:
                        st.caption("No pamphlet uploaded.")
            
            st.markdown(f"[🔗 Apply Online Here]({vac['link']})")
            st.markdown("<hr style='margin: 10px 0 25px 0; border-top: 1px dashed #CCC;'>", unsafe_allow_html=True)

    # --- TAB 2: ADMIN PANEL ---
    if user_role == "Admin":
        with tabs[1]:
            st.subheader("⚙️ Add / Remove Vacancies")
            
            with st.form("add_vacancy_form", clear_on_submit=True):
                st.markdown("### ➕ Add New Vacancy")
                v_title = st.text_input("Vacancy Title")
                v_date = st.date_input("Last Date to Apply", datetime.now())
                v_docs = st.text_area("Required Documents")
                v_syllabus = st.text_area("Syllabus / Exam Pattern")
                v_link = st.text_input("Official Link")
                v_pamphlet = st.file_uploader("Upload Pamphlet / Banner (Image)", type=["png", "jpg", "jpeg"])
                
                submit_btn = st.form_submit_button("Post Vacancy Now")
                
                if submit_btn:
                    if v_title and v_docs and v_link:
                        new_id = len(st.session_state.vacancies) + 1
