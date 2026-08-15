import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIGURATION & PREMIUM DESIGN (CSS) ---
st.set_page_config(page_title="Information with Tarun", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F3F4F6; }
    
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
        transition: transform 0.2s;
    }
    .vacancy-title {
        color: #1E3A8A;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
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
    </style>
""", unsafe_allow_html=True)

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

# --- 3. SIDEBAR: REGISTER & LOGIN SYSTEM ---
st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 User Portal</h2>", unsafe_allow_html=True)

if st.session_state.logged_in_user is None:
    auth_mode = st.sidebar.selectbox("Choose Action", ["Login", "Register"])
    
    if auth_mode == "Register":
        st.sidebar.subheader("Create Account")
        reg_user = st.sidebar.text_input("Username", key="reg_u").strip()
        reg_pass = st.sidebar.text_input("Password", type="password", key="reg_p")
        reg_role = st.sidebar.selectbox("Join As", ["Student", "Admin"])
        
        if st.sidebar.button("Sign Up"):
            if reg_user and reg_pass:
                if reg_user in st.session_state.users:
                    st.sidebar.error("Username already exists!")
                else:
                    st.session_state.users[reg_user] = {"password": reg_pass, "role": reg_role}
                    st.sidebar.success("Registration Successful! Please Login.")
            else:
                st.sidebar.warning("Please fill all fields.")

    elif auth_mode == "Login":
        st.sidebar.subheader("Account Login")
        login_user = st.sidebar.text_input("Username", key="log_u").strip()
        login_pass = st.sidebar.text_input("Password", type="password", key="log_p")
        
        if st.sidebar.button("Login"):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in_user = {
                    "username": login_user,
                    "role": st.session_state.users[login_user]["role"]
                }
                st.rerun()
            else:
                st.sidebar.error("Invalid Username or Password!")
else:
    st.sidebar.success(f"Logged in as: *{st.session_state.logged_in_user['username']}* ({st.session_state.logged_in_user['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

# --- 4. MAIN APP INTERFACE ---
st.markdown("<div class='main-title'>Information with Tarun</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Latest Vacancies, Syllabus & Smart Support Panel</div>", unsafe_allow_html=True)

if st.session_state.logged_in_user is None:
    st.info("👋 Please Login or Register from the Sidebar to access the features.")
else:
    user_role = st.session_state.logged_in_user["role"]
    
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
                        st.session_state.vacancies.append({
                            "id": new_id,
                            "title": v_title,
                            "last_date": str(v_date),
                            "docs": v_docs,
                            "syllabus": v_syllabus,
                            "link": v_link,
                            "pamphlet": v_pamphlet
                        })
                        st.success(f"'{v_title}' Added Successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill required fields (Title, Documents, Link).")
            
            st.markdown("### 🗑️ Delete Existing Vacancy")
            if st.session_state.vacancies:
                delete_options = {v["title"]: v["id"] for v in st.session_state.vacancies}
                to_delete = st.selectbox("Select Vacancy to Delete", list(delete_options.keys()))
                if st.button("Delete Selected Job", type="primary"):
                    st.session_state.vacancies = [v for v in st.session_state.vacancies if v["id"] != delete_options[to_delete]]
                    st.success("Vacancy successfully deleted!")
                    st.rerun()

    # --- TAB 3: LIVE DOUBT CHATBOX ---
    chat_tab_index = 2 if user_role == "Admin" else 1
    with tabs[chat_tab_index]:
        st.subheader("💬 Live Support Chatbox")
        
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "Admin":
                    st.markdown(f"<div class='chat-bubble-admin'><b>🧔 {message['user']}:</b><br>{message['msg']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble-user'><b>🎓 {message['user']}:</b><br>{message['msg']}</div>", unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_display_name = st.session_state.logged_in_user["username"]
            if user_role == "Admin":
                user_display_name = f"Admin ({user_display_name})"
