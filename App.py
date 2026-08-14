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
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "quizzes" not in st.session_state:
    st.session_state.quizzes = [
        {
            "question": "What is the capital of India?",
            "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
            "correct": "New Delhi"
        }
    ]
if "past_papers" not in st.session_state:
    st.session_state.past_papers = [
        {"title": "Maths Board Exam 2025", "url": "https://w3.org"}
    ]
if "current_affairs" not in st.session_state:
    st.session_state.current_affairs = [
        {"date": "2026-08-14", "title": "National Space Day Updates", "details": "India celebrates its achievements in space exploration with new mission updates."}
    ]

st.sidebar.title("📚 Tarun Education")

if st.session_state.logged_in_user:
    st.sidebar.write(f"👤 Logged in as: *{st.session_state.logged_in_user}*")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

page = st.sidebar.radio("Navigation", [
    "Home / Authentication", 
    "Live Classes", 
    "Recorded Classes", 
    "Paid Courses", 
    "Current Affairs",
    "Online Quiz Test", 
    "Previous Papers", 
    "Syllabus", 
    "Chat Box", 
    "Admin Panel"
])

if page == "Home / Authentication":
    st.title("👋 Welcome to Tarun Education")
    if st.session_state.logged_in_user:
        st.success(f"You are already logged in as {st.session_state.logged_in_user}! Use sidebar to navigate.")
    else:
        tab1, tab2 = st.tabs(["👨‍🎓 Student Login", "📝 Student Registration (Sign Up)"])
        with tab1:
            st.subheader("Login to Your Account")
            login_email = st.text_input("Email ID", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login_email in st.session_state.users and st.session_state.users[login_email] == login_password:
                    st.session_state.logged_in_user = login_email
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password!")
        with tab2:
            st.subheader("Create a New Account")
            reg_email = st.text_input("Enter Email ID", key="reg_email")
            reg_password = st.text_input("Create Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
            if st.button("Register Now"):
                if not reg_email or not reg_password:
                    st.error("Please fill all fields.")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match!")
                elif reg_email in st.session_state.users:
                    st.error("This Email is already registered!")
                else:
                    st.session_state.users[reg_email] = reg_password
                    st.success("Account created successfully! Now go to Login tab.")

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

elif page == "Current Affairs":
    st.title("📰 Daily Current Affairs Updates")
    if not st.session_state.current_affairs:
        st.info("No updates available for today.")
    else:
        for idx, news in enumerate(reversed(st.session_state.current_affairs)):
            st.subheader(f"📌 {news['title']}")
            st.caption(f"Date: {news['date']}")
            st.write(news['details'])
            st.write("---")

elif page == "Online Quiz Test":
    st.title("✍️ Online Practice Quiz Test")
    if not st.session_state.quizzes:
        st.info("No quiz available right now.")
    else:
        score = 0
        student_answers = {}
        for idx, q in enumerate(st.session_state.quizzes):
            st.markdown(f"*Q{idx+1}. {q['question']}*")
            student_answers[idx] = st.radio(f"Select option for Q{idx+1}:", q['options'], key=f"q_{idx}")
            st.write("---")
        if st.button("Submit Quiz"):
            for idx, q in enumerate(st.session_state.quizzes):
                if student_answers[idx] == q['correct']:
                    score += 1
            st.success(f"🎉 Your Score: {score} / {len(st.session_state.quizzes)}")

elif page == "Previous Papers":
    st.title("📂 Previous Year Question Papers (PDFs)")
    if not st.session_state.past_papers:
        st.info("No past papers uploaded yet.")
    else:
        for paper in st.session_state.past_papers:
            col_p1, col_p2 = st.columns()
            with col_p1:
                st.write(f"📄 *{paper['title']}*")
            with col_p2:
                st.markdown(f"[📥 Download PDF]({paper['url']})", unsafe_allow_html=True)
            st.write("---")

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
        st.session_state.chat_messages.append({"role": "assistant", "text": "Your query has been sent to the admin."})
        st.rerun()

elif page == "Admin Panel":
    st.title("🔒 Admin Control Center")
    admin_password = st.text_input("Enter Admin Secret Password", type="password")
    
    if admin_password == "tarun786":
        st.success("Admin Access Granted!")
        
        st.header("📰 Add Current Affairs")
        ca_date = st.text_input("Date (YYYY-MM-DD)")
        ca_title = st.text_input("News Title")
        ca_details = st.text_area("News Content / Details")
        if st.button("Publish Current Affairs"):
            if ca_date and ca_title and ca_details:
                st.session_state.current_affairs.append({
                    "date": ca_date,
                    "title": ca_title,
                    "details": ca_details
                })
                st.success("Current Affairs Published Successfully!")
            else:
                st.error("Please fill all fields.")
        
        st.header("🎯 Add New Quiz Question")
        q_text = st.text_input("Enter Question")
        opt1 = st.text_input("Option A")
        opt2 = st.text_input("Option B")
        opt3 = st.text_input("Option C")
        opt4 = st.text_input("Option D")
        correct_opt = st.selectbox("Select Correct Answer", [opt1, opt2, opt3, opt4])
        if st.button("Add Question to Quiz"):
            if q_text and opt1 and opt2:
                st.session_state.quizzes.append({
                    "question": q_text,
                    "options": [opt1, opt2, opt3, opt4],
                    "correct": correct_opt
                })
                st.success("Question Added Successfully!")
            else:
                st.error("Please fill question and options.")

        st.header("📂 Upload Previous Year Paper Link")
        paper_title = st.text_input("Paper Title")
        paper_pdf_url = st.text_input("Paste PDF Link")
        if st.button("Upload Paper"):
            if paper_title and paper_pdf_url:
                st.session_state.past_papers.append({"title": paper_title, "url": paper_pdf_url})
                st.success("Paper Link Uploaded Successfully!")
            else:
                st.error("Please fill both Title and PDF URL.")

        st.header("👥 Registered Students")
        for u_email in st.session_state.users.keys():
            st.text(f"• {u_email}")
        
        st.header("📤 Upload New Video")
        video_type = st.selectbox("Select Video Type", ["Recorded Class", "Paid Course"])
        video_url = st.text_input("Paste Video MP4 URL or YouTube Link")
        if st.button("Upload Video"):
            if video_url:
                st.session_state.videos[video_type].append(video_url)
                st.success("Successfully added video!")
                
        st.header("📝 Add New Syllabus Topic")
        new_sub = st.text_input("Topic Name")
        if st.button("Add Topic"):
            if new_sub:
                st.session_state.syllabus.append(new_sub)
