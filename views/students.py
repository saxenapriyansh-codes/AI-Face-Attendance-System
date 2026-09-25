import streamlit as st
import pandas as pd

from database import (
    get_all_students,
    get_student_attendance,
    delete_student
)


def show_students():

    st.header("👥 Student Management")

    students = get_all_students()

    # ==========================================
    # STUDENT COUNT
    # ==========================================

    st.metric(
        "👥 Total Students",
        len(students)
    )

    st.divider()

    if not students:

        st.info("No students registered yet.")

        return

    # ==========================================
    # SEARCH STUDENTS
    # ==========================================

    st.subheader("🔍 Search Students")

    search = st.text_input(
        "Search by name, enrollment or email",
        placeholder="Enter student name, enrollment or email..."
    )

    filtered_students = students

    if search:

        search_text = search.lower().strip()

        filtered_students = [
            student
            for student in students
            if search_text in str(student[1]).lower()
            or search_text in str(student[2]).lower()
            or search_text in str(student[3]).lower()
        ]

    # ==========================================
    # STUDENT TABLE
    # ==========================================

    st.subheader("📋 Registered Students")

    student_data = []

    for student in filtered_students:

        student_data.append(
            [
                student[0],
                student[1],
                student[2],
                student[3],
                "✅ Registered"
                if student[4] is not None
                else "❌ Face Not Registered"
            ]
        )

    if student_data:

        df = pd.DataFrame(
            student_data,
            columns=[
                "ID",
                "Name",
                "Enrollment",
                "Email",
                "Face Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No students found matching your search."
        )

    st.divider()

    # ==========================================
    # DELETE STUDENT
    # ==========================================

    st.subheader("🗑️ Remove Student")

    delete_options = {
        f"{student[1]} — {student[2]}": student[0]
        for student in students
    }

    selected_delete_name = st.selectbox(
        "Select Student to Remove",
        list(delete_options.keys()),
        key="delete_student_select"
    )

    selected_delete_id = delete_options[
        selected_delete_name
    ]

    st.warning(
        "⚠️ Deleting a student will permanently remove "
        "the student profile, face data, and attendance history."
    )

    # ==========================================
    # DELETE CONFIRMATION DIALOG
    # ==========================================

    @st.dialog("⚠️ Confirm Student Deletion")
    def confirm_delete():

        st.warning(
            f"Are you sure you want to permanently delete "
            f"**{selected_delete_name}**?"
        )

        st.write(
            "This will permanently remove:"
        )

        st.write("• Student profile")
        st.write("• Registered face data")
        st.write("• Complete attendance history")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "❌ Cancel",
                use_container_width=True
            ):

                st.rerun()

        with col2:

            if st.button(
                "🗑️ Yes, Delete",
                type="primary",
                use_container_width=True
            ):

                deleted = delete_student(
                    selected_delete_id
                )

                if deleted:

                    st.success(
                        "✅ Student deleted successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Unable to delete student."
                    )

    # ==========================================
    # DELETE BUTTON
    # ==========================================

    if st.button(
        "🗑️ Delete Student",
        key="delete_student_button"
    ):

        confirm_delete()

    st.divider()

    # ==========================================
    # STUDENT ANALYTICS
    # ==========================================

    st.subheader("📊 Student Attendance Analytics")

    student_options = {
        f"{student[1]} — {student[2]}": student[0]
        for student in students
    }

    selected_student_name = st.selectbox(
        "👤 Select Student",
        list(student_options.keys())
    )

    selected_student_id = student_options[
        selected_student_name
    ]

    # ==========================================
    # DATE RANGE
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "📅 Start Date"
        )

    with col2:

        end_date = st.date_input(
            "📅 End Date"
        )

    if start_date > end_date:

        st.error(
            "Start date cannot be after end date."
        )

        return

    # ==========================================
    # ATTENDANCE DATA
    # ==========================================

    attendance = get_student_attendance(
        selected_student_id,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )

    present_days = len(
        [
            record
            for record in attendance
            if record[2] == "Present"
        ]
    )

    working_days = len(
        pd.bdate_range(
            start=start_date,
            end=end_date
        )
    )

    absent_days = max(
        working_days - present_days,
        0
    )

    attendance_percentage = (
        (present_days / working_days) * 100
        if working_days > 0
        else 0
    )

    # ==========================================
    # ANALYTICS METRICS
    # ==========================================

    st.markdown("### 📈 Attendance Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📅 Working Days",
            working_days
        )

    with col2:

        st.metric(
            "✅ Present",
            present_days
        )

    with col3:

        st.metric(
            "❌ Absent",
            absent_days
        )

    with col4:

        st.metric(
            "📊 Attendance %",
            f"{attendance_percentage:.1f}%"
        )

    # ==========================================
    # ATTENDANCE CHART
    # ==========================================

    if working_days > 0:

        chart_data = pd.DataFrame(
            {
                "Status": [
                    "Present",
                    "Absent"
                ],
                "Days": [
                    present_days,
                    absent_days
                ]
            }
        )

        st.markdown("### 📊 Attendance Overview")

        st.bar_chart(
            chart_data.set_index("Status"),
            height=300
        )

    # ==========================================
    # ATTENDANCE HISTORY
    # ==========================================

    st.markdown("### 📋 Attendance History")

    if attendance:

        history_data = []

        for record in attendance:

            history_data.append(
                [
                    record[0],
                    record[1],
                    record[2]
                ]
            )

        history_df = pd.DataFrame(
            history_data,
            columns=[
                "Date",
                "Time",
                "Status"
            ]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No attendance records found for this date range."
        )