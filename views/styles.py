import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* ==============================
           MAIN APP
        ============================== */

        .main {
            padding-top: 1.5rem;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* ==============================
           SIDEBAR
        ============================== */

        section[data-testid="stSidebar"] {
            background: #111827;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: white;
        }


        /* ==============================
           HEADINGS
        ============================== */

        h1 {
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }

        h2 {
            font-weight: 650 !important;
        }

        h3 {
            font-weight: 600 !important;
        }


        /* ==============================
           METRIC CARDS
        ============================== */

        div[data-testid="stMetric"] {
            background: #171b26;
            border: 1px solid #2a3040;
            padding: 1.2rem;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
        }

        div[data-testid="stMetricValue"] {
            font-weight: 700;
        }


        /* ==============================
           BUTTONS
        ============================== */

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 42px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }


        /* ==============================
           DATAFRAMES
        ============================== */

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }


        /* ==============================
           INPUTS
        ============================== */

        div[data-baseweb="input"] {
            border-radius: 10px;
        }

        div[data-baseweb="select"] {
            border-radius: 10px;
        }


        /* ==============================
           ALERTS
        ============================== */

        div[data-testid="stAlert"] {
            border-radius: 10px;
        }


        /* ==============================
           DIVIDER
        ============================== */

        hr {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }


        /* ==============================
           FOOTER
        ============================== */

        .project-footer {
            text-align: center;
            color: #8b92a5;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #2a3040;
        }

        </style>
        """,
        unsafe_allow_html=True
    )