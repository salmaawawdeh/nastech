# NAS Tech - University Events and Workshops Portal

**NAS Tech** is a Streamlit-powered web application designed to streamline the organization, management, and attendance tracking of university events, workshops, and extracurricular activities. The platform integrates seamlessly with **Supabase** as a backend database service and provides tailored interactive dashboards for students, event organizers, university administrators, and visiting companies.

---

## 🔑 Key Features

### 👨‍🎓 Student Portal
- **Browse & Register:** Discover university events and workshops filtered by category or searched by title.
- **My Registrations:** Track personal registrations and attendance statuses (*Present* / *Absent*).
- **Smart Recommendations:** Get tailored event recommendations based on academic majors and personal interests.
- **Profile Management:** Easily update academic specialization/major details.

### 📋 Event Organizer Dashboard
- **Event Creation:** Submit new events and workshops with dates, descriptions, categories, and designated venue assignments.
- **Request Tracker:** Monitor real-time status updates (*Pending*, *Approved*, or *Rejected*) for submitted event proposals.
- **Attendee Management:** View registered students and record event attendance.
- **Event Insights:** Access key statistics and metrics regarding attendee turnouts and venue capacity.

### 🏛️ University Administration Portal
- **Review System:** Inspect incoming event proposals submitted by organizers.
- **Approval Workflow:** Approve valid proposals or reject them with mandatory rejection reasons for organizational feedback.

### 🏢 Corporate & Guest Portal
- **Partner Portal:** A session-based guest entry for external companies and partner organizations to propose hosting workshops or collaborative campus events.

---

## 🛠️ Tech Stack & Dependencies

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Backend / Database:** [Supabase](https://supabase.com/) (`supabase-py`)
- **Data Handling:** [Pandas](https://pandas.pydata.org/)
- **Language:** Python 3.9+

---

## 📁 Repository Structure

```text
NAS Tech/
├── app.py                 # Main Streamlit application entry point
├── .streamlit/
│   └── secrets.toml       # Supabase credentials configuration file (Local)
└── README.md              # Project documentation
```

---

## ⚙️ Setup and Installation

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your environment.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/NAS-Tech.git
cd NAS-Tech
```

### 3. Install Required Packages
Install the required dependencies using pip:
```bash
pip install streamlit pandas supabase
```

### 4. Database Setup (Supabase)
Set up the following tables in your Supabase database instance:
- `users`: `user_id`, `name`, `email`, `role` (`student`, `organizer`, `admin`), `major`
- `events`: `event_id`, `title`, `description`, `category`, `event_date`, `venue_id`, `organizer_id`, `status`, `rejection_reason`
- `venues`: `venue_id`, `venue_name`, `university_name`, `max_capacity`
- `registrations`: `registration_id`, `student_id`, `event_id`, `attendance_status`

### 5. Configure Secrets
Create a `.streamlit/secrets.toml` file in the root directory and add your Supabase credentials:

```toml
SUPABASE_URL = "https://your-supabase-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

---

## 🚀 Running the Application

Launch the Streamlit web application using the following command:

```bash
streamlit run app.py
```

Once running, navigate to `http://localhost:8501` in your web browser.
