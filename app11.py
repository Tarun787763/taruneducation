import streamlit as st
import sqlite3
import hashlib

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("job_hub_premium_v4.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies(
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

    admin_pass = hashlib.sha256("admin123".encode()).hexdigest()

    # हमेशा एडमिन अपडेट रहेगा
    cur.execute("DELETE FROM users WHERE username='admin'")
    cur.execute(
        "INSERT INTO users VALUES(?,?,?)",
        ("admin", admin_pass, "Admin")
    )

    conn.commit()
    conn.close()


def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hash_pass(password))
    )

    data = cur.fetchone()
    conn.close()

    if data:
        return data[0]
    return None


def register_user(username, password):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users VALUES(?,?,?)",
            (username, hash_pass(password), "Student")
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def add_vacancy(title, desc, last_date, link, img, name):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO vacancies
    (title,description,last_date,apply_link,pamphlet_bytes,file_name)
    VALUES(?,?,?,?,?,?)
    """, (title, desc, last_date, link, img, name))

    conn.commit()
    conn.close()


def get_vacancies(search=""):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    if search:
        cur.execute("""
        SELECT * FROM vacancies
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%"))
    else:
        cur.execute("SELECT * FROM vacancies ORDER BY id DESC")

    data = cur.fetchall()
    conn.close()
    return data


def delete_vacancy(v_id):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM vacancies WHERE id=?", (v_id,))

    conn.commit()
    conn.close()


def view(v_id):
    conn = sqlite3.connect("job_hub_premium_v4.db")
    cur = conn.cursor()

    cur.execute("UPDATE vacancies SET views=views+1 WHERE id=?", (v_id,))

    conn.commit()
    conn.close()


init_db()

# ---------------- UI ----------------
st.set_page_config(
    page_title="Information with Tarun",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
.block-container{
padding-top:20px;
padding-bottom:120px;
max-width:100%;
}
.stButton>button{
border-radius:12px;
height:48px;
font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = ""
    st.session_state.role = ""

# ---------------- LOGIN ----------------
if not st.session_state.login:

    st.title("🎓 Information & Vacancy Portal")

    tab = st.radio(
        "",
        ["🔐 लॉगिन", "📝 नया रजिस्ट्रेशन"],
        horizontal=True
    )

    if tab == "🔐 लॉगिन":

        u = st.text_input("यूज़रनेम")
        p = st.text_input("पासवर्ड", type="password")

        if st.button("डैशबोर्ड खोलें", use_container_width=True):

            role = login_user(u, p)

            if role:
                st.session_state.login = True
                st.session_state.user = u
                st.session_state.role = role
                st.rerun()
            else:
                st.error("गलत यूज़रनेम या पासवर्ड!")

    else:

        u = st.text_input("नया यूज़रनेम")
        p = st.text_input("पासवर्ड", type="password")

        if st.button("रजिस्टर करें", use_container_width=True):

            if register_user(u, p):
                st.success("रजिस्ट्रेशन सफल। अब लॉगिन करें।")
            else:
                st.error("यूज़रनेम पहले से मौजूद है।")

# ---------------- DASHBOARD ----------------
else:

    st.sidebar.success(f"👤 {st.session_state.user}")
    st.sidebar.write(st.session_state.role)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.login = False
        st.rerun()

    # ---------- ADMIN ----------
    if st.session_state.role == "Admin":

        st.title("🛠 Admin Panel")

        mode = st.radio(
            "",
            ["➕ Vacancy Add", "🗑 Delete Vacancy"],
            horizontal=True
        )

        if mode == "➕ Vacancy Add":

            title = st.text_input("Vacancy Title")
            last = st.text_input("Last Date")
            link = st.text_input("Apply Link")
            file = st.file_uploader(
                "Pamphlet Upload",
                type=["jpg","jpeg","png"]
            )
            desc = st.text_area("Description")

            if st.button("Publish Vacancy", use_container_width=True):

                if title and desc and last:

                    img = file.read() if file else None
                    name = file.name if file else None

                    add_vacancy(title, desc, last, link, img, name)

                    st.success("Vacancy Publish Successfully")
                    st.rerun()

                else:
                    st.warning("सभी जरूरी जानकारी भरें।")

        else:

            for v in get_vacancies():

                st.markdown(f"### {v[1]}")
                st.caption(v[3])

                if st.button("Delete", key=v[0]):
                    delete_vacancy(v[0])
                    st.rerun()

                st.divider()

    # ---------- STUDENT ----------
    else:

        st.title("📢 Live Vacancies")

        s = st.text_input("Search Vacancy")

        for v in get_vacancies(s):

            view(v[0])

            with st.container(border=True):

                st.subheader(v[1])
                st.write(f"**Last Date:** {v[3]}")
                st.write(v[2])

                if v[5]:
                    st.image(v[5], use_container_width=True)

                    st.download_button(
                        "📥 Download Pamphlet",
                        data=v[5],
                        file_name=v[6],
                        mime="image/jpeg",
                        key=f"d{v[0]}",
                        use_container_width=True
                    )

                if v[4]:
                    st.link_button(
                        "Apply Now",
                        v[4],
                        use_container_width=True
                    )

                st.caption(f"👁 {v[7]+1} Views")
