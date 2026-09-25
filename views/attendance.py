import streamlit as st
import cv2
import numpy as np

from database import (
    add_student,
    get_all_students,
    get_student_by_enrollment,
    update_face_data,
    mark_attendance,
    attendance_already_marked
)

from face_utils import (
    detect_face,
    get_face_embedding,
    embedding_to_bytes,
    bytes_to_embedding,
    compare_faces
)


def show_attendance():

    st.header("📸 Mark Your Attendance")

    st.write(
        "Position your face clearly in front of the camera."
    )

    photo = st.camera_input(
        "Take a photo"
    )

    if photo is None:
        return

    # ----------------------------------
    # Convert Camera Image
    # ----------------------------------

    image_bytes = photo.getvalue()

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    # ----------------------------------
    # Face Detection
    # ----------------------------------

    face_found, faces = detect_face(image)

    if not face_found:

        st.error(
            "❌ No face detected. "
            "Please position your face clearly."
        )

        return

    st.success(
        "✅ Face detected successfully!"
    )

    # ----------------------------------
    # Generate SFace Embedding
    # ----------------------------------

    current_embedding = get_face_embedding(
        image
    )

    if current_embedding is None:

        st.error(
            "❌ Could not generate face features."
        )

        return

    # ----------------------------------
    # Load Registered Students
    # ----------------------------------

    students = get_all_students()

    best_student = None
    best_score = -1.0

    # ----------------------------------
    # Compare Faces
    # ----------------------------------

    for student in students:

        stored_face_data = student[4]

        if stored_face_data is None:
            continue

        stored_embedding = bytes_to_embedding(
            stored_face_data
        )

        if stored_embedding is None:
            continue

        score = compare_faces(
            current_embedding,
            stored_embedding
        )

        if score > best_score:

            best_score = score
            best_student = student

    # ----------------------------------
    # Recognition Threshold
    # ----------------------------------

    RECOGNITION_THRESHOLD = 0.363

    # ==================================
    # KNOWN STUDENT
    # ==================================

    if (
        best_student is not None
        and best_score >= RECOGNITION_THRESHOLD
    ):

        student_id = best_student[0]
        name = best_student[1]
        enrollment = best_student[2]

        st.success(
            f"👋 Welcome, {name}!"
        )

        st.info(
            f"Enrollment: {enrollment}"
        )

        st.write(
            f"Face similarity: "
            f"{best_score:.4f}"
        )

        # ----------------------------------
        # Attendance Check
        # ----------------------------------

        if attendance_already_marked(
            student_id
        ):

            st.warning(
                "⚠️ Attendance already marked for today."
            )

        else:

            success = mark_attendance(
                student_id
            )

            if success:

                st.success(
                    "🎉 Attendance marked successfully!"
                )

    # ==================================
    # UNKNOWN FACE
    # ==================================

    else:

        st.warning(
            "🆕 Face not recognized."
        )

        if best_student is not None:

            st.write(
                f"Best similarity: "
                f"{best_score:.4f}"
            )

        st.info(
            "Please register as a new student."
        )

        # ----------------------------------
        # Registration
        # ----------------------------------

        st.subheader(
            "📝 New Student Registration"
        )

        with st.form(
            "registration_form"
        ):

            name = st.text_input(
                "Full Name"
            )

            enrollment = st.text_input(
                "Enrollment Number"
            )

            email = st.text_input(
                "Email"
            )

            register = st.form_submit_button(
                "Register Student & Mark Attendance"
            )

            if register:

                if (
                    not name.strip()
                    or not enrollment.strip()
                    or not email.strip()
                ):

                    st.error(
                        "❌ Please fill all fields."
                    )

                else:

                    face_data = embedding_to_bytes(
                        current_embedding
                    )

                    existing_student = (
                        get_student_by_enrollment(
                            enrollment.strip()
                        )
                    )

                    # ----------------------------------
                    # Existing Student
                    # ----------------------------------

                    if existing_student is not None:

                        old_embedding = (
                            bytes_to_embedding(
                                existing_student[4]
                            )
                        )

                        if old_embedding is None:

                            update_face_data(
                                existing_student[0],
                                face_data
                            )

                            student_id = (
                                existing_student[0]
                            )

                            st.success(
                                "✅ Face registered to your existing student record."
                            )

                        else:

                            st.error(
                                "❌ This enrollment number is already registered."
                            )

                            st.stop()

                    # ----------------------------------
                    # New Student
                    # ----------------------------------

                    else:

                        success, student_id = (
                            add_student(
                                name.strip(),
                                enrollment.strip(),
                                email.strip(),
                                face_data
                            )
                        )

                        if not success:

                            st.error(
                                "❌ Could not register student."
                            )

                            st.stop()

                        st.success(
                            "✅ New student registered successfully!"
                        )

                    # ----------------------------------
                    # Mark Attendance
                    # ----------------------------------

                    if attendance_already_marked(
                        student_id
                    ):

                        st.warning(
                            "⚠️ Attendance already marked for today."
                        )

                    else:

                        mark_attendance(
                            student_id
                        )

                        st.success(
                            "🎉 Attendance marked successfully!"
                        )
