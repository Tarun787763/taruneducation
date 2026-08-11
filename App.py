import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("education.db", check_same_thread=False, timeout=30)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT DEFAULT 'student',
    points INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

try:
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123', 'admin', 0)")
    cursor.execute("INSERT OR IGNORE INTO settings VALUES ('notice', 'कल सुबह 10:00 बजे गणित की महा-मैराथन लाइव क्लास होगी।')")
    cursor.execute("INSERT OR IGNORE INTO settings VALUES ('video_url', 'https://youtube.com')")
    conn.commit()
except:
    pass

st.set_page_config(page_title="Tarun Education", page_icon="🎓", layout="wide")

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = "student"

cursor.execute("SELECT value FROM settings WHERE key='notice'")
current_notice = cursor.fetchone()[0]
cursor.execute("SELECT value FROM settings WHERE key='video_url'")
current_video = cursor.fetchone()[0]

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🎓 Tarun Education</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>प्लेस्टोर एडिशन - डिजिटल लर्निंग प्लेटफॉर्म</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 छात्र लॉगिन (Student Login)", "📝 नया रजिस्ट्रेशन (Sign Up)"])
    
    with tab1:
        st.subheader("अपने रजिस्टर्ड अकाउंट से लॉगिन करें")
        u_name = st.text_input("यूज़रनेम / मोबाइल नंबर", key="l_user")
        u_pass = st.text_input("पासवर्ड (Password)", type="password", key="l_pass")
        
        if st.button("लॉगिन करें (Secure Login)"):
            cursor.execute("SELECT password, role FROM users WHERE username=?", (u_name,))
            user_data = cursor.fetchone()
            
            if user_data and user_data[0] == u_pass:
                st.session_state.logged_in = True
                st.session_state.username = u_name
                st.session_state.role = user_data[1]
                st.success("लॉगिन सफल! डैशबोर्ड खुल रहा है...")
                st.rerun()
            else:
                st.error("गलत यूज़रनेम या पासवर्ड! कृपया दोबारा जांचें।")
                
    with tab2:
        st.subheader("कोचिंग में नया एडमिशन लें")
        reg_name = st.text_input("अपना नया यूज़रनेम बनाएं", key="r_user")
        reg_pass = st.text_input("एक मजबूत पासवर्ड सेट करें", type="password", key="r_pass")
        
        if st.button("अकाउंट सुरक्षित करें (Register)"):
            if reg_name and reg_pass:
                try:
                    cursor.execute("INSERT INTO users (username, password, role, points) VALUES (?, ?, 'student', 0)", (reg_name, reg_pass))
                    conn.commit()
                    st.balloons()
                    st.success("🎉 रजिस्ट्रेशन सफल! अब लॉगिन टैब पर जाकर अपना अकाउंट खोलें।")
                except sqlite3.IntegrityError:
                    st.error("यह यूज़रनेम पहले से किसी और छात्र का है। कुछ अलग नाम चुनें।")
            else:
                st.warning("कृपया दोनों बॉक्स में जानकारी भरें।")

else:
    # लॉगआउट बटन
    if st.sidebar.button("🚪 ऐप बंद करें (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "student"
        st.rerun()
        
    st.sidebar.markdown(f"### 👤 यूज़र: {st.session_state.username.upper()}")
    
    if st.session_state.role == "admin":
        st.title("👑 तरूण एजुकेशन - ओनर कंट्रोल पैनल")
        st.sidebar.success("मोड: मुख्य व्यवस्थापक (Admin)")
        
        admin_opt = st.sidebar.radio("कंट्रोल सेटिंग्स", ["👥 छात्र मैनेजमेंट", "📢 लाइव नोटिस बोर्ड", "🎬 वीडियो लेक्चर बदलें"])
        
        if admin_opt == "👥 छात्र मैनेजमेंट":
            st.header("👥 ऐप पर पंजीकृत असली छात्र")
            st.write("यह डेटा आपके असली डेटाबेस (SQLite) से लाइव आ रहा है:")
            
            df = pd.read_sql_query("SELECT username, role, points FROM users WHERE role='student'", conn)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("अभी तक किसी छात्र ने रजिस्टर नहीं किया है।")
                
        elif admin_opt == "📢 लाइव नोटिस बोर्ड":
            st.header("📢 सभी छात्रों के लिए नया नोटिस जारी करें")
            new_not = st.text_area("नोटिस का मैटर यहाँ टाइप करें:", value=current_notice)
            if st.button("तुरंत पब्लिश करें"):
                cursor.execute("UPDATE settings SET value=? WHERE key='notice'", (new_not,))
                conn.commit()
                st.success("नोटिस डेटाबेस में सुरक्षित हो गया! सभी छात्रों को अब यही दिखेगा।")
                
        elif admin_opt == "🎬 वीडियो लेक्चर बदलें":
            st.header("🎬 क्लास का वीडियो बदलें")
            new_vid = st.text_input("नया YouTube वीडियो लिंक यहाँ डालें:", value=current_video)
            if st.button("वीडियो अपडेट करें"):
                cursor.execute("UPDATE settings SET value=? WHERE key='video_url'", (new_vid,))
                conn.commit()
                st.success("वीडियो लिंक बदल दिया गया है!")

    else:
        st.title("🎓 Tarun Education डिजिटल क्लासरूम")
        st.sidebar.info("बैच: सामान्य प्रतियोगिता परीक्षा")
        
        stud_opt = st.sidebar.radio("पढ़ाई मेनू", ["🏠 होम / नोटिस बोर्ड", "🔴 वीडियो क्लास रूम", "🏆 लीडरबोर्ड"])
        
        if stud_opt == "🏠 होम / नोटिस बोर्ड":
            st.subheader("📢 कोचिंग की तरफ से महत्वपूर्ण सूचना:")
            st.info(current_notice) 
            
            
            cursor.execute("SELECT points FROM users WHERE username=?", (st.session_state.username,))
            my_pts = cursor.fetchone()[0]
            st.metric(label="🎯 आपके टेस्ट पॉइंट्स", value=f"{my_pts} XP")
            
        elif stud_opt == "🔴 वीडियो क्लास रूम":
            st.subheader("📺 आज का वीडियो लेक्चर")
            st.video(current_video) 
            
            
            st.markdown("---")
            st.subheader("✍️ क्लास अटेंडेंस टेस्ट")
            ans = st.radio("पायथन एक किस प्रकार की भाषा है?", ["प्रोग्रामिंग भाषा", "हार्डवेयर"])
            if st.button("जवाब लॉक करें"):
                if ans == "प्रोग्रामिंग भाषा":
                    cursor.execute("UPDATE users SET points = points + 10 WHERE username=?", (st.session_state.username,))
                    conn.commit()
                    st.success("सही जवाब! डेटाबेस में आपके +10 पॉइंट्स जोड़ दिए गए हैं। होम पर जाकर चेक करें।")
                else:
                    st.error("गलत जवाब, दोबारा कोशिश करें।")
                    
        elif stud_opt == "🏆 लीडरबोर्ड":
            st.subheader("🥇 टॉपर्स लीडरबोर्ड")
            df_leader = pd.read_sql_query("SELECT username as 'छात्र का नाम', points as 'पॉइंट्स' FROM users WHERE role='student' ORDER BY points DESC", conn)
            st.table(df_leader)
