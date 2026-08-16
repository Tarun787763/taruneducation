import streamlit as st
import sqlite3
import hashlib
import os

# 1. डेटाबेस सेटअप (पम्फलेट इमेज ब्लॉब स्टोर करने के लिए कॉलम जोड़ा गया)
def init_db():
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    
    # यूज़र्स टेबल
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    
    # वैकेंसियां टेबल (pamphlet_bytes और file_name सपोर्ट के साथ)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            last_date TEXT,
            apply_link TEXT,
            pamphlet_bytes BLOB,
            file_name TEXT,
            views INTEGER DEFAULT 0,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # डिफ़ॉल्ट सुपर एडमिन
    admin_username = "admin"
    admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        (admin_username, admin_password_hash, "Admin")
    )
    conn.commit()
    conn.close()

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    hashed_password = hash_pass(password)
    cur.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    result = cur.fetchone()
    conn.close()
    return result if result else None

def register_user(username, password):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    hashed_password = hash_pass(password)
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'Student')", (username, hashed_password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

# वैकेंसियों के साथ पम्फलेट सेव करना
def add_vacancy(title, description, last_date, apply_link, pamphlet_bytes, file_name):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO vacancies (title, description, last_date, apply_link, pamphlet_bytes, file_name) VALUES (?, ?, ?, ?, ?, ?)", 
                (title, description, last_date, apply_link, pamphlet_bytes, file_name))
    conn.commit()
    conn.close()

def get_all_vacancies(search_query=""):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    if search_query:
        cur.execute("SELECT id, title, description, last_date, apply_link, pamphlet_bytes, file_name, views, date_added FROM vacancies WHERE title LIKE ? OR description LIKE ? ORDER BY id DESC", 
                    (f"%{search_query}%", f"%{search_query}%"))
    else:
        cur.execute("SELECT id, title, description, last_date, apply_link, pamphlet_bytes, file_name, views, date_added FROM vacancies ORDER BY id DESC")
    vacancies = cur.fetchall()
    conn.close()
    return vacancies

def increment_views(v_id):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    cur.execute("UPDATE vacancies SET views = views + 1 WHERE id = ?", (v_id,))
    conn.commit()
    conn.close()

def delete_vacancy(v_id):
    conn = sqlite3.connect("job_hub_premium_v3.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM vacancies WHERE id = ?", (v_id,))
    conn.commit()
    conn.close()

init_db()

# --- STREAMLIT UI कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Premium Job & Info Hub", page_icon="🚀", layout="wide")

# परमानेंट लॉगिन स्टेट हैंडलिंग (URL पैरामीटर्स के साथ)
params = st.query_params

if "logged_in" not in st.session_state:
    if "user" in params and "role" in params:
        st.session_state.logged_in = True
        st.session_state.username = params["user"]
        st.session_state.role = params["role"]
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

# लॉगिन/रजिस्ट्रेशन स्क्रीन
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🎓 Information & Vacancy Portal</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 सुरक्षित लॉगिन", "📝 नया छात्र रजिस्ट्रेशन"])
        
        with tab1:
            l_user = st.text_input("यूज़रनेम (Username)", key="l_user")
            l_pass = st.text_input("पासवर्ड (Password)", type="password", key="l_pass")
            if st.button("डैशबोर्ड खोलें", use_container_width=True, type="primary"):
                if l_user and l_pass:
                    role = login_user(l_user, l_pass)
                    if role:
                        st.session_state.logged_in = True
                        st.session_state.username = l_user
                        st.session_state.role = role
                        st.query_params["user"] = l_user
                        st.query_params["role"] = role
                        st.rerun()
                    else:
                        st.error("गलत यूज़रनेम या पासवर्ड!")
                else:
                    st.warning("कृपया दोनों फ़ील्ड भरें।")
                    
        with tab2:
            r_user = st.text_input("नया यूज़रनेम चुनें", key="r_user")
            r_pass = st.text_input("मजबूत पासवर्ड बनाएँ", type="password", key="r_pass")
            if st.button("खाता बनाएँ", use_container_width=True):
                if r_user and r_pass:
                    if register_user(r_user, r_pass):
                        st.success("रजिस्ट्रेशन सफल! अब लॉगिन करें।")
                    else:
                        st.error("यह यूज़रनेम पहले से मौजूद है।")
                else:
                    st.warning("कृपया सभी फ़ील्ड भरें।")

# लॉगिन के बाद मुख्य डैशबोर्ड एरिया
else:
    st.sidebar.markdown(f"### 👤 स्वागत है, *{st.session_state.username}*")
    st.sidebar.info(f"💼 रोल: {st.session_state.role}")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔴 सुरक्षित लॉग आउट (Log Out)", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.query_params.clear()
        st.rerun()

    # --- ए. एडमिन कंट्रोल डैशबोर्ड ---
    if st.session_state.role == "Admin":
        st.title("🛠️ प्रीमियम एडमिन कंट्रोल पैनल")
        
        adm_tab1, adm_tab2 = st.tabs(["➕ नई भर्ती & पम्फलेट जोड़ें", "⚙️ वैकेंसियां डिलीट करें"])
        
        with adm_tab1:
            st.subheader("📝 नई वैकेंसी और पम्फलेट अपलोड फॉर्म")
            col_a, col_b = st.columns(2)
            with col_a:
                v_title = st.text_input("वैकेंसी का शीर्षक (e.g., Rajasthan Police Bharti 2026)")
                v_last_date = st.text_input("आवेदन की अंतिम तिथि (e.g., 30-10-2026)")
            with col_b:
                v_link = st.text_input("अप्लाई करने का डायरेक्ट लिंक (Optional)")
                # पम्फलेट/इमेज अपलोडर टूल
                uploaded_file = st.file_uploader("🖼️ वैकेंसी का पम्फलेट/नोटिफिकेशन इमेज अपलोड करें", type=["png", "jpg", "jpeg"])
                
            v_desc = st.text_area("भर्ती की पूरी जानकारी (शॉर्ट में विवरण लिखें)")
            
            if st.button("🌐 वैकेंसी लाइव (Publish) करें", type="primary"):
                if v_title and v_desc and v_last_date:
                    file_bytes = None
                    file_name = None
                    if uploaded_file is not None:
                        file_bytes = uploaded_file.read()
                        file_name = uploaded_file.name
                    
                    add_vacancy(v_title, v_desc, v_last_date, v_link, file_bytes, file_name)
                    st.success("बधाई हो! पम्फलेट के साथ नई वैकेंसी पोर्टल पर लाइव हो चुकी है।")
                    st.rerun()
                else:
                    st.warning("कृपया शीर्षक, विवरण और अंतिम तिथि ज़रूर भरें।")
                    
        with adm_tab2:
            st.subheader("📋 एक्टिव वैकेंसियों की सूची")
            adm_vacancies = get_all_vacancies()
            if adm_vacancies:
                for v_id, title, desc, last_date, link, pb, fn, views, date_added in adm_vacancies:
                    col_x, col_y = st.columns([4,1])
                    with col_x:
                        st.markdown(f"*📌 {title}* (अंतिम तिथि: {last_date}) | 👁️ व्यूज: {views} {'🖼️ (पम्फलेट अटैच है)' if pb else ''}")
                    with col_y:
                        if st.button("🗑️ डिलीट", key=f"del_{v_id}"):
                            delete_vacancy(v_id)
                            st.error("वैकेंसी हटा दी गई!")
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("फिलहाल पोर्टल पर कोई वैकेंसी नहीं है।")

    # --- बी. स्टूडेंट लाइव डैशबोर्ड ---
    else:
        st.title("🎯 लाइव स्टूडेंट वैकेंसी डैशबोर्ड")
        
        search_query = st.text_input("🔍 अपनी मनपसंद जॉब का नाम खोजें...", "")
        vacancies_list = get_all_vacancies(search_query)
        
        if vacancies_list:
            for v_id, title, desc, last_date, link, p_bytes, f_name, views, date_added in vacancies_list:
                increment_views(v_id)
                
                with st.container(border=True):
                    col_l, col_r = st.columns([3,1])
                    with col_l:
                        st.markdown(f"## 📌 {title}")
                        st.caption(f"📅 पोस्ट: {date_added} | 👁️ {views+1} छात्र देख चुके हैं")
                    with col_r:
                        st.markdown(f"<h4 style='color: red; text-align: right;'>⏳ अंतिम तिथि: {last_date}</h4>", unsafe_allow_html=True)
