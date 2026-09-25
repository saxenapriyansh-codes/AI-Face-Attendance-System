import streamlit as st
import pandas as pd

from database import get_all_students, get_attendance_by_date


def show_dashboard():

    st.header("📊 Attendance Dashboard")

    selected_date = st.date_input("📅 Select Attendance Date")

    selected_date_string = selected_date.strftime("%Y-%m-%d")

    students = get_all_students()

    attendance_data = get_attendance_by_date(selected_date_string)

    total_students = len(students)

    present_students = 0

    attendance_rows = []

    for record in attendance_data:

        name = record[1]
        enrollment = record[2]
        attendance_date = record[4]
        attendance_time = record[5]
        status = record[6]

        if status == "Present":
            present_students += 1
            attendance_status = "Present"
        else:
            attendance_status = "Absent"

        attendance_rows.append(
            [
                name,
                enrollment,
                attendance_date if attendance_date else selected_date_string,
                attendance_time if attendance_time else "-",
                attendance_status
            ]
        )

    absent_students = max(
        total_students - present_students,
        0
    )

    attendance_percentage = (
        (present_students / total_students) * 100
        if total_students > 0
        else 0
    )

    # ==========================================
    # METRICS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "✅ Present",
            present_students
        )

    with col3:
        st.metric(
            "❌ Absent",
            absent_students
        )

    with col4:
        st.metric(
            "📊 Attendance %",
            f"{attendance_percentage:.1f}%"
        )

    st.divider()

    # ==========================================
    # ATTENDANCE OVERVIEW
    # ==========================================

    st.subheader(
        f"📈 Attendance Overview — {selected_date.strftime('%d-%m-%Y')}"
    )

    chart_data = pd.DataFrame(
        {
            "Status": ["Present", "Absent"],
            "Students": [
                present_students,
                absent_students
            ]
        }
    )

    if total_students > 0:

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.bar_chart(
                chart_data.set_index("Status"),
                height=300
            )

        with chart_col2:

            st.write("### 📋 Summary")

            st.write(
                f"**Total Students:** {total_students}"
            )

            st.write(
                f"**Present:** {present_students}"
            )

            st.write(
                f"**Absent:** {absent_students}"
            )

            st.write(
                f"**Attendance Rate:** {attendance_percentage:.1f}%"
            )

    else:

        st.info(
            "No registered students available for attendance analysis."
        )

    st.divider()

    # ==========================================
    # STUDENT-WISE ATTENDANCE
    # ==========================================

    st.subheader(
        f"📅 Attendance for {selected_date.strftime('%d-%m-%Y')}"
    )

    if attendance_rows:

        df = pd.DataFrame(
            attendance_rows,
            columns=[
                "Name",
                "Enrollment",
                "Date",
                "Time",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # ==========================================
        # DATE-WISE CSV DOWNLOAD
        # ==========================================

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download This Date's Attendance",
            data=csv,
            file_name=f"attendance_{selected_date_string}.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No registered students found."
        )