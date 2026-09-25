\# 📸 AI Face Recognition Attendance System



An AI-powered face recognition attendance system built with Python, Streamlit, OpenCV YuNet, SFace, SQLite, and Pandas.



The system automatically recognizes registered students through a camera, records their attendance for the current day, prevents duplicate attendance, and provides attendance dashboards, student analytics, date-based filtering, and CSV export.



\---



\## 🚀 Features



\### 👤 Face Recognition

\- Real-time face detection using OpenCV YuNet

\- Face recognition using OpenCV SFace

\- Automatic identification of registered students

\- Unknown face detection

\- New student registration through the application

\- Face embeddings stored locally



\### 📅 Attendance Management

\- Automatic attendance marking

\- Date-wise attendance tracking

\- Prevents duplicate attendance on the same day

\- Present/Absent calculation

\- Attendance percentage calculation

\- Date-based attendance filtering

\- CSV export



\### 📊 Dashboard

\- Total students

\- Present students

\- Absent students

\- Attendance percentage

\- Present vs Absent visualization

\- Date-wise attendance overview



\### 👥 Student Management

\- View registered students

\- Search by name, enrollment number, or email

\- Face registration status

\- Individual student attendance analytics

\- Attendance history

\- Date-range analysis



\### 📥 Data Export

\- Download complete attendance records

\- Download date-specific attendance records as CSV



\### 🗄️ Local Database

\- SQLite database

\- Student information stored locally

\- Face embeddings stored locally

\- Attendance records stored locally

\- No cloud database required



\---



\## 🛠️ Tech Stack



| Technology | Purpose |

|---|---|

| Python | Core programming language |

| Streamlit | Web application interface |

| OpenCV | Computer vision |

| YuNet | Face detection |

| SFace | Face recognition |

| SQLite | Local database |

| Pandas | Data processing and analytics |

| NumPy | Numerical operations |



\---



\## 🧠 How It Works



```text

&#x20;               ┌──────────────────────┐

&#x20;               │       Start App      │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │   Capture Camera     │

&#x20;               │       Frame           │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │   YuNet Detection    │

&#x20;               │     Detect Face      │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │   SFace Recognition  │

&#x20;               │ Compare Face Feature │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                 ┌────────┴────────┐

&#x20;                 │                 │

&#x20;                 ▼                 ▼

&#x20;            Known Face        Unknown Face

&#x20;                 │                 │

&#x20;                 ▼                 ▼

&#x20;         Check Attendance     Registration

&#x20;                 │                 │

&#x20;                 ▼                 ▼

&#x20;         Mark Attendance      Save Student

&#x20;                 │                 │

&#x20;                 └────────┬────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │   SQLite Database    │

&#x20;               └──────────────────────┘
📂 Project Structure



AI-Face-Attendance-System/

│

├── app.py

├── database.py

├── face\_utils.py

│

├── face\_detection\_yunet\_2023mar.onnx

├── face\_recognition\_sface\_2021dec.onnx

│

├── views/

│   ├── \_\_init\_\_.py

│   ├── attendance.py

│   ├── dashboard.py

│   ├── records.py

│   ├── students.py

│   └── styles.py

│

├── README.md

└── .gitignore



⚙️ Installation



1\. Clone the repository



git clone https://github.com/YOUR-USERNAME/AI-Face-Attendance-System.git



2\. Navigate to the project



cd AI-Face-Attendance-System



3\. Install dependencies



pip install streamlit opencv-python opencv-contrib-python pandas numpy



4\. Run the application



python -m streamlit run app.py



The application will open in your browser.



📋 Requirements



\-Python 3.10+

\-Webcam

\-Windows/Linux/macOS

\-Internet connection for initial package/model setup



🗃️ Database



The application uses SQLite for local data storage.



The database contains:



\-Student information

\-Enrollment number

\-Email

\-Face embeddings

\-Attendance date

\-Attendance time

\-Attendance status



The local database file is intentionally excluded from GitHub using .gitignore.



🔐 Privacy



Face recognition data is stored locally as numerical face embeddings rather than storing the original face image.

The application is designed as a local academic/project implementation and does not use a cloud database.



📊 Attendance Analytics



The student analytics section provides:



\-Working days

\-Present days

\-Absent days

\-Attendance percentage

\-Attendance history

\-Date-range analysis

\-Attendance visualization



Attendance percentage currently uses Monday–Friday as working days. Holidays are not separately configured.



📥 CSV Export



Attendance records can be exported as CSV files from:



\-Dashboard — selected date

\-Attendance Records — all dates or selected date



🎯 Project Objective



The objective of this project is to automate student attendance using face recognition while providing an easy-to-use dashboard for attendance monitoring, student management, analytics, and data export.



🔮 Future Improvements



Possible future enhancements include:



\-Admin authentication

\-Holiday/calendar management

\-Multiple camera support

\-Advanced attendance reports

\-Monthly attendance reports

\-Email notifications

\-Cloud database integration

\-Deployment support

\-Improved biometric security



👨‍💻 Author



Name:- Priyansh Saxena

Gmail:- Priyanshsaxena224@gmail.com



📄 License



This project is developed for educational and academic purposes.

