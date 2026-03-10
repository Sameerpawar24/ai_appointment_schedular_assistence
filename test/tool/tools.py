# from langchain.tools import tool
# from datetime import datetime
# from zoneinfo import ZoneInfo
# import pandas as pd
# import os



# @tool
# def get_current_datetime_ist():
#     """
#     Returns current date and time in Indian Standard Time.
#     Format: YYYY-MM-DD HH:MM:SS
#     """
#     return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")



# class AppointmentManager:

#     def __init__(self, file_path="appointments.csv"):
#         self.file_path = file_path

#         if os.path.exists(self.file_path):
#             self.appointments = pd.read_csv(self.file_path)
#         else:
#             self.appointments = pd.DataFrame(columns=[
#                 "Patient Name",
#                 "Doctor Name",
#                 "Appointment Date",
#                 "Appointment Time"
#             ])

#     def save(self):
#         self.appointments.to_csv(self.file_path, index=False)

#     def check_availability(self, doctor_name, date_str, time_str):

#         conflict = self.appointments[
#             (self.appointments["Doctor Name"] == doctor_name) &
#             (self.appointments["Appointment Date"] == date_str) &
#             (self.appointments["Appointment Time"] == time_str)
#         ]

#         if conflict.empty:
#             return "AVAILABLE"
#         else:
#             return "NOT_AVAILABLE"

#     def add_appointment(self, patient_name, doctor_name, date_str, time_str):

#         conflict = self.check_availability(
#             doctor_name,
#             date_str,
#             time_str
#         )

#         if conflict == "NOT_AVAILABLE":
#             return "FAILED"

#         new_row = {
#             "Patient Name": patient_name,
#             "Doctor Name": doctor_name,
#             "Appointment Date": date_str,
#             "Appointment Time": time_str
#         }

#         self.appointments = pd.concat(
#             [self.appointments, pd.DataFrame([new_row])],
#             ignore_index=True
#         )

#         self.save()

#         return "BOOKED"


# # Initialize manager
# manager = AppointmentManager()


# # ==============================
# # Tool: Check Availability
# # ==============================

# @tool
# def check_doctor_availability(doctor_name: str, date: str, time: str) -> str:
#     """
#     Check if a doctor is available at a given date and time.
#     Returns AVAILABLE or NOT_AVAILABLE.
#     """

#     try:

#         appointment_time = datetime.strptime(time, "%H:%M").time()

#         # enforce working hours
#         if appointment_time.hour < 10 or appointment_time.hour >= 19:
#             return "OUT_OF_WORKING_HOURS"

#         return manager.check_availability(
#             doctor_name,
#             date,
#             time
#         )

#     except Exception:
#         return "INVALID_INPUT"


# # ==============================
# # Tool: Book Appointment
# # ==============================

# @tool
# def add_appointment(patient_name: str, doctor_name: str, date: str, time: str) -> str:
#     """
#     Book a medical appointment.
#     Must be called only after checking availability.
#     """

#     print("📅 Booking appointment in system...")

#     try:

#         appointment_time = datetime.strptime(time, "%H:%M").time()

#         if appointment_time.hour < 10 or appointment_time.hour >= 19:
#             return "OUT_OF_WORKING_HOURS"

#         return manager.add_appointment(
#             patient_name,
#             doctor_name,
#             date,
#             time
#         )

#     except Exception:
#         return "FAILED"


# # ==============================
# # Tool: Simple Math (Optional)
# # ==============================

# @tool
# def add(a: int, b: int):
#     """Return sum of two numbers."""
#     return a + b



from langchain.tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from datetime import datetime
import os



@tool
def add(a,b):
    """This tool is return the addition of two number"""
    return a+b


@tool
def book_appointment(name: str, doctor: str, date: str, time: str) -> str:
    """
    Books a medical appointment.

    Args:
        name: Patient name
        doctor: Doctor name
        date: Appointment date
        time: Appointment time
    """

    print("📅 Booking appointment in system...")

    # Later connect to database here
    return (
        f"Your appointment has been successfully booked for {name} "
        f"with Dr. {doctor} on {date} at {time}."
    )


@tool
def get_current_datetime_ist():
    """Returns the current date and time in Indian Standard Time IST formatted as YYYY MM DD HH MM SS.
Use this function when the system needs the present IST timestamp for scheduling logging or time based operations."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")





class AppointmentManager:
    def __init__(self, file_path="appointments.csv"):
        self.file_path = file_path

        # Load existing CSV if present
        if os.path.exists(self.file_path):
            self.appointments = pd.read_csv(self.file_path)
        else:
            self.appointments = pd.DataFrame(columns=[
                "Patient Name",
                "Doctor Name",
                "Appointment Date",
                "Appointment Time"
            ])

    def add_appointment(self, patient_name, doctor_name, date_str, time_str):
        from datetime import datetime

        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            appointment_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return "Invalid date or time format."

        # 🔎 Check if doctor already has appointment at same date & time
        conflict = self.appointments[
            (self.appointments["Doctor Name"] == doctor_name) &
            (self.appointments["Appointment Date"] == str(appointment_date)) &
            (self.appointments["Appointment Time"] == str(appointment_time))
        ]

        if not conflict.empty:
            return f"Sorry, Dr. {doctor_name} is not available at {appointment_time}. Please choose another time."

        new_row = {
            "Patient Name": patient_name,
            "Doctor Name": doctor_name,
            "Appointment Date": str(appointment_date),
            "Appointment Time": str(appointment_time)
        }

        self.appointments = pd.concat(
            [self.appointments, pd.DataFrame([new_row])],
            ignore_index=True
        )

        # Save to CSV
        self.appointments.to_csv(self.file_path, index=False)

        return f"Appointment booked successfully with Dr. {doctor_name} at {appointment_time}."

    def view_appointments(self):
        return self.appointments
    def view_appointments(self):
        """Return all appointments."""
        if self.appointments.empty:
            return "No appointments scheduled."
        return self.appointments

    def get_doctor_schedule(self, doctor_name):
        """Return all appointments for a specific doctor."""
        doctor_data = self.appointments[
            self.appointments["Doctor Name"] == doctor_name
        ]

        if doctor_data.empty:
            return f"No appointments found for Dr. {doctor_name}."
        
        return doctor_data


manager = AppointmentManager()

@tool
def add_appointment(patient_name: str, doctor_name: str, date: str, time: str):
    """Add a medical appointment."""
    return manager.add_appointment(patient_name, doctor_name, date, time)

@tool
def view_appointments():
    """View all scheduled appointments.For do not dup"""
    return manager.view_appointments().to_string()

@tool 
def view_doctor_schedule(doctor_name:str):
    """Return all appointments for a specific doctor."""
    return manager.get_doctor_schedule(doctor_name)