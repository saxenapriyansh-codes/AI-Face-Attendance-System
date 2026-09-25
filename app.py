import streamlit as st

from database import create_tables

from views.styles import apply_styles
from views.dashboard import show_dashboard
from views.attendance import show_attendance
from views.students import show_students
from views.records import show_records


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Face Attendance",
    page_icon="📸",
    layout="wide"
)


# ==========================================
# DATABASE & STYLING
# ==========================================

create_tables()

apply_styles()


# ==========================================
# APP HEADER
# ==========================================

st.title("📸 AI Face Recognition Attendance System")

st.caption(
    "Automated attendance using OpenCV YuNet + SFace"
)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("📋 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Dashboard",
        "📸 Mark Attendance",
        "👥 Students",
        "📊 Attendance Records"
    ]
)


# ==========================================
# PAGE ROUTING
# ==========================================

if page == "🏠 Dashboard":

    show_dashboard()


elif page == "📸 Mark Attendance":

    show_attendance()


elif page == "👥 Students":

    show_students()


elif page == "📊 Attendance Records":

    show_records()

# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class="project-footer">
        <strong>AI Face Recognition Attendance System</strong><br>
        Built with Python • Streamlit • OpenCV YuNet • SFace • SQLite<br>
        © 2026 Priyansh Saxena
    </div>
    """,
    unsafe_allow_html=True
)