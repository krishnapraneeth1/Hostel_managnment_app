import mysql.connector
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta
from tkinter import PhotoImage



# Establish MySQL connection (update credentials if needed)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123"
)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS housing_management")
cursor.execute("USE housing_management")

# Create Roles table
# After table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
)
""")

cursor.execute("""
INSERT INTO roles (role_id, role_name) VALUES
(1, 'Admin'),
(2, 'User') AS new
ON DUPLICATE KEY UPDATE role_name = new.role_name
""")

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(255),
    mobile VARCHAR(15),
    student_id VARCHAR(20) UNIQUE,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
)
""")

# Create Rooms table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(20) UNIQUE,
    capacity INT,
    availability VARCHAR(50)
)
""")

# Create Room Allocation table
cursor.execute("""
CREATE TABLE IF NOT EXISTS room_allocation (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    room_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
)
""")

# Create Payments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    room_id INT,
    amount FLOAT,
    payment_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
)
""")

# Create Maintenance Requests table
cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance_requests (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    date_submitted DATE,
    date_resolved DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Create Leave Requests table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests (
    leave_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

conn.commit()
print("Database and tables have been created successfully.")

cursor.close()
conn.close()


# # # Initialize the application window
# ctk.set_appearance_mode("white")  # Set theme
# ctk.set_default_color_theme("blue")



class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Housing Management System - Login")
        self.geometry("1200x750")
        self.resizable(False, False)
        #self.show_login_screen()
        #self.show_user_dashboard()
        self.show_admin_dashboard()
        self.configure(fg_color="white", bg_color="white")

    def show_login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()


        bg_image = Image.open("UI/login_sceen.png")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.login_frame = ctk.CTkFrame(self, width=345, height=400, corner_radius=20, fg_color="#544D4D")
        self.login_frame.place(relx=0.75, rely=0.5, anchor="center")

        self.logo = Image.open("UI/home-button.png")
        self.logo = self.logo.resize((30, 30), Image.LANCZOS)
        self.logo_ctk = ctk.CTkImage(light_image=self.logo, size=(30, 30))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_ctk, text="")
        self.logo_label.place(relx=0.68, rely=0.20, anchor="center")

        self.label = ctk.CTkLabel(self, text="Management", font=("Arial", 25, "bold"), text_color="black", bg_color="white")
        self.label.place(relx=0.76, rely=0.20, anchor="center")

        self.title_label = ctk.CTkLabel(self.login_frame, text="Login / Register", font=("Arial", 25, "bold"), text_color="white")
        self.title_label.place(relx=0.5, rely=0.15, anchor="center")

        self.username_label = ctk.CTkLabel(self.login_frame, text="Username", font=("Arial", 18), text_color="white")
        self.username_label.place(relx=0.15, rely=0.25)
        self.username_entry = ctk.CTkEntry(self.login_frame, width=250, height=35, fg_color="#1E1E1E", text_color="white")
        self.username_entry.place(relx=0.15, rely=0.35)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Password", font=("Arial", 18), text_color="white")
        self.password_label.place(relx=0.15, rely=0.45)
        self.password_entry = ctk.CTkEntry(self.login_frame, width=250, height=35, fg_color="#1E1E1E", text_color="white", show="*")
        self.password_entry.place(relx=0.15, rely=0.55)

        self.forgot_password = ctk.CTkLabel(self.login_frame, text="Forgot Password", font=("Arial", 12, "underline"), text_color="white", cursor="hand2")
        self.forgot_password.place(relx=0.15, rely=0.65)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=100, height=40, font=("Arial", 18, "bold"), command=self.login_authenticate)
        self.login_button.place(relx=0.15, rely=0.8)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", width=100, height=40, font=("Arial", 18, "bold"), command=self.show_register_screen)
        self.register_button.place(relx=0.55, rely=0.8)

    def show_register_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        bg_image = Image.open("UI/registeration_screen.jpg")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self, text="Sign up to Login", font=("Arial", 28, "bold"), text_color="black")
        self.title_label.place(relx=0.5, rely=0.38, anchor="center")

        self.register_frame = ctk.CTkFrame(self, width=1050, height=400, corner_radius=20, fg_color="#45403F")
        self.register_frame.place(relx=0.5, rely=0.70, anchor="center")

        self.first_name_label = ctk.CTkLabel(self.register_frame, text="First Name", font=("Arial", 18, "bold"), text_color="white")
        self.first_name_label.place(x=50, y=50)
        self.first_name_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E")
        self.first_name_entry.place(x=170, y=50)

        self.last_name_label = ctk.CTkLabel(self.register_frame, text="Last Name", font=("Arial", 18, "bold"), text_color="white")
        self.last_name_label.place(x=50, y=110)
        self.last_name_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E")
        self.last_name_entry.place(x=170, y=110)

        self.email_label = ctk.CTkLabel(self.register_frame, text="Email", font=("Arial", 18, "bold"), text_color="white")
        self.email_label.place(x=50, y=170)
        self.email_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E")
        self.email_entry.place(x=170, y=170)

        self.student_id_label = ctk.CTkLabel(self.register_frame, text="Student ID", font=("Arial", 18, "bold"), text_color="white")
        self.student_id_label.place(x=50, y=230)
        self.student_id_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E")
        self.student_id_entry.place(x=170, y=230)

        self.mobile_label = ctk.CTkLabel(self.register_frame, text="Mobile Number", font=("Arial", 18, "bold"), text_color="white")
        self.mobile_label.place(x=520, y=50)
        self.mobile_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E")
        self.mobile_entry.place(x=700, y=50)

        self.password_label = ctk.CTkLabel(self.register_frame, text="Password", font=("Arial", 18, "bold"), text_color="white")
        self.password_label.place(x=520, y=110)
        self.password_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E", show="*")
        self.password_entry.place(x=700, y=110)

        self.confirm_password_label = ctk.CTkLabel(self.register_frame, text="Confirm Password", font=("Arial", 18, "bold"), text_color="white")
        self.confirm_password_label.place(x=520, y=170)
        self.confirm_password_entry = ctk.CTkEntry(self.register_frame, width=300, height=35, fg_color="#1E1E1E", show="*")
        self.confirm_password_entry.place(x=700, y=170)

        #show password checkbox for password and confirm password entry
        self.show_password_var = ctk.IntVar()
        self.show_password_checkbox = ctk.CTkCheckBox(self.register_frame, text="Show Password", variable=self.show_password_var, text_color="white", bg_color="#45403F", command=self.show_password)
        self.show_password_checkbox.place(x=700, y=210)
        

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", width=150, height=40, command=self.register_user, font=("Arial", 18, "bold"))
        self.register_button.place(relx=0.5, rely=0.85, anchor="center")

    def login_authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Please enter both Username and Password.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root@123",
                database="housing_management"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                role_id = result[7]  # Assuming role_id is in column 8 (index 7)
                user_id = result[0]  # Assuming user_id is in column 1 (index 0)
                messagebox.showinfo("Login Success", "Login successful!")
                # Redirect to respective dashboard
                if role_id == 1:  # Admin role
                    self.show_admin_dashboard()
                else:  # User role
                    self.show_user_dashboard(user_id=user_id)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials. Try again.")

            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    #show password function
    def show_password(self):

        if self.show_password_var.get() == 1:
            self.password_entry.configure(show="")
            self.confirm_password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.confirm_password_entry.configure(show="*")

    def register_user(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        student_id = self.student_id_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        # Validation
        if not all([first_name, last_name, email, student_id, mobile, password, confirm_password]):
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root@123",  # Update if needed
                database="housing_management"
            )
            cursor = conn.cursor()

            # Check for duplicate email or student_id
            cursor.execute("SELECT * FROM users WHERE email = %s OR student_id = %s", (email, student_id))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Email or Student ID already exists.")
                return

            # Determine role_id based on email
            role_id = 1 if "admin" in email.lower() else 2

            # Insert into users with determined role_id
            insert_query = """
                INSERT INTO users (first_name, last_name, email, password, mobile, student_id, role_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, password, mobile, student_id, role_id)
            cursor.execute(insert_query, values)
            conn.commit()

            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.show_login_screen()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    # def show_user_dashboard(self):
        user_id = self.current_user_id
    #     for widget in self.winfo_children():
    #         widget.destroy()

    #     self.geometry("1200x750")
    #     self.configure(fg_color="#3B3737", bg_color="#3B3737")

    #     #add image to the dashboard
    #     bg_image = Image.open("UI/user_dashboard_screen.jpg")
    #     bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
    #     self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
    #     self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
    #     self.bg_label.place(relx=0.5, rely=0.5, anchor="center")


    #     # Sidebar (Navigation Panel)
    #     self.sidebar = ctk.CTkFrame(self, width=370, height=750, corner_radius=0, fg_color="#3B3737")
    #     self.sidebar.place(x=0, y=0)

    #     # Hello Label
    #     self.hello_label = ctk.CTkLabel(self.sidebar, text="Hello User", font=("Arial", 18, "bold"), text_color="white")
    #     self.hello_label.place(x=20, y=40)

    #     # Navigation Buttons (Icons to be added later)
    #     self.room_details_button = ctk.CTkButton(self.sidebar, text="View my Room Details", font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w")
    #     self.room_details_button.place(x=70, y=200)

    #     #add image beside the button
    #     self.room_details = Image.open("UI/home-button.png")
    #     self.room_details = self.room_details.resize((30, 30), Image.LANCZOS)
    #     self.room_details_ctk = ctk.CTkImage(light_image=self.room_details, size=(30, 30))
    #     self.room_details_label = ctk.CTkLabel(self, image=self.room_details_ctk, text="",fg_color="#3B3737")
    #     self.room_details_label.place(x=40, y=220, anchor="center")

    #     self.rent_payment_button = ctk.CTkButton(self.sidebar, text="Rent Payment", font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w")
    #     self.rent_payment_button.place(x=70, y=260)

    #     #add image beside the button
    #     self.rent_payment = Image.open("UI/key.png")
    #     self.rent_payment = self.rent_payment.resize((30, 30), Image.LANCZOS)
    #     self.rent_payment_ctk = ctk.CTkImage(light_image=self.rent_payment, size=(30, 30))
    #     self.rent_payment_label = ctk.CTkLabel(self, image=self.rent_payment_ctk, text="",fg_color="#3B3737")
    #     self.rent_payment_label.place(x=40, y=280, anchor="center")

    #     self.maintenance_button = ctk.CTkButton(self.sidebar, text="Maintenance Request", font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w")
    #     self.maintenance_button.place(x=70, y=320)

    #     #add image beside the button
    #     self.maintenance = Image.open("UI/maintainance.png")
    #     self.maintenance = self.maintenance.resize((30, 30), Image.LANCZOS)
    #     self.maintenance_ctk = ctk.CTkImage(light_image=self.maintenance, size=(30, 30))
    #     self.maintenance_label = ctk.CTkLabel(self, image=self.maintenance_ctk, text="",fg_color="#3B3737")
    #     self.maintenance_label.place(x=40, y=340, anchor="center")


    #     self.exit_request_button = ctk.CTkButton(self.sidebar, text="Exit Request", font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w")
    #     self.exit_request_button.place(x=70, y=380)

    #     #add image beside the button
    #     self.exit_request = Image.open("UI/logout.png")
    #     self.exit_request = self.exit_request.resize((30, 30), Image.LANCZOS)
    #     self.exit_request_ctk = ctk.CTkImage(light_image=self.exit_request, size=(30, 30))
    #     self.exit_request_label = ctk.CTkLabel(self, image=self.exit_request_ctk, text="",fg_color="#3B3737")
    #     self.exit_request_label.place(x=40, y=400, anchor="center")
        
    #     self.logout = Image.open("UI/log-out.png")
    #     self.logout = self.logout.resize((50, 50), Image.LANCZOS)
    #     self.logout_ctk = ctk.CTkImage(light_image=self.logout, size=(50, 50))
    #     self.logout_button = ctk.CTkButton(self, image=self.logout_ctk, text="", fg_color="#3B3737",hover_color="#3B3737", command=self.show_login_screen)
    #     self.logout_button.place(relx=0.05, rely=0.95, anchor="center")



    #     # Main Title
    #     self.dashboard_title = ctk.CTkLabel(self, text="My Room Details", font=("Arial", 24, "bold"), text_color="black")
    #     self.dashboard_title.place(relx=0.65, rely=0.25, anchor="center")

    #     # Room Details Box
    #     self.details_frame = ctk.CTkFrame(self, width=600, height=300, corner_radius=20, fg_color="#1E1E1E")
    #     self.details_frame.place(relx=0.65, rely=0.6, anchor="center")

    #     # Static Labels (Values to be dynamically populated later)
    #     label_style = {"font": ("Arial", 18, "bold"), "text_color": "white"}
    #     ctk.CTkLabel(self.details_frame, text="Student ID", **label_style).place(x=40, y=40)
    #     ctk.CTkLabel(self.details_frame, text="Room Number", **label_style).place(x=40, y=90)
    #     ctk.CTkLabel(self.details_frame, text="Capacity", **label_style).place(x=40, y=140)
    #     ctk.CTkLabel(self.details_frame, text="Availability Status", **label_style).place(x=40, y=190)
    #     ctk.CTkLabel(self.details_frame, text="Maintenance Requests", **label_style).place(x=40, y=240)

    def show_user_dashboard(self):
        user_id = self.current_user_id
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="#3B3737", bg_color="#3B3737")

        # Add background image
        bg_image = Image.open("UI/user_dashboard_screen.jpg")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=370, height=750, corner_radius=0, fg_color="#3B3737")
        self.sidebar.place(x=0, y=0)

        self.hello_label = ctk.CTkLabel(self.sidebar, text="Hello User", font=("Arial", 18, "bold"), text_color="white")
        self.hello_label.place(x=20, y=40)

        # Sidebar Buttons + Icons
        nav_buttons = [
            ("View my Room Details", "UI/home-button.png", 200, self.show_user_dashboard),
            ("Rent Payment", "UI/key.png", 260, self.show_rent_payment_screen),
            ("Maintenance Request", "UI/maintainance.png", 320,self.show_maintenance_screen),
            ("Exit Request", "UI/logout.png", 380,self.show_exit_request_screen)
        ]

        for idx, (label, icon_path, y_pos, command) in enumerate(nav_buttons):
            button = ctk.CTkButton(self.sidebar, text=label, font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w", command=command)
            button.place(x=70, y=y_pos)

            icon = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            icon_ctk = ctk.CTkImage(light_image=icon, size=(30, 30))
            icon_label = ctk.CTkLabel(self, image=icon_ctk, text="", fg_color="#3B3737")
            icon_label.place(x=40, y=y_pos + 20, anchor="center")

        # Logout Button
        self.logout = Image.open("UI/log-out.png").resize((50, 50), Image.LANCZOS)
        self.logout_ctk = ctk.CTkImage(light_image=self.logout, size=(50, 50))
        self.logout_button = ctk.CTkButton(self, image=self.logout_ctk, text="", fg_color="#3B3737", hover_color="#3B3737", command=self.show_login_screen)
        self.logout_button.place(relx=0.05, rely=0.95, anchor="center")

        # Main Section Title
        self.dashboard_title = ctk.CTkLabel(self, text="My Room Details", font=("Arial", 24, "bold"), text_color="black")
        self.dashboard_title.place(relx=0.65, rely=0.25, anchor="center")

        # Room Details Frame
        self.details_frame = ctk.CTkFrame(self, width=600, height=300, corner_radius=20, fg_color="#1E1E1E")
        self.details_frame.place(relx=0.65, rely=0.6, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "white"}
        value_style = {"font": ("Arial", 18), "text_color": "white"}

        # Database Query to Populate Data
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",  # add password if needed
            database="housing_management"
        )
        cursor = conn.cursor()

        student_id = room_number = capacity = availability_status = maintenance_status = "N/A"

        cursor.execute("""
            SELECT u.student_id, r.room_number, r.capacity,
                CASE WHEN r.availability = 'Yes' THEN 'Free' ELSE 'Occupied' END AS availability_status
            FROM users u
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE u.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            student_id, room_number, capacity, availability_status = result

        cursor.execute("""
            SELECT status FROM maintenance_requests
            WHERE user_id = %s
            ORDER BY date_submitted DESC
            LIMIT 1
        """, (user_id,))
        maintenance_result = cursor.fetchone()
        if maintenance_result:
            maintenance_status = maintenance_result[0].capitalize()
        else:
            maintenance_status = "None"

        conn.close()

        # Display Labels and Values
        data = [
            ("Student ID", student_id),
            ("Room Number", room_number),
            ("Capacity", capacity),
            ("Availability Status", availability_status),
            ("Maintenance Requests", maintenance_status)
        ]

        for i, (label, value) in enumerate(data):
            y = 40 + i * 50
            ctk.CTkLabel(self.details_frame, text=label, **label_style).place(x=40, y=y)
            ctk.CTkLabel(self.details_frame, text=str(value), **value_style).place(x=300, y=y)


    def show_rent_payment_screen(self):
        user_id = self.current_user_id
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="#3B3737")

        # Background image
        bg_image = Image.open("UI/user_dashboard_screen.jpg")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Sidebar with nav buttons (reuse existing code if possible)
        self.sidebar = ctk.CTkFrame(self, width=370, height=750, corner_radius=0, fg_color="#3B3737")
        self.sidebar.place(x=0, y=0)

        ctk.CTkLabel(self.sidebar, text="Hello User", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=40)

        nav_buttons = [
            ("View my Room Details", "UI/home-button.png", 200, self.show_user_dashboard),
            ("Rent Payment", "UI/key.png", 260, self.show_rent_payment_screen),
            ("Maintenance Request", "UI/maintainance.png", 320, self.show_maintenance_screen),
            ("Exit Request", "UI/logout.png", 380, self.show_exit_request_screen)
        ]

        for label, icon_path, y_pos, command in nav_buttons:
            ctk.CTkButton(self.sidebar, text=label, font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w", command=command).place(x=70, y=y_pos)
            icon = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            icon_ctk = ctk.CTkImage(light_image=icon, size=(30, 30))
            ctk.CTkLabel(self, image=icon_ctk, text="", fg_color="#3B3737").place(x=40, y=y_pos + 20, anchor="center")

        self.logout = Image.open("UI/log-out.png").resize((50, 50), Image.LANCZOS)
        self.logout_ctk = ctk.CTkImage(light_image=self.logout, size=(50, 50))
        self.logout_button = ctk.CTkButton(self, image=self.logout_ctk, text="", fg_color="#3B3737", hover_color="#3B3737", command=self.show_login_screen)
        self.logout_button.place(relx=0.05, rely=0.95, anchor="center")

        # Title
        ctk.CTkLabel(self, text="Rent Payment", font=("Arial", 24, "bold"), text_color="black").place(relx=0.65, rely=0.25, anchor="center")

        # Payment Details Frame
        payment_frame = ctk.CTkFrame(self, width=600, height=300, corner_radius=20, fg_color="#1E1E1E")
        payment_frame.place(relx=0.65, rely=0.6, anchor="center")


        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="housing_management"
        )
        cursor = conn.cursor()

        student_id = room_id = amount_due = due_date = "N/A"
        room_capacity = 1

        cursor.execute("""
            SELECT u.student_id, r.room_id, r.capacity, ra.allocation_id
            FROM users u
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE u.user_id = %s
        """, (user_id,))
        room_data = cursor.fetchone()

        if room_data:
            student_id, room_id, room_capacity, allocation_id = room_data
            due_date_calc = datetime.today() + timedelta(days=30)
            due_date = due_date_calc.strftime('%Y-%m-%d')

            full_rent = 1000  # Assume full rent = 1000
            amount_due = full_rent / room_capacity
            


        # Create labels for data display
        label_style = {"font": ("Arial", 18, "bold"), "text_color": "white"}
        value_style = {"font": ("Arial", 18), "text_color": "white"}

        ctk.CTkLabel(payment_frame, text="Student ID", **label_style).place(x=40, y=40)
        ctk.CTkLabel(payment_frame, text=str(student_id), **value_style).place(x=300, y=40)

        ctk.CTkLabel(payment_frame, text="Room ID", **label_style).place(x=40, y=90)
        ctk.CTkLabel(payment_frame, text=str(room_id), **value_style).place(x=300, y=90)

        # Amount Due
        ctk.CTkLabel(payment_frame, text="Amount Due", **label_style).place(x=40, y=140)

        if amount_due != "N/A":
            amount_due = float(amount_due)
            ctk.CTkLabel(payment_frame, text=f"${amount_due:.2f}", **value_style).place(x=300, y=140)
        else:
            ctk.CTkLabel(payment_frame, text="N/A", **value_style).place(x=300, y=140)


        ctk.CTkLabel(payment_frame, text="Payment Due Date", **label_style).place(x=40, y=190)
        ctk.CTkLabel(payment_frame, text=str(due_date), **value_style).place(x=300, y=190)

        ctk.CTkLabel(payment_frame, text="Enter Amount to be Paid", **label_style).place(x=40, y=240)
        self.amount_entry = ctk.CTkEntry(payment_frame, width=200, height=35, fg_color="#544D4D", text_color="white")
        self.amount_entry.place(x=300, y=240)

        def process_payment():
            entered_amount = self.amount_entry.get()
            try:
                entered_amount = float(entered_amount)
                if entered_amount != amount_due:
                    raise ValueError("Incorrect payment amount")

                today = datetime.today().strftime('%Y-%m-%d')
                cursor.execute("""
                    INSERT INTO payments (user_id, room_id, amount, payment_date)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, room_id, entered_amount, today))
                conn.commit()
                ctk.CTkLabel(payment_frame, text="Payment Successful!", text_color="green").place(relx=0.5, rely=1.1, anchor="center")
            except:
                ctk.CTkLabel(payment_frame, text="Invalid payment.", text_color="red").place(relx=0.5, rely=1.1, anchor="center")

        # Payment Button as image inside the payment_frame
        self.payment_button = Image.open("UI/pay-per-click.png")
        self.payment_button = self.payment_button.resize((200, 50), Image.LANCZOS)  
        self.payment_button_ctk = ctk.CTkImage(light_image=self.payment_button, size=(200, 50))

        self.payment_button_btn = ctk.CTkButton(
            payment_frame,  
            image=self.payment_button_ctk,
            text="",  
            fg_color="#1E1E1E",  
            hover_color="#2F2F2F",  
            width=200,
            height=50,
            command=process_payment
        )
        self.payment_button_btn.place(relx=0.5, rely=1.2, anchor="center")  
        conn.close()

    def show_maintenance_screen(self):
        user_id = self.current_user_id
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="#3B3737", bg_color="#3B3737")

        # Background image
        bg_image = Image.open("UI/user_dashboard_screen.jpg").resize((1200, 750))
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=370, height=750, corner_radius=0, fg_color="#3B3737")
        self.sidebar.place(x=0, y=0)

        ctk.CTkLabel(self.sidebar, text="Hello User", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=40)

        # Individual sidebar buttons
        sidebar_buttons = [
            ("View my Room Details", "UI/home-button.png", 200, self.show_user_dashboard),
            ("Rent Payment", "UI/key.png", 260, self.show_rent_payment_screen),
            ("Maintenance Request", "UI/maintainance.png", 320, self.show_maintenance_screen),
            ("Exit Request", "UI/logout.png", 380,self.show_exit_request_screen)
        ]

        for label, icon_path, y_pos, command in sidebar_buttons:
            ctk.CTkButton(self.sidebar, text=label, font=("Arial", 16), fg_color="#3B3737",
                        width=200, height=40, anchor="w",
                        command=command).place(x=70, y=y_pos)
            icon = Image.open(icon_path).resize((30, 30))
            icon_ctk = ctk.CTkImage(light_image=icon, size=(30, 30))
            ctk.CTkLabel(self, image=icon_ctk, text="", fg_color="#3B3737").place(x=40, y=y_pos + 20, anchor="center")

        logout_icon = Image.open("UI/log-out.png").resize((50, 50))
        logout_ctk = ctk.CTkImage(light_image=logout_icon, size=(50, 50))
        ctk.CTkButton(self, image=logout_ctk, text="", fg_color="#3B3737", hover_color="#3B3737",
                    command=self.show_login_screen).place(relx=0.05, rely=0.95, anchor="center")

        # Title
        ctk.CTkLabel(self, text="Maintenance Request", font=("Arial", 24, "bold"), text_color="black").place(relx=0.65, rely=0.25, anchor="center")

        # Frame for maintenance
        form_frame = ctk.CTkFrame(self, width=600, height=300, corner_radius=20, fg_color="#1E1E1E")
        form_frame.place(relx=0.65, rely=0.6, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "white"}
        value_style = {"font": ("Arial", 18), "text_color": "white"}

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="housing_management"
        )
        cursor = conn.cursor()

        student_id = room_number = "N/A"

        cursor.execute("""
            SELECT u.student_id, r.room_number
            FROM users u
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE u.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            student_id, room_number = result

        # Static labels and values
        ctk.CTkLabel(form_frame, text="Student ID", **label_style).place(x=40, y=40)
        ctk.CTkLabel(form_frame, text=str(student_id), **value_style).place(x=300, y=40)

        ctk.CTkLabel(form_frame, text="Room Number", **label_style).place(x=40, y=90)
        ctk.CTkLabel(form_frame, text=str(room_number), **value_style).place(x=300, y=90)

        ctk.CTkLabel(form_frame, text="Maintenance Description", **label_style).place(x=40, y=140)
        self.maintenance_description_entry = ctk.CTkTextbox(form_frame, width=400, height=80, fg_color="#544D4D", text_color="white")
        self.maintenance_description_entry.place(x=40, y=180)

        def submit_maintenance():
            description = self.maintenance_description_entry.get("1.0", "end").strip()
            if description:
                date_today = datetime.today().strftime('%Y-%m-%d')
                cursor.execute("""
                    INSERT INTO maintenance_requests (user_id, description, status, date_submitted)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, description, "Pending", date_today))
                conn.commit()
                ctk.CTkLabel(form_frame, text="Request submitted!", text_color="green").place(relx=0.5, rely=1.1, anchor="center")
                self.maintenance_description_entry.delete("1.0", "end")
            else:
                ctk.CTkLabel(form_frame, text="Please enter a description", text_color="red").place(relx=0.5, rely=1.1, anchor="center")

        submit_img = Image.open("UI/submit.png").resize((50, 50))
        submit_ctk = ctk.CTkImage(light_image=submit_img, size=(50, 50))
        ctk.CTkButton(self, image=submit_ctk, text="", fg_color="white", command=submit_maintenance).place(relx=0.65, rely=0.87, anchor="center")

        conn.close()

    def show_exit_request_screen(self):
        user_id = self.current_user_id
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="#3B3737", bg_color="#3B3737")

        # Background Image
        bg_image = Image.open("UI/user_dashboard_screen.jpg")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=370, height=750, corner_radius=0, fg_color="#3B3737")
        self.sidebar.place(x=0, y=0)

        # Sidebar Greeting
        ctk.CTkLabel(self.sidebar, text="Hello User", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=40)

        # Sidebar Buttons
        nav_buttons = [
            ("View my Room Details", "UI/home-button.png", 200, self.show_user_dashboard),
            ("Rent Payment", "UI/key.png", 260, self.show_rent_payment_screen),
            ("Maintenance Request", "UI/maintainance.png", 320, self.show_maintenance_screen),
            ("Exit Request", "UI/logout.png", 380, self.show_exit_request_screen)
        ]

        for label, icon_path, y_pos, command in nav_buttons:
            button = ctk.CTkButton(self.sidebar, text=label, font=("Arial", 16), fg_color="#3B3737", width=200, height=40, anchor="w", command=command)
            button.place(x=70, y=y_pos)

            icon = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            icon_ctk = ctk.CTkImage(light_image=icon, size=(30, 30))
            icon_label = ctk.CTkLabel(self.sidebar, image=icon_ctk, text="", fg_color="#3B3737")
            icon_label.place(x=40, y=y_pos + 20, anchor="center")
        ctk.CTkLabel(self, text="Exit Request", font=("Arial", 24, "bold"), text_color="black").place(relx=0.65, rely=0.25, anchor="center")

        # Request Frame
        exit_frame = ctk.CTkFrame(self, width=600, height=250, corner_radius=20, fg_color="#1E1E1E")
        exit_frame.place(relx=0.65, rely=0.6, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "white"}
        value_style = {"font": ("Arial", 18), "text_color": "white"}

        # Get user + room info
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="housing_management"
        )
        cursor = conn.cursor()

        student_id = room_number = "N/A"

        cursor.execute("""
            SELECT u.student_id, r.room_number
            FROM users u
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE u.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            student_id, room_number = result

        conn.close()

        # Labels
        ctk.CTkLabel(exit_frame, text="Student ID", **label_style).place(x=40, y=40)
        ctk.CTkLabel(exit_frame, text=str(student_id), **value_style).place(x=300, y=40)

        ctk.CTkLabel(exit_frame, text="Room Number", **label_style).place(x=40, y=90)
        ctk.CTkLabel(exit_frame, text=str(room_number), **value_style).place(x=300, y=90)

        # Submit Button
        def submit_exit_request():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root@123",
                    database="housing_management"
                )
                cursor = conn.cursor()

                # Insert exit request into a hypothetical 'exit_requests' table
                query = """
                    INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                today = datetime.today().strftime('%Y-%m-%d')
                cursor.execute(query, (user_id, "Exit", today, today, "Exit Request", "Pending"))
                conn.commit()

                ctk.CTkLabel(exit_frame, text="Exit Request Submitted!", text_color="green").place(relx=0.5, rely=1.1, anchor="center")
            except mysql.connector.Error as err:
                ctk.CTkLabel(exit_frame, text=f"Error: {err}", text_color="red").place(relx=0.5, rely=1.1, anchor="center")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

        # Submit image button
        submit_icon = Image.open("UI/submit.png").resize((60, 60), Image.LANCZOS)
        submit_ctk = ctk.CTkImage(light_image=submit_icon, size=(60, 60))
        submit_button = ctk.CTkButton(exit_frame, image=submit_ctk, text="", width=60, height=60, fg_color="#1E1E1E", hover_color="#1E1E1E", command=submit_exit_request)
        submit_button.place(relx=0.5, rely=0.85, anchor="center")



    def show_admin_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="white")

        # Background image (left side)
        bg_image = Image.open("UI/login_sceen.png")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(x=0, y=0)

        # Welcome Text
        self.title_label = ctk.CTkLabel(self, text="Welcome Admin", font=("Arial", 26, "bold"), text_color="black")
        self.title_label.place(relx=0.72, rely=0.1, anchor="center")

        # Admin Icon
        admin_icon = Image.open("UI/admin-panel.png").resize((30, 30), Image.LANCZOS)
        self.admin_icon_ctk = ctk.CTkImage(light_image=admin_icon, size=(30, 30))
        self.admin_icon_label = ctk.CTkLabel(self, image=self.admin_icon_ctk, text="")
        self.admin_icon_label.place(relx=0.87, rely=0.1, anchor="center")

        # Button Styles
        button_config = {
            "width": 280,
            "height": 50,
            "fg_color": "#4A4343",
            "hover_color": "#5B5454",
            "font": ("Arial", 20, "bold"),
            "text_color": "black",
            "corner_radius": 8
        }

        # Assign Room Button
        self.assign_room_button = ctk.CTkButton(self, text="  Assign Room", image=ctk.CTkImage(Image.open("UI/user.png").resize((25, 25), Image.LANCZOS)), command=self.show_assign_room_screen, **button_config)
        self.assign_room_button.place(relx=0.75, rely=0.25, anchor="center")

        # Add Room Button
        self.add_room_button = ctk.CTkButton(self, text="  Add Room", image=ctk.CTkImage(Image.open("UI/plus.png").resize((25, 25), Image.LANCZOS)), command=self.show_add_room_screen, **button_config)
        self.add_room_button.place(relx=0.75, rely=0.35, anchor="center")

        # Maintenance Button
        self.maintenance_button = ctk.CTkButton(self, text="  Maintenance", image=ctk.CTkImage(Image.open("UI/maintainance.png").resize((25, 25), Image.LANCZOS)), command=self.show_maintenance_requests_screen, **button_config)
        self.maintenance_button.place(relx=0.75, rely=0.45, anchor="center")

        # Leave Request Button
        self.leave_button = ctk.CTkButton(self, text="  Leave Request", image=ctk.CTkImage(Image.open("UI\logout.png").resize((25, 25), Image.LANCZOS)), command=self.show_leave_requests_screen, **button_config)
        self.leave_button.place(relx=0.75, rely=0.55, anchor="center")

        # Reports Button
        self.report_button = ctk.CTkButton(self, text="  Reports", image=ctk.CTkImage(Image.open("UI/report.png").resize((25, 25), Image.LANCZOS)), command=self.show_reports_screen, **button_config)
        self.report_button.place(relx=0.75, rely=0.65, anchor="center")

        # Logout Button (Image)
        logout_img = Image.open("UI/log-out.png").resize((50, 50), Image.LANCZOS)
        self.logout_ctk = ctk.CTkImage(light_image=logout_img, size=(50, 50))
        self.logout_button = ctk.CTkButton(self, image=self.logout_ctk, text="", fg_color="transparent", hover_color="#DD4A4A", command=self.show_login_screen, width=50, height=50)
        self.logout_button.place(relx=0.75, rely=0.75, anchor="center")
   
    def show_assign_room_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="white")

        # Background image
        bg_image = Image.open("UI/login_sceen.png")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_ctk, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Assign Frame
        assign_frame = ctk.CTkFrame(self, width=500, height=400, corner_radius=20, fg_color="#D3D3D3")
        assign_frame.place(x=680, y=150)

        ctk.CTkLabel(assign_frame, text="Assign Room", font=("Arial", 26, "bold"), text_color="black").place(relx=0.5, rely=0.08, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "black"}
        entry_style = {"width": 200, "height": 35, "fg_color": "#544D4D", "text_color": "white"}

        # Student ID Dropdown
        ctk.CTkLabel(assign_frame, text="Student ID", **label_style).place(x=40, y=60)
        student_id_combo = ctk.CTkComboBox(assign_frame, width=200)
        student_id_combo.place(x=200, y=60)

        # Room No Dropdown
        ctk.CTkLabel(assign_frame, text="Room no.", **label_style).place(x=40, y=110)
        room_no_combo = ctk.CTkComboBox(assign_frame, width=200)
        room_no_combo.place(x=200, y=110)

        # Availability
        ctk.CTkLabel(assign_frame, text="Availability", **label_style).place(x=40, y=160)
        availability_combo = ctk.CTkComboBox(assign_frame, values=["Yes", "No"], width=120)
        availability_combo.place(x=200, y=160)

        # Capacity
        ctk.CTkLabel(assign_frame, text="Capacity", **label_style).place(x=40, y=210)
        capacity_entry = ctk.CTkEntry(assign_frame, **entry_style)
        capacity_entry.place(x=200, y=210)

        # Populate Student ID and Room No
        import mysql.connector
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root@123",
                database="housing_management"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT student_id FROM users")
            student_ids = [str(row[0]) for row in cursor.fetchall()]
            student_id_combo.configure(values=student_ids)

            cursor.execute("SELECT room_number FROM rooms")
            room_numbers = [str(row[0]) for row in cursor.fetchall()]
            room_no_combo.configure(values=room_numbers)

            conn.close()
        except Exception as e:
            print("DB Error:", e)

        # Assign Room Logic
        def assign_room():
            student_id = student_id_combo.get()
            room_number = room_no_combo.get()
            availability = availability_combo.get()
            capacity = capacity_entry.get()

            if not student_id or not room_number or not availability or not capacity:
                messagebox.showwarning("Validation Error", "Please fill in all fields.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root@123",
                    database="housing_management"
                )
                cursor = conn.cursor()

                cursor.execute("SELECT user_id FROM users WHERE student_id = %s", (student_id,))
                user_id = cursor.fetchone()[0]

                cursor.execute("SELECT room_id FROM rooms WHERE room_number = %s", (room_number,))
                room_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO room_allocation (user_id, room_id) VALUES (%s, %s)", (user_id, room_id))
                cursor.execute("UPDATE rooms SET availability=%s, capacity=%s WHERE room_id=%s", (availability, capacity, room_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Room assigned successfully.")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Assign Button
        assign_icon = Image.open("UI/user.png").resize((30, 30), Image.LANCZOS)
        assign_ctk = ctk.CTkImage(light_image=assign_icon, size=(30, 30))
        ctk.CTkButton(assign_frame, text="Assign", image=assign_ctk, compound="right", font=("Arial", 18, "bold"),
                command=assign_room, width=180, height=40, fg_color="#544D4D").place(relx=0.58, y=285, anchor="center")

        # Back Button
        back_image = Image.open("UI/back.png").resize((50, 50), Image.LANCZOS)
        back_ctk = ctk.CTkImage(light_image=back_image, size=(50, 50))
        ctk.CTkButton(self, image=back_ctk, text="", width=50, height=50,
                    fg_color="transparent", hover_color="gray",
                    command=self.show_admin_dashboard).place(x=1150, y=710)



    
    def show_add_room_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="white")

        # Background image
        bg_image = Image.open("UI/login_sceen.png")
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        ctk.CTkLabel(self, image=bg_image_ctk, text="").place(relx=0.5, rely=0.5, anchor="center")

        # Frame for Add Room
        add_room_frame = ctk.CTkFrame(self, width=500, height=400, corner_radius=20, fg_color="#D3D3D3")
        add_room_frame.place(x=680, y=150)

        ctk.CTkLabel(add_room_frame, text="Add Room", font=("Arial", 26, "bold"), text_color="black").place(relx=0.5, rely=0.08, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "black"}
        entry_style = {"width": 200, "height": 35, "fg_color": "#544D4D", "text_color": "white"}

        # Room Number
        ctk.CTkLabel(add_room_frame, text="Room no.", **label_style).place(x=40, y=80)
        room_entry = ctk.CTkEntry(add_room_frame, **entry_style)
        room_entry.place(x=200, y=80)

        # Availability dropdown
        ctk.CTkLabel(add_room_frame, text="Availability", **label_style).place(x=40, y=140)
        availability_combo = ctk.CTkComboBox(add_room_frame, values=["Yes", "No"], width=120)
        availability_combo.place(x=200, y=140)

        # Capacity
        ctk.CTkLabel(add_room_frame, text="Capacity", **label_style).place(x=40, y=200)
        capacity_entry = ctk.CTkEntry(add_room_frame, **entry_style)
        capacity_entry.place(x=200, y=200)

        # Add Room Logic
        def add_room():
            room_no = room_entry.get()
            availability = availability_combo.get()
            capacity = capacity_entry.get()

            if not room_no or not availability or not capacity:
                messagebox.showwarning("Validation Error", "Please fill in all fields.")
                return

            try:
                import mysql.connector
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root@123",
                    database="housing_management"
                )
                cursor = conn.cursor()

                cursor.execute("INSERT INTO rooms (room_number, availability, capacity) VALUES (%s, %s, %s)",
                            (room_no, availability, capacity))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Room added successfully.")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        # Add Button with icon
        add_icon = Image.open("UI/user.png").resize((30, 30), Image.LANCZOS)
        add_ctk = ctk.CTkImage(light_image=add_icon, size=(30, 30))
        ctk.CTkButton(add_room_frame, text="Add", image=add_ctk, compound="right", font=("Arial", 18, "bold"),
                    command=add_room, width=180, height=40, fg_color="#544D4D").place(relx=0.58, y=300, anchor="center")

        # Back Button
        back_image = Image.open("UI/back.png").resize((50, 50), Image.LANCZOS)
        back_ctk = ctk.CTkImage(light_image=back_image, size=(50, 50))
        ctk.CTkButton(self, image=back_ctk, text="", width=50, height=50,
                fg_color="transparent", hover_color="gray",
                command=self.show_admin_dashboard).place(x=1100, y=680)


    def show_maintenance_requests_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="white")

        # Background image
        bg_image = Image.open("UI/request_screen.png").resize((1200, 750), Image.LANCZOS)
        bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        ctk.CTkLabel(self, image=bg_image_ctk, text="").place(relx=0.5, rely=0.5, anchor="center")

        # Frame
        frame = ctk.CTkFrame(self, width=600, height=400, corner_radius=20, fg_color="#D3D3D3")
        frame.place(x=530, y=130)  # Moved slightly to the left

        # Title
        ctk.CTkLabel(self, text="Maintenance Requests", font=("Arial", 24, "bold"), text_color="black").place(x=820, y=80, anchor="center")

        label_style = {"font": ("Arial", 18, "bold"), "text_color": "black"}
        value_style = {"font": ("Arial", 18), "text_color": "white"}

        # Fetch latest pending maintenance request
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="housing_management"
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mr.maintenance_id, u.student_id, r.room_number, mr.description
            FROM maintenance_requests mr
            JOIN users u ON mr.user_id = u.user_id
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE mr.status = 'Pending'
            ORDER BY mr.date_submitted ASC
            LIMIT 1
        """)
        data = cursor.fetchone()
        conn.close()

        if not data:
            ctk.CTkLabel(frame, text="No pending requests", font=("Arial", 18), text_color="black").place(relx=0.5, rely=0.5, anchor="center")
            return

        maintenance_id, student_id, room_no, description = data

        # Student ID
        ctk.CTkLabel(frame, text="Student ID", **label_style).place(x=40, y=40)
        ctk.CTkLabel(frame, text=str(student_id), **value_style, fg_color="#544D4D").place(x=220, y=40)

        # Room No
        ctk.CTkLabel(frame, text="Room No.", **label_style).place(x=40, y=100)
        ctk.CTkLabel(frame, text=str(room_no), **value_style, fg_color="#544D4D").place(x=220, y=100)

        # Description
        ctk.CTkLabel(frame, text="Description", **label_style).place(x=40, y=160)
        desc_box = ctk.CTkTextbox(frame, width=330, height=150, fg_color="#544D4D", text_color="white")
        desc_box.place(x=220, y=160)
        desc_box.insert("1.0", description)
        desc_box.configure(state="disabled")

        # Approve Function
        def approve_request():
            update_status("Closed")

        # Reject Function
        def reject_request():
            update_status("Rejected")

        def update_status(status):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root@123",
                    database="housing_management"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE maintenance_requests SET status=%s, date_resolved=CURDATE() WHERE maintenance_id=%s",
                            (status, maintenance_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Request marked as {status}")
                self.show_maintenance_requests_screen()  # reload screen
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        # Approve and Reject Icons
        approve_img = ctk.CTkImage(Image.open("UI/mark.png").resize((50, 50), Image.LANCZOS))
        reject_img = ctk.CTkImage(Image.open("UI/decline.png").resize((50, 50), Image.LANCZOS))

        ctk.CTkButton(self, image=approve_img, text="", width=50, height=50, fg_color="transparent", command=approve_request).place(x=500, y=550)
        ctk.CTkButton(self, image=reject_img, text="", width=50, height=50, fg_color="transparent", command=reject_request).place(x=600, y=550)

        # Logout (bottom right)
        logout_img = ctk.CTkImage(Image.open("UI/log-out.png").resize((50, 50), Image.LANCZOS))
        ctk.CTkButton(self, image=logout_img, text="", width=50, height=50, fg_color="transparent", command=self.show_login_screen).place(x=1100, y=650)


    def show_leave_requests_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1200x750")
        self.configure(fg_color="white", bg_color="white")

        # Background Image
        bg_image = Image.open("UI/login_sceen.png")  # Adjust image path
        bg_image = bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(light_image=bg_image, size=(1200, 750))
        ctk.CTkLabel(self, image=self.bg_image_ctk, text="").place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(self, text="Leave Requests", font=("Arial", 28, "bold"), text_color="black").place(relx=0.75, rely=0.12, anchor="center")

        # Card
        card = ctk.CTkFrame(self, width=500, height=250, fg_color="#D9D9D9", corner_radius=20)
        card.place(relx=0.75, rely=0.45, anchor="center")

        label_style = {"font": ("Arial", 20, "bold"), "text_color": "black"}
        value_style = {"font": ("Arial", 18), "text_color": "black"}

        # Get next leave request
        conn = mysql.connector.connect(host="localhost", user="root", password="root@123", database="housing_management")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.student_id, r.room_number, lr.leave_id
            FROM leave_requests lr
            JOIN users u ON lr.user_id = u.user_id
            JOIN room_allocation ra ON u.user_id = ra.user_id
            JOIN rooms r ON ra.room_id = r.room_id
            WHERE lr.status = 'Pending'
            ORDER BY lr.start_date ASC
            LIMIT 1
        """)
        data = cursor.fetchone()

        if not data:
            ctk.CTkLabel(card, text="No pending leave requests.", font=("Arial", 18), text_color="red").place(relx=0.5, rely=0.5, anchor="center")
            return

        student_id, room_no, leave_id = data

        # Labels
        ctk.CTkLabel(card, text="Student ID", **label_style).place(x=50, y=50)
        ctk.CTkLabel(card, text=str(student_id), **value_style).place(x=250, y=50)

        ctk.CTkLabel(card, text="Room No.", **label_style).place(x=50, y=120)
        ctk.CTkLabel(card, text=str(room_no), **value_style).place(x=250, y=120)

        # Button Handlers
        def update_leave_status(status):
            cursor.execute("UPDATE leave_requests SET status=%s WHERE leave_id=%s", (status, leave_id))
            conn.commit()
            conn.close()
            self.show_leave_requests_admin()  # reload next pending

        # Buttons
        approve_icon = Image.open("UI/approve.png").resize((40, 40), Image.LANCZOS)
        approve_ctk = ctk.CTkImage(light_image=approve_icon, size=(40, 40))
        ctk.CTkButton(self, image=approve_ctk, text="", width=50, command=lambda: update_leave_status("Approved")).place(relx=0.65, rely=0.75)

        reject_icon = Image.open("UI/reject.png").resize((40, 40), Image.LANCZOS)
        reject_ctk = ctk.CTkImage(light_image=reject_icon, size=(40, 40))
        ctk.CTkButton(self, image=reject_ctk, text="", width=50, command=lambda: update_leave_status("Rejected")).place(relx=0.75, rely=0.75)

        # Logout / Back
        logout_icon = Image.open("UI/log-out.png").resize((50, 50), Image.LANCZOS)
        logout_ctk = ctk.CTkImage(light_image=logout_icon, size=(50, 50))
        ctk.CTkButton(self, image=logout_ctk, text="", fg_color="white", hover_color="white", command=self.show_admin_dashboard).place(relx=0.93, rely=0.93)


    def show_reports_screen(self):
        import mysql.connector
        from fpdf import FPDF
        from tkinter import messagebox

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root@123",
                database="housing_management"
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT u.student_id, u.first_name, u.last_name, u.email,
                    r.room_number, r.capacity, r.availability
                FROM users u
                JOIN room_allocation ra ON u.user_id = ra.user_id
                JOIN rooms r ON ra.room_id = r.room_id
            """)
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("No Data", "No user-room allocation data found.")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="User Room Allocation Report", ln=True, align="C")
            pdf.ln(10)

            headers = ["Student ID", "First Name", "Last Name", "Email", "Room No", "Capacity", "Availability"]
            col_widths = [25, 30, 30, 50, 20, 20, 20]

            # Header Row
            for i in range(len(headers)):
                pdf.cell(col_widths[i], 10, headers[i], border=1)
            pdf.ln()

            # Data Rows
            for row in rows:
                for i in range(len(row)):
                    pdf.cell(col_widths[i], 10, str(row[i]), border=1)
                pdf.ln()

            pdf.output("user_report.pdf")
            messagebox.showinfo("Success", "PDF report downloaded as 'user_report.pdf'")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()







if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
