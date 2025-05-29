import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Dental Clinic Assistant", page_icon="🦷")

# Title and intro
st.title("🦷 SmileCare Dental Clinic Assistant")
st.markdown("Hi! I'm your virtual assistant for **SmileCare Dental Clinic**. I can help you with clinic information and appointments.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How may I assist you today? You can ask about our services, timings, or say 'book an appointment'."}
    ]
if "booking_mode" not in st.session_state:
    st.session_state.booking_mode = False
if "appointment_data" not in st.session_state:
    st.session_state.appointment_data = {}

# FAQ database
faq_responses = {
    "what are your working hours": "We’re open from 9 AM to 6 PM, Monday through Saturday.",
    "where are you located": "We are located at 123 Bright Smile Avenue, Mumbai.",
    "do you accept walk-ins": "Yes, we accept walk-ins, but appointments are preferred.",
    "what services do you offer": "We provide general dentistry, orthodontics, root canals, teeth whitening, and pediatric care.",
    "how can i book an appointment": "Sure, just say 'book an appointment' to begin the process."
}

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Appointment booking form handler
def show_appointment_form():
    with st.chat_message("assistant"):
        st.markdown("Let's schedule your appointment:")
        name = st.text_input("🧑 Full Name", key="name")
        contact = st.text_input("📞 Contact Number", key="contact")
        date = st.date_input("📅 Appointment Date", key="date")
        time = st.time_input("⏰ Appointment Time", key="time")

        if st.button("✅ Confirm Appointment"):
            if name and contact:
                confirmation = (
                    f"Thank you, **{name}**! Your appointment is scheduled for "
                    f"**{date.strftime('%d %b %Y')} at {time.strftime('%I:%M %p')}**. "
                    f"We will contact you at **{contact}** to confirm."
                )
                st.session_state.messages.append({"role": "assistant", "content": confirmation})
                st.session_state.booking_mode = False
                st.session_state.chat_input = ""  # reset user input
                st.rerun()
            else:
                st.warning("⚠️ Please fill in both your name and contact number.")

# Generate response function
def generate_response(user_input):
    user_input_lower = user_input.lower().strip()

    # FAQ handling
    for question, answer in faq_responses.items():
        if question in user_input_lower:
            return answer

    # Trigger appointment flow
    if "book an appointment" in user_input_lower or "appointment" in user_input_lower:
        st.session_state.booking_mode = True
        return "Sure! Let’s book your appointment."

    # Fallback
    return "❓ Sorry, I don’t know that yet. Please contact our front desk at +91-9876543210 for further help."

# Chat input
user_input = st.chat_input("Ask a question or say 'book an appointment'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = generate_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Show booking form if enabled
if st.session_state.booking_mode:
    show_appointment_form()
