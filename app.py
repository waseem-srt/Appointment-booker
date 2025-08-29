import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime

# --- CSS for vibrant style, hover effects, animated heading ---
st.markdown("""
<style>
/* Animated Gradient Heading */
.animated-gradient {
  font-size: 2.6rem;
  font-weight: 900;
  background: linear-gradient(-45deg, #ff7e5f, #feb47b, #6dd5ed, #2193b0, #b721ff, #21d4fd);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientMove 4s ease-in-out infinite;
  text-align: center;
  margin-bottom: 1.2rem;
  letter-spacing: 0.04em;
}

@keyframes gradientMove {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

/* Vibrant Card Styles */
.card {
  background: linear-gradient(135deg, #f9d423 0%, #ff4e50 100%);
  border-radius: 18px;
  box-shadow: 0 6px 24px 0 rgba(255,87,34,0.12);
  padding: 1.1rem 1.5rem 1.1rem 1.3rem;
  margin: 1.2rem 0;
  color: #222;
  transition: transform 0.15s, box-shadow 0.15s;
  position: relative;
  border-left: 6px solid #21d4fd;
}

.card:hover {
  transform: scale(1.025) translateY(-2px);
  box-shadow: 0 10px 32px 0 rgba(255,87,34,0.20);
  border-left: 8px solid #b721ff;
}

/* Vibrant Button Hover */
.stButton > button {
  background: linear-gradient(90deg, #21d4fd 0%, #b721ff 100%);
  color: white;
  font-weight: 700;
  border-radius: 8px;
  border: none;
  transition: background 0.24s, transform 0.14s;
  box-shadow: 0 2px 8px 0 rgba(33, 212, 253, 0.10);
}

.stButton > button:hover {
  background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
  color: #222;
  transform: scale(1.065) translateY(-3px);
}

/* Sidebar Icon Nav */
.sidebar-icons {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  margin-top: 1.5rem;
  margin-bottom: 2.5rem;
  align-items: flex-start;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.7em;
  font-size: 1.16rem;
  font-weight: 500;
  color: #21d4fd;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 9px;
  padding: 0.45em 0.82em;
  transition: background 0.16s, color 0.12s;
}

.sidebar-link.selected, .sidebar-link:hover {
  background: #b721ff22;
  color: #b721ff !important;
  text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# --- File Setup ---
CSV_FILE = "appointments.csv"
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=[
        "Appointment ID", "Name", "Age", "Gender", "Phone", "Camp Date", "Time Slot", "Symptoms",
        "Native Place", "Dialect", "Festival", "Proverb/Story", "Created At"])
    df_init.to_csv(CSV_FILE, index=False)

# --- Sidebar Navigation ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4320/4320337.png", width=70)
st.sidebar.markdown('<h2 style="color:#21d4fd;margin-bottom:-10px;">🩺 Nav</h2>', unsafe_allow_html=True)

# Sidebar nav state
if "page" not in st.session_state:
    st.session_state.page = "Book"

def sidebar_link(label, icon, key):
    selected = (st.session_state.page == key)
    st.sidebar.markdown(
        f'<button class="sidebar-link {"selected" if selected else ""}" onclick="window.location.search=\'?page={key}\'">{icon} {label}</button>',
        unsafe_allow_html=True
    )

# Streamlit doesn't allow JS on click, so do with a selectbox for page state
page = st.sidebar.selectbox(
    "Go to", ["Book Appointment", "View/Search"], 
    index=0 if st.session_state.page == "Book" else 1,
    format_func=lambda x: "📝 " + x if x == "Book Appointment" else "🔍 " + x
)
st.session_state.page = "Book" if page == "Book Appointment" else "Search"

# --- Animated Gradient Heading ---
st.markdown('<div class="animated-gradient">🌈 Telugu Heritage Camp Appointments</div>', unsafe_allow_html=True)

# --- BOOKING FORM ---
if st.session_state.page == "Book":
    st.subheader("📝 Book a Camp Appointment")

    with st.form("appointment_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name*", max_chars=40)
        age = c2.number_input("Age*", min_value=0, max_value=120, step=1)
        gender = c1.selectbox("Gender*", ["Male", "Female", "Other"])
        phone = c2.text_input("Phone Number*", max_chars=15, help="For SMS confirmation")
        camp_date = c1.date_input("Camp Date*", min_value=datetime.now().date())
        time_slot = c2.selectbox("Time Slot*", [
            "09:00 - 10:00 AM", "10:00 - 11:00 AM", "11:00 - 12:00 PM",
            "01:00 - 02:00 PM", "02:00 - 03:00 PM"
        ])
        symptoms = st.text_area("Symptoms*", max_chars=100)

        with st.expander("✨ Telugu Heritage (Optional)"):
            native_place = st.text_input("Native Place (e.g., Tirupati, Vijayawada)")
            dialect = st.text_input("Dialect (e.g., Rayalaseema, Telangana, Coastal)")
            festival = st.text_input("Favorite Telugu Festival (e.g., Ugadi, Sankranti)")
            proverb = st.text_area("Favorite Proverb/Story (in Telugu or English)")

        submitted = st.form_submit_button("Book Appointment 🚀")
        
    if submitted:
        if not name or not phone or not symptoms or not age:
            st.error("Please fill all required fields marked with *.")
        else:
            appt_id = str(uuid.uuid4())[:8].upper()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            data = {
                "Appointment ID": appt_id, "Name": name, "Age": age, "Gender": gender,
                "Phone": phone, "Camp Date": camp_date.strftime("%Y-%m-%d"),
                "Time Slot": time_slot, "Symptoms": symptoms,
                "Native Place": native_place, "Dialect": dialect,
                "Festival": festival, "Proverb/Story": proverb,
                "Created At": created_at
            }
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success(f"🎉 Appointment booked successfully! Your Appointment ID: {appt_id}")
            st.balloons()

# --- SEARCH / VIEW ---
if st.session_state.page == "Search":
    st.subheader("🔍 Search/View Appointments")
    df = pd.read_csv(CSV_FILE)

    search_mode = st.radio("Search by:", ["Appointment ID", "Phone Number"], horizontal=True)
    search_query = st.text_input(
        "Enter Appointment ID" if search_mode == "Appointment ID" else "Enter Phone Number"
    )

    if st.button("Search 🔎"):
        if search_query.strip() == "":
            st.warning("Please enter a value to search.")
        else:
            if search_mode == "Appointment ID":
                match = df[df["Appointment ID"].str.upper() == search_query.strip().upper()]
            else:
                match = df[df["Phone"].astype(str).str.strip() == search_query.strip()]
            
            if match.empty:
                st.error("❌ No appointment found with the provided details.")
            else:
                for _, row in match.iterrows():
                    st.markdown(f"""
                    <div class="card">
                        <h4>🆔 {row['Appointment ID']} - <span style="color:#b721ff;">{row['Name']}</span></h4>
                        <b>👤 Age:</b> {row['Age']} &nbsp; | &nbsp; <b>🚻 Gender:</b> {row['Gender']}<br>
                        <b>📱 Phone:</b> {row['Phone']}<br>
                        <b>📅 Camp Date:</b> {row['Camp Date']} &nbsp; | &nbsp; <b>⏰ Time:</b> {row['Time Slot']}<br>
                        <b>🤒 Symptoms:</b> {row['Symptoms']}<br>
                        {"<b>🌏 Native Place:</b> " + str(row['Native Place']) + "<br>" if row['Native Place'] else ""}
                        {"<b>🗣 Dialect:</b> " + str(row['Dialect']) + "<br>" if row['Dialect'] else ""}
                        {"<b>🎉 Festival:</b> " + str(row['Festival']) + "<br>" if row['Festival'] else ""}
                        {"<b>📖 Proverb/Story:</b> " + str(row['Proverb/Story']) + "<br>" if row['Proverb/Story'] else ""}
                        <span style="font-size:0.95em;color:#555;">🕑 Booked at: {row['Created At']}</span>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("----")
    with st.expander("📋 Show All Appointments"):
        if df.empty:
            st.info("No appointments booked yet.")
        else:
            for _, row in df.sort_values(by="Created At", ascending=False).iterrows():
                st.markdown(f"""
                <div class="card">
                    <h4>🆔 {row['Appointment ID']} - <span style="color:#b721ff;">{row['Name']}</span></h4>
                    <b>👤 Age:</b> {row['Age']} &nbsp; | &nbsp; <b>🚻 Gender:</b> {row['Gender']}<br>
                    <b>📱 Phone:</b> {row['Phone']}<br>
                    <b>📅 Camp Date:</b> {row['Camp Date']} &nbsp; | &nbsp; <b>⏰ Time:</b> {row['Time Slot']}<br>
                    <b>🤒 Symptoms:</b> {row['Symptoms']}<br>
                    {"<b>🌏 Native Place:</b> " + str(row['Native Place']) + "<br>" if row['Native Place'] else ""}
                    {"<b>🗣 Dialect:</b> " + str(row['Dialect']) + "<br>" if row['Dialect'] else ""}
                    {"<b>🎉 Festival:</b> " + str(row['Festival']) + "<br>" if row['Festival'] else ""}
                    {"<b>📖 Proverb/Story:</b> " + str(row['Proverb/Story']) + "<br>" if row['Proverb/Story'] else ""}
                    <span style="font-size:0.95em;color:#555;">🕑 Booked at: {row['Created At']}</span>
                </div>
                """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<hr style="border-top: 1.5px dashed #b721ff;margin-top:2.5em;">
<div style="text-align:center;font-size:1.06em; color:#888;">Made with ❤️ for Telugu Community • Vibrant Streamlit App</div>
""", unsafe_allow_html=True)