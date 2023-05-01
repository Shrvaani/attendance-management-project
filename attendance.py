import tkinter as tk
import sqlite3

# create database connection
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# create table
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT NOT NULL, 
              password TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              date TEXT NOT NULL,
              status TEXT NOT NULL)''')
conn.commit()
# create main window
root = tk.Tk()
root.title("Office Attendance Management System")

# create login page
login_frame = tk.Frame(root)
login_frame.pack()

login_username_label = tk.Label(login_frame, text="Username")
login_username_label.pack()
login_username_entry = tk.Entry(login_frame, state="normal")
login_username_entry.pack()
login_username_entry.focus()

login_password_label = tk.Label(login_frame, text="Password")
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*", state="normal")
login_password_entry.pack()

def login():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    if not username or not password:
        login_error_label = tk.Label(login_frame, text="Please enter your username and password")
        login_error_label.pack()
        return
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    if result:
        attendance_page(result[1])
    else:
        login_error_label = tk.Label(login_frame, text="Invalid username or password")
        login_error_label.pack()

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

# create registration page
registration_frame = tk.Frame(root)
registration_frame.pack()

registration_username_label = tk.Label(registration_frame, text="Username")
registration_username_label.pack()
registration_username_entry = tk.Entry(registration_frame, state="normal")
registration_username_entry.pack()
registration_username_entry.focus()

registration_password_label = tk.Label(registration_frame, text="Password")
registration_password_label.pack()
registration_password_entry = tk.Entry(registration_frame, show="*", state="normal")
registration_password_entry.pack()


def register():
    username = registration_username_entry.get().strip()
    password = registration_password_entry.get().strip()
    if not username or not password:
        registration_error_label = tk.Label(registration_frame, text="Please enter a valid username and password")
        registration_error_label.pack()
        return
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    registration_success_label = tk.Label(registration_frame, text="Registration successful")
    registration_success_label.pack()

registration_button = tk.Button(registration_frame, text="Register", command=register)
registration_button.pack()
# create attendance page
attendance_frame = tk.Frame(root)

attendance_username_label = tk.Label(attendance_frame)
attendance_username_label.pack()

attendance_date_label = tk.Label(attendance_frame)
attendance_date_label.pack()

attendance_status_label = tk.Label(attendance_frame)
attendance_status_label.pack()

def mark_attendance(status):
    username = attendance_username_label['text']
    date = attendance_date_label['text']
    c.execute("INSERT INTO attendance (username, date, status) VALUES (?, ?, ?)", (username, date, status))
    conn.commit()
    attendance_status_label['text'] = "Attendance marked: " + status

def attendance_page(username):
    login_frame.pack_forget()
    registration_frame.pack_forget()

    # set up attendance page
    attendance_frame.pack()

    attendance_username_label['text'] = "Username: " + username

    from datetime import date
    today = date.today()
    date_str = today.strftime("%B %d, %Y")
    attendance_date_label['text'] = "Date: " + date_str

    present_button = tk.Button(attendance_frame, text="Present", command=lambda: mark_attendance("Present"))
    present_button.pack()

    absent_button = tk.Button(attendance_frame, text="Absent", command=lambda: mark_attendance("Absent"))
    absent_button.pack()

# create admin page
admin_frame = tk.Frame(root)

def view_attendance():
    c.execute("SELECT * FROM attendance")
    results = c.fetchall()

    # clear previous content in admin frame
    for widget in admin_frame.winfo_children():
        widget.destroy()

    # display attendance data in admin frame
    for result in results:
        attendance_info = tk.Label(admin_frame, text=f"Username: {result[1]}, Date: {result[2]}, Status: {result[3]}")
        attendance_info.pack()

def admin_page():
    login_frame.pack_forget()
    registration_frame.pack_forget()

    # set up admin page
    admin_frame.pack()

    view_attendance_button = tk.Button(admin_frame, text="View Attendance", command=view_attendance)
    view_attendance_button.pack()

# create main menu
def main_menu():
    attendance_frame.pack_forget()
    admin_frame.pack_forget()

    # set up main menu
    login_frame.pack()
    registration_button.pack()

root.after(0, main_menu)
root.mainloop()

# close database connection
conn.close()
