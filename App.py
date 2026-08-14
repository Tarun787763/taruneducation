import streamlit as st

st.set_page_config(page_title="Tarun Education", layout="wide")

if "videos" not in st.session_state:
    st.session_state.videos = {
        "Paid Course": ["https://w3schools.com"],
        "Recorded Class": ["https://w3schools.com"]
    }
if "syllabus" not in st.session_state:
    st.session_state.syllabus = ["Maths - Chapter 1", "Science - Chapter 1"]
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "users" not in st.session_state:
    st.session_state.users = {"student@email.com": "password123"}

st.sidebar.title("📚 Tarun Education")
page = st.sidebar.radio("Navigation", ["Home / Login", "Live Classes", "Recorded Classes", "Paid Courses", "Syllabus", "Chat Box", "Admin Panel"])

if page == "Home / Login":
    st.title("👋 Welcome to Tarun Education")
    st.subheader("👨‍🎓 Student Login")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email in st.session_state.users and st.session_state.users[email] == password:
            st.success("Login Successful!")
        else:
            st.error("Invalid Email or Password! (Use: student@email.com / password123)")

elif page == "Live Classes":
    st.title("🎥 Live Classroom")
    st.warning("No live classes are running at the moment.")
    st.video("https://youtube.com")

elif page == "Recorded Classes":
    st.title("自由 Free Recorded Classes")
    for idx, vid in enumerate(st.session_state.videos["Recorded Class"]):
        st.write(f"Video #{idx+1}")
        st.video(vid)

elif page == "Paid Courses":
    st.title("💎 Premium Paid Courses")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://unsplash.com", width=300)
        st.subheader("Target Batch 2026")
        st.write("Price: INR 999")
        if st.button("Buy Now", key="buy_btn"):
            st.success("Payment Gateway Link.")
            
    with col2:
        st.write("🔑 Your purchased course videos:")
        for vid in st.session_state.videos["Paid Course"]:
            st.video(vid)

elif page == "Syllabus":
    st.title("📋 Exam Syllabus")
    for item in st.session_state.syllabus:
        st.markdown(f"- *{item}*")

elif page == "Chat Box":
    st.title("💬 Student Doubt Chat Box")
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])
            
    user_msg = st.chat_input("Ask your doubt here...")
    if user_msg:
        st.session_state.chat_messages.append({"role": "user", "text": user_msg})
        st.session_state.chat_messages.append({"role": "assistant", "text": "Your query has been sent to the admin. You will receive a reply shortly."})
        st.rerun()

elif page == "Admin Panel":
    st.title("🔒 Admin Control Center")
    admin_password = st.text_input("Enter Admin Secret Password", type="password")
    
    if admin_password == "tarun786":
        st.success("Admin Access Granted!")
        
        st.header("📤 Upload New Video")
        video_type = st.selectbox("Select Video Type", ["Recorded Class", "Paid Course"])
        video_url = st.text_input("Paste Video MP4 URL or YouTube Link")
        
        if st.button("Upload Video"):
            if video_url:
                st.session_state.videos[video_type].append(video_url)
                st.success(f"Successfully added video to {video_type}!")
            else:
                st.error("Please enter a valid video link.")
                
        st.header("📝 Add New Syllabus Topic")
        new_sub = st.text_input("Topic Name")
        if st.button("Add Topic"):
            if new_sub:
                st.session_state.syllabus.append(new_sub)
                st.success("Syllabus updated successfully!")
    
    elif admin_password != "":
        st.error("Wrong password! Access denied.")

