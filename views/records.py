import streamlit as st
import pandas as pd

from database import get_attendance, get_attendance_by_date


def show_records():

    st.header("📊 Attendance Records")

    # ==========================================
    # FILTER
    # ==========================================

    filter_option = st.radio(
        "📅 Attendance Filter",
        ["All Dates", "Specific Date"],
        horizontal=True
    )

    selected_date = None

    if filter_option == "Specific Date":

        selected_date = st.date_input(
            "Select Attendance Date"
        )

    st.divider()

    # ==========================================
    # GET DATA
    # ==========================================

    if filter_option == "Specific Date":

        selected_date_string = selected_date.strftime("%Y-%m-%d")

        attendance = get_attendance_by_date(
            selected_date_string
        )

        # get_attendance_by_date also returns students
        # who were absent, so keep only actual attendance
        attendance = [
            record
            for record in attendance
            if record[6] == "Present"
        ]

    else:

        attendance = get_attendance()

    # ==========================================
    # DISPLAY RECORDS
    # ==========================================

    if attendance:

        if filter_option == "Specific Date":

            df = pd.DataFrame(
                attendance,
                columns=[
                    "ID",
                    "Name",
                    "Enrollment",
                    "Email",
                    "Date",
                    "Time",
                    "Status"
                ]
            )

        else:

            df = pd.DataFrame(
                attendance,
                columns=[
                    "ID",
                    "Name",
                    "Enrollment",
                    "Email",
                    "Date",
                    "Time",
                    "Status"
                ]
            )

        st.subheader(
            f"📋 {len(df)} Attendance Record(s)"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==========================================
        # CSV DOWNLOAD
        # ==========================================

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        if filter_option == "Specific Date":

            file_name = (
                f"attendance_{selected_date.strftime('%Y-%m-%d')}.csv"
            )

            button_label = (
                "📥 Download This Date's Attendance"
            )

        else:

            file_name = "attendance_records.csv"

            button_label = (
                "📥 Download All Attendance"
            )

        st.download_button(
            label=button_label,
            data=csv,
            file_name=file_name,
            mime="text/csv"
        )

    else:

        if filter_option == "Specific Date":

            st.info(
                f"No attendance records found for "
                f"{selected_date.strftime('%d-%m-%Y')}."
            )

        else:

            st.info(
                "No attendance records available."
            )