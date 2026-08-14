import streamlit as st
import datetime

# 1. ऐप सेटिंग्स
st.set_page_config(
    page_title="स्मार्ट डिजिटल एकेडमी प्रो", 
    page_icon="🎓", 
    layout="wide"
)

# ऐप की सुंदर डिज़ाइन (CSS Styling)
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#1E3A8A; text-align:center; margin-bottom:5px; }
    .sub-title { font-size:18px; color:#4B5563; text-align:center; margin-bottom:25px; }
    .section-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 25px; }
    .feature-header { font-size:24px; font-weight:bold; color:#0F172A; margin-bottom:15px; border-bottom: 2px solid #3B82F6; padding-bottom:5px; }
    .price-tag { font-size: 20px; font-weight: bold; color: #10B981; }
    </style>
    """, unsafe_allow_html=True)

# मुख्य हेडर
st.markdown('<div class="main-title">🚀 स्मार्ट डिजिटल एकेडमी प्रो</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">लाइव क्लास, रिकॉर्डेड कोर्सेज, पेड कोर्सेज और नोट्स - सब कुछ एक ही स्थान पर</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 1: स्टूडेंट लॉगिन और प्रोफाइल
# =========================================================
st.markdown('<div class="feature-header">👤 स्टूडेंट लॉगिन और प्रोफाइल</div>', unsafe_allow_html=True)
st.markdown('<div class="section-box">', unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    student_name = st.text_input("अपना नाम दर्ज करें:", value="रमेश कुमार")
with col_p2:
    student_id = st.text_input("स्टूडेंट रोल नंबर / ID:", value="STD-2026-89")
with col_p3:
    st.write("*अकाउंट स्टेटस:*")
    st.success("🟢 प्रीमियम सदस्य (Premium Student)")
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 2: नोटिस बोर्ड
# =========================================================
st.markdown('<div class="feature-header">📢 नोटिस बोर्ड (Announcements)</div>', unsafe_allow_html=True)
st.info("🔔 *महत्वपूर्ण सूचना:* आज रात 9:00 बजे नया 'पेड深度 कोर्स' लाइव होने जा रहा है। सीमित सीटें उपलब्ध हैं।")
st.warning("⚠️ *अपडेट:* इस रविवार को सुबह 10:00 बजे 'पायथन का लाइव मेगा टेस्ट' होगा।")
st.write("---")

# =========================================================
# फीचर 3: लाइव क्लास रूम
# =========================================================
st.markdown('<div class="feature-header">📹 लाइव क्लास रूम (Live Classes)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-box">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    live_class_url = "https://jit.si" 
    st.write("🔴 *लाइव क्लास में शामिल होने के लिए नीचे दिए गए बटन पर क्लिक करें:*")
    st.link_button("🚀 अभी लाइव क्लास जॉइन करें", live_class_url, use_container_width=True)
with col2:
    st.write("⏰ *आज की क्लास का समय:*")
    st.success("रोजाना सुबह 11:00 AM से 12:30 PM (पायथन बेसिक्स)")

with st.expander("📸 अपने मोबाइल का कामना और माइक टेस्ट करें (क्लास जॉइन करने से पहले)"):
    try:
        from streamlit_webrtc import streamlit_webrtc_wrapper
        streamlit_webrtc_wrapper(key="live-stream")
    except ImportError:
        st.info("नोट: कैमरा टेस्ट चालू करने के लिए requirements.txt में streamlit-webrtc जोड़ें।")
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 4: प्रीमियम / पेड कोर्सेज
# =========================================================
st.markdown('<div class="feature-header">💎 प्रीमियम पेड कोर्सेज (Paid Courses)</div>', unsafe_allow_html=True)
st.write("विशेष तैयारी के लिए हमारे बेस्ट सेलिंग प्रीमियम कोर्सेज में शामिल हों:")

col_c1, col_c2 = st.columns(2)
with col_c1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.image("https://unsplash.com", width=250, caption="कोडिंग सीखें")
    st.markdown("### *1. मास्टर इन पायथन (Complete Guide)*")
    st.write("• बेसिक से एडवांस कोडिंग, 20+ लाइव प्रोजेक्ट्स और सर्टिफिकेट।")
    st.markdown('<span class="price-tag">💰 कीमत: ₹499/- (Life Time Access)</span>', unsafe_allow_html=True)
    st.link_button("💳 कोर्स खरीदें (Buy Now)", "https://pwebintoapp.com", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.image("https://unsplash.com", width=250, caption="डेटा विज्ञान")
    st.markdown("### *2. डेटा साइंस और AI (Artificial Intelligence)*")
    st.write("• मशीन लर्निंग, डेटा एनालिसिस और कंपनियों में प्लेसमेंट सपोर्ट।")
    st.markdown('<span class="price-tag">💰 कीमत: ₹999/- (1 Year Access)</span>', unsafe_allow_html=True)
    st.link_button("💳 कोर्स खरीदें (Buy Now)", "https://pwebintoapp.com", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 5: रिकॉर्डेड कोर्सेज
# =========================================================
st.markdown('<div class="feature-header">📺 रिकॉर्डेड कोर्सेज (Recorded Lectures)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.write("यदि आपकी कोई लाइव क्लास छूट गई है, तो पुराने सभी वीडियो लेक्चर्स यहाँ देखें:")

courses_database = {
    "पायथन लेक्चर 1: सॉफ्टवेयर इंस्टॉलेशन और पहला प्रोग्राम": "https://w3schools.com", 
    "पायथन लेक्चर 2: वेरिएबल्स और डेटा इनपुट": "https://w3schools.com",
    "पायथन लेक्चर 3: फंक्शन्स और कोडिंग प्रैक्टिस": "https://zencdn.net"
}

selected_lecture = st.selectbox("आपको कौन सा लेक्चर देखना है? चुनें:", list(courses_database.keys()))
st.write(f"🎬 *अब चल रहा है:* {selected_lecture}")
st.video(courses_database[selected_lecture])
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 6: सिलेबस और पीडीएफ नोट्स
# =========================================================
st.markdown('<div class="feature-header">📑 कोर्स सिलेबस और पीडीएफ नोट्स (PDF Material)</div>', unsafe_allow_html=True)
st.write("चैप्टर के अनुसार सिलेबस देखें और पढ़ाई के लिए पीडीएफ डाउनलोड करें:")

with st.expander("📚 चैप्टर 1: परिचय (Python Intro) - सिलेबस और पीडीएफ देखें"):
    st.markdown("""
    * *विषय 1.1:* वेरिएबल्स, डेटा टाइप्स और ऑपरेटर्स क्या हैं?
    * *विषय 1.2:* इफ-एल्स (If-Else) कंडीशनल स्टेटमेंट्स
    * *विषय 1.3:* लूप्स का इस्तेमाल (For और While Loops)
    """)
    st.download_button(
        label="📥 चैप्टर 1 के पीडीएफ नोट्स डाउनलोड करें", 
        data="यह चैप्टर 1 के स्टडी नोट्स की पीडीएफ फाइल का सैंपल डेटा है।", 
        file_name="python_chapter1_notes.pdf",
        mime="application/pdf"
    )

with st.expander("📚 चैप्टर 2: ऑब्जेक्ट ओरिएंटेड प्रोग्रामिंग (OOPs) - सिलेबस और पीडीएफ देखें"):
    st.markdown("""
    * *विषय 2.1:* क्लासेस और ऑब्जेक्ट्स का बेसिक (Classes & Objects)
    * *विषय 2.2:* इनहेरिटेंस और पॉलीमॉर्फिज्म (Inheritance)
    """)
    st.download_button(
        label="📥 चैप्टर 2 के पीडीएफ नोट्स डाउनलोड करें", 
        data="यह चैप्टर 2 के स्टडी नोट्स की पीडीएफ फाइल का सैंपल डेटा है।", 
        file_name="python_chapter2_notes.pdf",
        mime="application/pdf"
    )
st.write("---")

# =========================================================
# फीचर 7: ऑनलाइन टेस्ट / क्विज़
# =========================================================
st.markdown('<div class="feature-header">📝 ऑनलाइन प्रैक्टिस टेस्ट (Quiz Exam)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-box">', unsafe_allow_html=True)
score = 0

st.markdown("##### *प्रश्न 1: Python का आविष्कार किसने किया था?*")
q1 = st.radio("सही विकल्प चुनें:", ["Dennis Ritchie", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"], key="q1")
if q1 == "Guido van Rossum":
    score += 1
    
st.markdown("##### *प्रश्न 2: इनमें से कौन सा डेटा टाइप Python में नहीं है?*")
q2 = st.radio("सही विकल्प चुनें:", ["List", "Dictionary", "Tuple", "Array (Built-in)"], key="q2")
if q2 == "Array (Built-in)":
    score += 1
    
if st.button("अपना टेस्ट सबमिट करें", use_container_width=True):
    st.metric(label="आपका फाइनल स्कोर", value=f"{score} / 2")
    if score == 2:
        st.balloons()
        st.success("🏆 बधाई हो! आपने सभी प्रश्नों के सही उत्तर दिए हैं।")
    else:
        st.warning("📖 थोड़ा और अभ्यास करें! आप अगले टेस्ट में बेहतर कर सकते हैं।")
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

# =========================================================
# फीचर 8: चैट बॉक्स और डाउट सपोर्ट
# =========================================================
st.markdown('<div class="feature-header">💬 स्टूडेंट डाउट चैट बॉक्स (Help & Support)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-box">', unsafe_allow_html=True)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
c1, c2 = st.columns(2)
with c1:
    current_user = st.text_input("चैट में आपका नाम:", value=student_name, disabled=True)
with c2:
    user_msg = st.text_input("अपना सवाल या समस्या यहाँ लिखें और बटन दबाएं:")

if st.button("मैसेज भेजें (Send Message)", use_container_width=True):
    if user_msg:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        st.session_state.chat_history.append(f"👤 *{current_user}* ({time_now}): {user_msg}")
        st.success("आपका मैसेज भेज दिया गया है!")
    else:
        st.error("मैसेज बॉक्स खाली है, कृपया कुछ लिखें।")
        
st.write("💬 *लाइव चैट बोर्ड (Chat Board):*")
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):
        st.info(chat)
else:
    st.info("अभी तक कोई बातचीत नहीं हुई है। अपना पहला सवाल ऊपर पूछें।")
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")
