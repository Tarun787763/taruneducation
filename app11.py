import streamlit as st
import sqlite3
import os
import hashlib
import uuid
from datetime import date

st.set_page_config(page_title="Information with Tarun", page_icon="🎓", layout="wide")

# ------------------ DATABASE ------------------
DB = "information_with_tarun.db"
IMG_DIR = "uploads"
os.makedirs(IMG_DIR, exist_ok=True)

conn = sqlite3.connect(DB, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
role TEXT)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS vacancies(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
last_date TEXT,
docs TEXT,
syllabus TEXT,
link TEXT,
image TEXT)
""")
conn.commit()

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

cur.execute(
    "INSERT OR IGNORE INTO users VALUES(?,?,?)",
    ("admin", hash_pass("admin123"), "Admin")
)
conn.commit()

# ------------------ CSS ------------------
st.markdown("""
<style>
.stApp{background:#f4f7fb;}
.main-title{
text-align:center;
font-size:40px;
font-weight:800;
color:#0f4c81;
}
.card{
background:white;
padding:20px;
border-radius:18px;
margin:16px 0;
border-left:6px solid #2563eb;
box-shadow:0 4px 12px rgba(0,0,0,.08);
}
html,body,.stApp{
overflow-y:auto!important;
overscroll-behavior-y:contain;
-webkit-overflow-scrolling:touch;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔐 User Portal")

if st.session_state.user is None:

    mode = st.sidebar.radio("Choose", ["Login", "Register"])

    if mode == "Login":
        u = st.sidebar.text_input("Username")
        p = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            row = cur.execute(
                "SELECT role,password FROM users WHERE username=?",
                (u,)
            ).fetchone()

            if row and row[1] == hash_pass(p):
                st.session_state.user = {
                    "username": u,
                    "role": row[0]
                }
                st.rerun()
            else:
                st.sidebar.error("Wrong Username or Password")

    else:
        u = st.sidebar.text_input("New Username")
        p = st.sidebar.text_input("New Password", type="password")

        if st.sidebar.button("Register"):
            try:
                cur.execute(
                    "INSERT INTO users VALUES(?,?,?)",
                    (u, hash_pass(p), "Student")
                )
                conn.commit()
                st.sidebar.success("Registration Successful")
            except sqlite3.IntegrityError:
                st.sidebar.error("Username already exists")

else:
    st.sidebar.success(
        f"{st.session_state.user['username']} ({st.session_state.user['role']})"
    )

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ------------------ HEADER ------------------
st.markdown("<div class='main-title'>Information with Tarun</div>", unsafe_allow_html=True)
st.caption("Latest Government Jobs • Admit Card • Result • Polytechnic Updates")

# ------------------ GUEST ------------------
if st.session_state.user is None:
    st.info("👈 Login या Register करके सभी Government Vacancy देख सकते हैं।")
    st.stop()

role = st.session_state.user["role"]

# ------------------ TABS ------------------
tabs = st.tabs(
    ["🏠 Vacancies", "⚙️ Admin Panel"]
    if role == "Admin"
    else ["🏠 Vacancies"]
)

# ------------------ VACANCIES ------------------
with tabs[0]:

    q = st.text_input("🔍 Search Vacancy")

    rows = cur.execute(
        "SELECT * FROM vacancies WHERE title LIKE ? ORDER BY id DESC",
        (f"%{q}%",)
    ).fetchall()

    if not rows:
        st.warning("No Vacancy Available")

    for r in rows:

        st.markdown(f"""
        <div class='card'>
        <h3>📌 {r[1]}</h3>
        <p>📅 Last Date: <b>{r[2]}</b></p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.expander("📄 Documents"):
                st.write(r[3])

        with c2:
            with st.expander("📚 Syllabus"):
                st.write(r[4])

        with c3:
            with st.expander("🖼️ Pamphlet"):
                if r[6] and os.path.exists(r[6]):
                    st.image(r[6], use_container_width=True)
                else:
                    st.caption("No Image")

        if r[5]:
            st.link_button("🔗 Apply Here", r[5])

        st.divider()

# ------------------ ADMIN PANEL ------------------
if role == "Admin":

    with tabs[1]:

        st.subheader("➕ Add New Vacancy")

        with st.form("add_vacancy", clear_on_submit=True):

            title = st.text_input("Vacancy Title")
            last = st.date_input("Last Date", value=date.today())
            docs = st.text_area("Required Documents")
            syllabus = st.text_area("Syllabus")
            link = st.text_input("Official Link")
            img = st.file_uploader(
                "Pamphlet",
                type=["png", "jpg", "jpeg"]
            )

            submit = st.form_submit_button("Post Vacancy")

            if submit:

                img_path = ""

                if img:
                    ext = img.name.split(".")[-1]
                    img_path = os.path.join(
                        IMG_DIR,
                        f"{uuid.uuid4()}.{ext}"
                    )
                    with open(img_path, "wb") as f:
                        f.write(img.read())

                cur.execute("""
                INSERT INTO vacancies
                (title,last_date,docs,syllabus,link,image)
                VALUES(?,?,?,?,?,?)
                """, (
                    title,
                    str(last),
                    docs,
                    syllabus,
                    link,
                    img_path
                ))

                conn.commit()

                st.success("✅ Vacancy Posted Successfully")
                st.rerun()

        st.subheader("🗑️ Manage Vacancies")

        rows = cur.execute(
            "SELECT id,title,image FROM vacancies ORDER BY id DESC"
        ).fetchall()

        if rows:

            names = [r[1] for r in rows]

            selected = st.selectbox(
                "Select Vacancy",
                names
            )

            if st.button("Delete Vacancy"):

                for r in rows:
                    if r[1] == selected:

                        if r[2] and os.path.exists(r[2]):
                            os.remove(r[2])

                        cur.execute(
                            "DELETE FROM vacancies WHERE id=?",
                            (r[0],)
                        )
                        conn.commit()
                        st.success("Deleted")
                        st.rerun()
