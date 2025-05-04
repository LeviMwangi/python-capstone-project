import customtkinter as ctk
from db import (
    authenticate_user, add_user, remove_user, update_user, view_users,
    add_tip, update_tip as db_update_tip, remove_tip as db_remove_tip, get_tips,
    view_activities, log_activity
)
from datetime import datetime # Import datetime for timestamp formatting

# Modern color theme setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# Custom color palette
COLORS = {
    "primary": "#4F46E5",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "danger": "#EF4444",
    "background": "#1E293B",
    "text": "#F8FAFC"
}

class SafetyTipsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Safety Tips App")
        self.root.geometry("1000x700")
        self.root.configure(fg_color=COLORS["background"])
        self.user = None
        self.login_page()

    def clear_screen(self):
        """Clear all widgets on the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        """Create a scrollable frame to hold dynamic content."""
        scrollable_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=COLORS["background"],
            scrollbar_button_color=COLORS["primary"],
            scrollbar_button_hover_color=COLORS["secondary"]
        )
        scrollable_frame.pack(fill="both", expand=True)
        return scrollable_frame

    def login_page(self):
        """Display login page UI."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=100, padx=200, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Safety Tips App", font=("Helvetica", 24, "bold"),
                            text_color=COLORS["primary"])
        title.pack(pady=(0, 30))

        # Username entry field
        username_label = ctk.CTkLabel(frame, text="Username:", text_color=COLORS["text"])
        username_label.pack()
        self.username_entry = ctk.CTkEntry(frame, width=300, fg_color="#2D3748", border_color=COLORS["primary"])
        self.username_entry.pack(pady=5)

        # Password entry field
        password_label = ctk.CTkLabel(frame, text="Password:", text_color=COLORS["text"])
        password_label.pack()
        self.password_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"])
        self.password_entry.pack(pady=5)

        # Login button
        login_button = ctk.CTkButton(
            frame, text="Login", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.attempt_login
        )
        login_button.pack(pady=20)

        # Sign up button
        signup_button = ctk.CTkButton(
            frame, text="Sign Up", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.sign_up_page
        )
        signup_button.pack()

    def attempt_login(self):
        """Attempt user login with provided credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.authenticate(username, password)

    def sign_up_page(self):
        """Navigate to sign-up page."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Create Account", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        # Sign-up fields
        self.signup_username = ctk.CTkEntry(frame, width=300, fg_color="#2D3748", border_color=COLORS["primary"],
                                          placeholder_text="Username")
        self.signup_username.pack(pady=5)

        self.signup_password = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"],
                                          placeholder_text="Password")
        self.signup_password.pack(pady=5)

        self.signup_confirm = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"],
                                          placeholder_text="Confirm Password")
        self.signup_confirm.pack(pady=5)

        # Sign-up button
        signup_button = ctk.CTkButton(
            frame, text="Sign Up", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.attempt_signup
        )
        signup_button.pack(pady=20)

        # Back button to login page
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.login_page
        )
        back_button.pack()

    def attempt_signup(self):
        """Attempt to create a new user account."""
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        self.sign_up(username, password, confirm)

    def sign_up(self, username, password, confirm_password):
        """Sign up process with validation."""
        if not username or not password:
            self.show_error("Username and password cannot be empty!")
            return

        if password != confirm_password:
            self.show_error("Passwords do not match!")
            return

        if add_user(username, password):
            self.show_success("User registered successfully!")
            self.login_page()
        else:
            self.show_error("Username already exists!")

    def authenticate(self, username, password):
        """Authenticate user and navigate based on role."""
        user = authenticate_user(username, password)
        if user:
            self.user = user
            log_activity(self.user['id'], "User logged in") # Log successful login
            if user.get("is_admin"):
                AdminDashboard(self.root, self.user)
            else:
                UserDashboard(self.root, self.user)
        else:
            self.show_error("Invalid username or password!")

    def show_error(self, message):
        """Show error messages on the UI."""
        # Clear existing error messages
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["danger"]:
                widget.destroy()

        error = ctk.CTkLabel(self.root, text=message, text_color=COLORS["danger"])
        error.pack(pady=10)
        self.root.after(3000, error.destroy)

    def show_success(self, message):
        """Show success messages on the UI."""
        # Clear existing success messages
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["secondary"]:
                widget.destroy()

        success = ctk.CTkLabel(self.root, text=message, text_color=COLORS["secondary"])
        success.pack(pady=10)
        self.root.after(3000, success.destroy)

class UserDashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.user_dashboard()

    def clear_screen(self):
        """Clear all widgets on the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        """Create a scrollable frame to hold dynamic content."""
        scrollable_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=COLORS["background"],
            scrollbar_button_color=COLORS["primary"],
            scrollbar_button_hover_color=COLORS["secondary"]
        )
        scrollable_frame.pack(fill="both", expand=True)
        return scrollable_frame

    def user_dashboard(self):
        """Display the user dashboard."""
        self.clear_screen()
        frame = self.create_scrollable_frame()

        title = ctk.CTkLabel(frame, text=f"Welcome, {self.user['username']}", font=("Helvetica", 24, "bold"),
                            text_color=COLORS["primary"])
        title.pack(pady=20)

        # --- Navigation Buttons ---
        nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
        nav_frame.pack(pady=20)

        search_tips_button = ctk.CTkButton(
            nav_frame, text="Search Tips", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.search_tips_page
        )
        search_tips_button.pack(side="left", padx=10)

        settings_button = ctk.CTkButton(
            nav_frame, text="Settings", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.settings_page
        )
        settings_button.pack(side="left", padx=10)

        logout_button = ctk.CTkButton(
            nav_frame, text="Logout", fg_color=COLORS["danger"], hover_color="#EF4444",
            command=self.logout
        )
        logout_button.pack(side="left", padx=10)
        # --- End Navigation Buttons ---

        # Default view: Search tips
        self.search_tips_page(frame) # Pass the frame to add search elements

    def search_tips_page(self, parent_frame=None):
        """Display search functionality and search results."""
        if parent_frame is None:
            # If navigating directly to search page, clear and create new frame
            self.clear_screen()
            frame = self.create_scrollable_frame()
            self.add_user_dashboard_nav(frame) # Add navigation buttons back
        else:
             # If called from dashboard, use the existing frame
             frame = parent_frame
             # Clear previous content within the frame (except navigation)
             for widget in frame.winfo_children():
                 if widget not in frame.winfo_children()[:1] and widget.cget("text") not in ["Search Tips", "Settings", "Logout"]: # Keep title and nav
                     widget.destroy()


        search_frame = ctk.CTkFrame(frame, fg_color="#2D3748")
        search_frame.pack(pady=10, padx=10, fill="x")

        search_label = ctk.CTkLabel(search_frame, text="Search Safety Tips by Title:", text_color=COLORS["text"])
        search_label.pack(side="left", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, width=300, fg_color="#1E293B", border_color=COLORS["primary"])
        self.search_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        self.search_entry.bind("<Return>", lambda event=None: self.perform_search(frame)) # Bind Enter key

        search_button = ctk.CTkButton(
            search_frame, text="Search", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=lambda: self.perform_search(frame)
        )
        search_button.pack(side="left", padx=10, pady=5)

        # Frame to hold search results
        self.results_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display all tips initially when coming from dashboard
        if parent_frame is not None:
             self.display_tips(get_tips(), self.results_frame)


    def perform_search(self, parent_frame):
        """Perform the search and display results."""
        query = self.search_entry.get()
        tips = get_tips(search_query=query) # Use the search_query parameter

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.display_tips(tips, self.results_frame)


    def display_tips(self, tips, parent_frame):
         """Helper function to display a list of tips in a given frame."""
         if not tips:
             no_tips_label = ctk.CTkLabel(parent_frame, text="No matching safety tips found.", text_color=COLORS["text"])
             no_tips_label.pack(pady=10)
         else:
             for tip in tips:
                 tip_frame = ctk.CTkFrame(parent_frame, fg_color="#2D3748")
                 tip_frame.pack(fill="x", pady=5, ipady=10)

                 tip_title = ctk.CTkLabel(tip_frame, text=tip['title'], font=("Helvetica", 16, "bold"),
                                        text_color=COLORS["accent"])
                 tip_title.pack(anchor="w", padx=10)

                 tip_content = ctk.CTkLabel(tip_frame, text=tip['content'], text_color=COLORS["text"],
                                           wraplength=800, justify="left")
                 tip_content.pack(anchor="w", padx=10, pady=5)


    def settings_page(self):
        """Display user settings page."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="User Settings", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        # Display Username
        username_label = ctk.CTkLabel(frame, text=f"Username: {self.user['username']}", text_color=COLORS["text"])
        username_label.pack(pady=10)

        # Display Account Creation Date
        created_at = self.user.get('created_at')
        if isinstance(created_at, datetime):
             created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
             created_at_str = str(created_at) # Handle potential non-datetime values

        created_label = ctk.CTkLabel(frame, text=f"Account Created: {created_at_str}", text_color=COLORS["text"])
        created_label.pack(pady=5)

        # --- Change Password Section ---
        password_title = ctk.CTkLabel(frame, text="Change Password", font=("Helvetica", 16, "bold"),
                                     text_color=COLORS["accent"])
        password_title.pack(pady=(20, 10))

        new_password_label = ctk.CTkLabel(frame, text="New Password:", text_color=COLORS["text"])
        new_password_label.pack(pady=5)
        self.new_password_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"])
        self.new_password_entry.pack(pady=5)

        confirm_password_label = ctk.CTkLabel(frame, text="Confirm New Password:", text_color=COLORS["text"])
        confirm_password_label.pack(pady=5)
        self.confirm_new_password_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"])
        self.confirm_new_password_entry.pack(pady=5)

        update_password_button = ctk.CTkButton(
            frame, text="Update Password", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.update_user_password
        )
        update_password_button.pack(pady=20)
        # --- End Change Password Section ---


        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back to Dashboard", fg_color="#64748B", hover_color="#475569",
            command=self.user_dashboard # Go back to the main dashboard view
        )
        back_button.pack(pady=10)

    def update_user_password(self):
        """Update the user's password."""
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_new_password_entry.get()

        if not new_password:
            self.show_error("New password cannot be empty!")
            return

        if new_password != confirm_password:
            self.show_error("Passwords do not match!")
            return

        # Call the db function to update only the password
        if update_user(self.user['id'], new_password=new_password):
            log_activity(self.user['id'], "User updated password") # Log activity
            self.show_success("Password updated successfully!")
            # Clear the password fields after successful update
            self.new_password_entry.delete(0, ctk.END)
            self.confirm_new_password_entry.delete(0, ctk.END)
        else:
            self.show_error("Failed to update password.")

    def add_user_dashboard_nav(self, frame):
        """Helper to add navigation buttons back to a page."""
        nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
        nav_frame.pack(pady=20)

        search_tips_button = ctk.CTkButton(
            nav_frame, text="Search Tips", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.search_tips_page
        )
        search_tips_button.pack(side="left", padx=10)

        settings_button = ctk.CTkButton(
            nav_frame, text="Settings", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.settings_page
        )
        settings_button.pack(side="left", padx=10)

        logout_button = ctk.CTkButton(
            nav_frame, text="Logout", fg_color=COLORS["danger"], hover_color="#EF4444",
            command=self.logout
        )
        logout_button.pack(side="left", padx=10)


    def logout(self):
        """Log out the user."""
        if self.user:
            log_activity(self.user['id'], "User logged out") # Log logout
        SafetyTipsApp(self.root)

    def show_error(self, message):
        """Show error messages on the UI."""
        # Clear existing error messages
        # Find the frame containing the dashboard content (which is the scrollable frame)
        # and look for error labels within it.
        dashboard_frame = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                dashboard_frame = widget
                break

        if dashboard_frame:
            for widget in dashboard_frame.winfo_children():
                 # Check widgets within the dashboard frame and its sub-frames
                 if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["danger"]:
                     widget.destroy()

        error = ctk.CTkLabel(dashboard_frame if dashboard_frame else self.root, text=message, text_color=COLORS["danger"])
        error.pack(pady=10)
        self.root.after(3000, error.destroy)


    def show_success(self, message):
        """Show success messages on the UI."""
        # Clear existing success messages
         # Find the frame containing the dashboard content (which is the scrollable frame)
        # and look for success labels within it.
        dashboard_frame = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                dashboard_frame = widget
                break

        if dashboard_frame:
            for widget in dashboard_frame.winfo_children():
                 # Check widgets within the dashboard frame and its sub-frames
                 if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["secondary"]:
                     widget.destroy()


        success = ctk.CTkLabel(dashboard_frame if dashboard_frame else self.root, text=message, text_color=COLORS["secondary"])
        success.pack(pady=10)
        self.root.after(3000, success.destroy)


# Admin Dashboard class
class AdminDashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.admin_dashboard()

    def clear_screen(self):
        """Clear all widgets on the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        """Create a scrollable frame to hold dynamic content."""
        scrollable_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=COLORS["background"],
            scrollbar_button_color=COLORS["primary"],
            scrollbar_button_hover_color=COLORS["secondary"]
        )
        scrollable_frame.pack(fill="both", expand=True)
        return scrollable_frame

    def admin_dashboard(self):
        """Display the admin dashboard."""
        self.clear_screen()
        frame = self.create_scrollable_frame()

        title = ctk.CTkLabel(frame, text=f"Admin Dashboard - Welcome {self.user['username']}",
                            font=("Helvetica", 24, "bold"), text_color=COLORS["primary"])
        title.pack(pady=20)

        # Manage Users section
        manage_users_button = ctk.CTkButton(
            frame, text="Manage Users", fg_color=COLORS["secondary"], hover_color="#10B981",
            command=self.manage_users
        )
        manage_users_button.pack(pady=10)

        # Manage Tips section
        manage_tips_button = ctk.CTkButton(
            frame, text="Manage Tips", fg_color=COLORS["accent"], hover_color="#F59E0B",
            command=self.manage_tips
        )
        manage_tips_button.pack(pady=10)

        # View Activities section
        view_activities_button = ctk.CTkButton(
            frame, text="View Activities", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.view_activities
        )
        view_activities_button.pack(pady=10)

        # Logout button
        logout_button = ctk.CTkButton(
            frame, text="Logout", fg_color=COLORS["danger"], hover_color="#EF4444",
            command=self.logout
        )
        logout_button.pack(pady=20)

    def logout(self):
        """Log out the admin."""
        if self.user:
            log_activity(self.user['id'], "Admin logged out") # Log logout
        SafetyTipsApp(self.root)

    def manage_users(self):
        """Allow the admin to manage users (view, add, remove)."""
        self.clear_screen()
        frame = self.create_scrollable_frame()

        title = ctk.CTkLabel(frame, text="Manage Users", font=("Helvetica", 20, "bold"), text_color=COLORS["primary"])
        title.pack(pady=20)

        # Display users list
        users = view_users() # Use view_users from db.py
        if not users:
             no_users_label = ctk.CTkLabel(frame, text="No users found.", text_color=COLORS["text"])
             no_users_label.pack(pady=10)
        else:
            for user in users:
                user_frame = ctk.CTkFrame(frame, fg_color="#2D3748")
                user_frame.pack(fill="x", padx=10, pady=5, ipady=10)

                user_label = ctk.CTkLabel(user_frame,
                                        text=f"Username: {user['username']}, Role: {'Admin' if user['is_admin'] else 'User'}",
                                        text_color=COLORS["text"])
                user_label.pack(side="left", padx=10)

                # Edit and delete buttons for each user
                button_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=10)

                # Prevent admin from deleting themselves
                if user['id'] != self.user['id']:
                    edit_button = ctk.CTkButton(
                        button_frame, text="Edit", fg_color=COLORS["primary"], hover_color="#4338CA",
                        command=lambda user_id=user['id']: self.edit_user(user_id)
                    )
                    edit_button.pack(side="left", padx=5)

                    delete_button = ctk.CTkButton(
                        button_frame, text="Delete", fg_color=COLORS["danger"], hover_color="#EF4444",
                        command=lambda user_id=user['id']: self.remove_user(user_id)
                    )
                    delete_button.pack(side="left", padx=5)
                else:
                    # Optional: Add a label indicating the current user
                    current_user_label = ctk.CTkLabel(button_frame, text="(Current Admin)", text_color=COLORS["accent"])
                    current_user_label.pack(side="left", padx=5)


        # Add User Button
        add_user_button = ctk.CTkButton(
            frame, text="Add User", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.add_user_page
        )
        add_user_button.pack(pady=10)

        # Back to Admin Dashboard
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.admin_dashboard
        )
        back_button.pack(pady=10)

    def add_user_page(self):
        """Allow the admin to add a new user."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Add New User", font=("Helvetica", 20, "bold"), text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        username_label = ctk.CTkLabel(frame, text="Username", text_color=COLORS["text"])
        username_label.pack(pady=5)
        self.add_user_username_entry = ctk.CTkEntry(frame, width=300, fg_color="#2D3748", border_color=COLORS["primary"])
        self.add_user_username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(frame, text="Password", text_color=COLORS["text"])
        password_label.pack(pady=5)
        self.add_user_password_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"])
        self.add_user_password_entry.pack(pady=5)

        confirm_label = ctk.CTkLabel(frame, text="Confirm Password", text_color=COLORS["text"])
        confirm_label.pack(pady=5)
        self.add_user_confirm_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748", border_color=COLORS["primary"])
        self.add_user_confirm_entry.pack(pady=5)

        # Checkbox for admin status
        self.is_admin_var = ctk.BooleanVar()
        is_admin_checkbox = ctk.CTkCheckBox(frame, text="Make Admin", variable=self.is_admin_var,
                                            fg_color=COLORS["primary"], hover_color=COLORS["secondary"])
        is_admin_checkbox.pack(pady=10)


        submit_button = ctk.CTkButton(
            frame, text="Submit", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.submit_new_user
        )
        submit_button.pack(pady=10)

        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.manage_users
        )
        back_button.pack(pady=10)

    def submit_new_user(self):
        """Submit new user creation."""
        username = self.add_user_username_entry.get()
        password = self.add_user_password_entry.get()
        confirm_password = self.add_user_confirm_entry.get()
        is_admin = self.is_admin_var.get()

        if not username or not password or not confirm_password:
            self.show_error("All fields are required!")
            return

        if password != confirm_password:
            self.show_error("Passwords do not match!")
            return

        if add_user(username, password, is_admin): # Use add_user from db.py
            log_activity(self.user['id'], f"Added user: {username}") # Log activity
            self.show_success(f"User '{username}' added successfully!")
            self.manage_users()
        else:
            self.show_error(f"Failed to add user '{username}'. Username might already exist.")

    def remove_user(self, user_id):
        """Remove a user from the system."""
        # Add a confirmation dialog
        confirm = ctk.CTkInputDialog(text="Are you sure you want to delete this user? Type 'YES' to confirm.", title="Confirm Deletion")
        response = confirm.get_input()

        if response == "YES":
            # Fetch username before deleting for logging
            users = view_users()
            username_to_delete = next((u['username'] for u in users if u['id'] == user_id), "Unknown User")

            if remove_user(user_id): # Use remove_user from db.py
                log_activity(self.user['id'], f"Removed user: {username_to_delete}") # Log activity
                self.show_success(f"User removed successfully!")
                self.manage_users()
            else:
                self.show_error(f"Failed to remove user.")
        else:
            self.show_error("Deletion cancelled.")


    def edit_user(self, user_id):
        """Edit user information."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        # Fetch current user data
        users = view_users()
        current_user = next((u for u in users if u['id'] == user_id), None)

        if not current_user:
            self.show_error("User not found!")
            self.manage_users()
            return

        title = ctk.CTkLabel(frame, text=f"Edit User: {current_user['username']}", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        # Username field (optional edit)
        username_label = ctk.CTkLabel(frame, text="Username", text_color=COLORS["text"])
        username_label.pack(pady=5)
        self.edit_user_username_entry = ctk.CTkEntry(frame, width=300, fg_color="#2D3748",
                                             border_color=COLORS["primary"])
        self.edit_user_username_entry.insert(0, current_user['username'])
        self.edit_user_username_entry.pack(pady=5)


        new_password_label = ctk.CTkLabel(frame, text="New Password (leave blank to keep current)",
                                         text_color=COLORS["text"])
        new_password_label.pack(pady=5)
        self.edit_user_new_password_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748",
                                             border_color=COLORS["primary"])
        self.edit_user_new_password_entry.pack(pady=5)

        confirm_label = ctk.CTkLabel(frame, text="Confirm New Password", text_color=COLORS["text"])
        confirm_label.pack(pady=5)
        self.edit_user_confirm_new_entry = ctk.CTkEntry(frame, width=300, show="*", fg_color="#2D3748",
                                           border_color=COLORS["primary"])
        self.edit_user_confirm_new_entry.pack(pady=5)

        # Checkbox for admin status (only if not editing yourself)
        if user_id != self.user['id']:
            self.edit_user_is_admin_var = ctk.BooleanVar(value=current_user['is_admin'])
            edit_is_admin_checkbox = ctk.CTkCheckBox(frame, text="Is Admin", variable=self.edit_user_is_admin_var,
                                                    fg_color=COLORS["primary"], hover_color=COLORS["secondary"])
            edit_is_admin_checkbox.pack(pady=10)
        else:
            # Display current admin status if editing yourself
            admin_status_label = ctk.CTkLabel(frame, text="Role: Admin", text_color=COLORS["accent"])
            admin_status_label.pack(pady=10)
            self.edit_user_is_admin_var = None # No variable to update


        submit_button = ctk.CTkButton(
            frame, text="Update", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=lambda: self.update_user(user_id)
        )
        submit_button.pack(pady=10)

        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.manage_users
        )
        back_button.pack(pady=10)

    def update_user(self, user_id):
        """Update user information."""
        new_username = self.edit_user_username_entry.get()
        new_password = self.edit_user_new_password_entry.get()
        confirm_password = self.edit_user_confirm_new_entry.get()
        is_admin = self.edit_user_is_admin_var.get() if self.edit_user_is_admin_var else None # Get value only if checkbox exists

        if new_password and new_password != confirm_password:
            self.show_error("Passwords do not match!")
            return

        # Determine which fields to update
        update_username = new_username # Always try to update username if changed
        update_password = new_password if new_password else None # Only update password if a new one is provided
        update_admin_status = is_admin # Update admin status if checkbox exists

        if update_user(user_id, new_username=update_username, new_password=update_password, is_admin=update_admin_status): # Use update_user from db.py
            # Log activity (handle username change)
            activity_message = f"Updated user ID: {user_id}"
            if new_username:
                 activity_message += f" (Username changed to: {new_username})"
            if new_password:
                 activity_message += " (Password updated)"
            if self.edit_user_is_admin_var is not None: # Check if admin status was editable
                 activity_message += f" (Admin status set to: {is_admin})"

            log_activity(self.user['id'], activity_message)
            self.show_success("User updated successfully!")
            self.manage_users()
        else:
            self.show_error("Failed to update user.")


    def manage_tips(self):
        """Allow the admin to manage safety tips."""
        self.clear_screen()
        frame = self.create_scrollable_frame()

        title = ctk.CTkLabel(frame, text="Manage Safety Tips", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=20)

        # Add Tip Button (moved to its own page)
        add_tip_button = ctk.CTkButton(
            frame, text="Add New Tip", fg_color=COLORS["primary"], hover_color="#4338CA",
            command=self.add_tip_page
        )
        add_tip_button.pack(pady=10)

        # Display tips in a lighter format
        tips = get_tips()
        if not tips:
            no_tips_label = ctk.CTkLabel(frame, text="No safety tips available.", text_color=COLORS["text"])
            no_tips_label.pack(pady=10)
        else:
            for tip in tips:
                tip_summary_frame = ctk.CTkFrame(frame, fg_color="#2D3748")
                tip_summary_frame.pack(fill="x", padx=10, pady=3) # Reduced vertical padding

                tip_title_label = ctk.CTkLabel(tip_summary_frame, text=tip['title'], font=("Helvetica", 14, "bold"),
                                             text_color=COLORS["accent"])
                tip_title_label.pack(side="left", padx=10, pady=5)

                # Edit and delete buttons
                button_frame = ctk.CTkFrame(tip_summary_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=10)

                edit_button = ctk.CTkButton(
                    button_frame, text="Edit", fg_color=COLORS["primary"], hover_color="#4338CA", width=70, # Reduced width
                    command=lambda tip_id=tip['tip_id']: self.edit_tip(tip_id)
                )
                edit_button.pack(side="left", padx=5)

                delete_button = ctk.CTkButton(
                    button_frame, text="Delete", fg_color=COLORS["danger"], hover_color="#EF4444", width=70, # Reduced width
                    command=lambda tip_id=tip['tip_id']: self.delete_tip(tip_id)
                )
                delete_button.pack(side="left", padx=5)

        # Back to Admin Dashboard
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.admin_dashboard
        )
        back_button.pack(pady=10)


    def add_tip_page(self):
        """Allow the admin to add a new safety tip."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Add New Safety Tip", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        title_label = ctk.CTkLabel(frame, text="Title", text_color=COLORS["text"])
        title_label.pack(pady=5)
        self.add_tip_title_entry = ctk.CTkEntry(frame, width=300, fg_color="#2D3748", border_color=COLORS["primary"])
        self.add_tip_title_entry.pack(pady=5)

        content_label = ctk.CTkLabel(frame, text="Content", text_color=COLORS["text"])
        content_label.pack(pady=5)
        self.add_tip_content_entry = ctk.CTkTextbox(frame, width=300, height=150, fg_color="#2D3748",
                                              border_color=COLORS["primary"])
        self.add_tip_content_entry.pack(pady=5)

        submit_button = ctk.CTkButton(
            frame, text="Submit", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=self.submit_new_tip
        )
        submit_button.pack(pady=10)

        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back to Manage Tips", fg_color="#64748B", hover_color="#475569",
            command=self.manage_tips # Go back to the manage tips page after adding
        )
        back_button.pack(pady=10)

    def submit_new_tip(self):
        """Submit new safety tip."""
        title = self.add_tip_title_entry.get()
        content = self.add_tip_content_entry.get("1.0", "end-1c")

        if not title or not content.strip(): # Check for empty content after stripping whitespace
            self.show_error("Title and content cannot be empty!")
            return

        if add_tip(title, content.strip()): # Use add_tip from db.py
            log_activity(self.user['id'], f"Added safety tip: '{title}'") # Log activity
            self.show_success("Safety tip added successfully!")
            self.manage_tips() # Navigate back to manage tips after successful addition
        else:
            self.show_error("Failed to add safety tip.")

    def edit_tip(self, tip_id):
        """Edit an existing safety tip."""
        self.clear_screen()
        frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        frame.pack(pady=50, padx=200, fill="both", expand=True)

        # Fetch the current tip data
        tips = get_tips()
        current_tip = next((t for t in tips if t['tip_id'] == tip_id), None)

        if not current_tip:
            self.show_error("Safety tip not found!")
            self.manage_tips()
            return


        title = ctk.CTkLabel(frame, text=f"Edit Safety Tip", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=(0, 20))

        title_label = ctk.CTkLabel(frame, text="Title", text_color=COLORS["text"])
        title_label.pack(pady=5)
        self.edit_tip_title_entry = ctk.CTkEntry(frame, width=300, fg_color="#2D3748",
                                              border_color=COLORS["primary"])
        self.edit_tip_title_entry.insert(0, current_tip['title'])
        self.edit_tip_title_entry.pack(pady=5)

        content_label = ctk.CTkLabel(frame, text="Content", text_color=COLORS["text"])
        content_label.pack(pady=5)
        self.edit_tip_content_entry = ctk.CTkTextbox(frame, width=300, height=150, fg_color="#2D3748",
                                                   border_color=COLORS["primary"])
        self.edit_tip_content_entry.insert("1.0", current_tip['content'])
        self.edit_tip_content_entry.pack(pady=5)

        submit_button = ctk.CTkButton(
            frame, text="Update", fg_color=COLORS["secondary"], hover_color="#0D9488",
            command=lambda: self.update_tip(tip_id) # Pass tip_id
        )
        submit_button.pack(pady=10)

        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back to Manage Tips", fg_color="#64748B", hover_color="#475569",
            command=self.manage_tips # Go back to the manage tips page after updating
        )
        back_button.pack(pady=10)

    def update_tip(self, tip_id):
        """Update safety tip information."""
        title = self.edit_tip_title_entry.get()
        content = self.edit_tip_content_entry.get("1.0", "end-1c")

        if not title or not content.strip(): # Check for empty content after stripping whitespace
            self.show_error("Title and content cannot be empty!")
            return

        if db_update_tip(tip_id, title, content.strip()): # Use db_update_tip from db.py
            log_activity(self.user['id'], f"Updated safety tip ID: {tip_id} ('{title}')") # Log activity
            self.show_success("Safety tip updated successfully!")
            self.manage_tips()
        else:
            self.show_error("Failed to update safety tip.")

    def delete_tip(self, tip_id):
        """Delete a safety tip."""
         # Add a confirmation dialog
        confirm = ctk.CTkInputDialog(text="Are you sure you want to delete this tip? Type 'YES' to confirm.", title="Confirm Deletion")
        response = confirm.get_input()

        if response == "YES":
            # Fetch tip title before deleting for logging
            tips = get_tips()
            tip_title_to_delete = next((t['title'] for t in tips if t['tip_id'] == tip_id), "Unknown Tip")

            if db_remove_tip(tip_id): # Use db_remove_tip from db.py
                log_activity(self.user['id'], f"Deleted safety tip: '{tip_title_to_delete}' (ID: {tip_id})") # Log activity
                self.show_success("Safety tip deleted successfully!")
                self.manage_tips()
            else:
                self.show_error("Failed to delete safety tip.")
        else:
            self.show_error("Deletion cancelled.")


    def view_activities(self):
        """View system activities."""
        self.clear_screen()
        frame = self.create_scrollable_frame()

        title = ctk.CTkLabel(frame, text="System Activities", font=("Helvetica", 20, "bold"),
                           text_color=COLORS["primary"])
        title.pack(pady=20)

        activities = view_activities() # Use view_activities from db.py
        if not activities:
            no_activities_label = ctk.CTkLabel(frame, text="No activities found.", text_color=COLORS["text"])
            no_activities_label.pack(pady=10)
        else:
            for activity in activities:
                activity_frame = ctk.CTkFrame(frame, fg_color="#2D3748")
                activity_frame.pack(fill="x", padx=10, pady=5, ipady=10)

                # Ensure timestamp is formatted nicely
                timestamp_str = activity['timestamp'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(activity['timestamp'], datetime) else str(activity['timestamp'])

                # Get username from user_id
                username = "Unknown User"
                users = view_users()
                for user in users:
                    if user['id'] == activity['user_id']:
                        username = user['username']
                        break

                activity_text = f"{timestamp_str} - {username}: {activity['activity']}"
                activity_label = ctk.CTkLabel(activity_frame, text=activity_text, text_color=COLORS["text"],
                                            wraplength=800, justify="left")
                activity_label.pack(anchor="w", padx=10, pady=5)

        # Back button
        back_button = ctk.CTkButton(
            frame, text="Back", fg_color="#64748B", hover_color="#475569",
            command=self.admin_dashboard
        )
        back_button.pack(pady=20)

    def show_error(self, message):
        """Show error messages on the UI."""
        # Clear existing error messages
        # Find the frame containing the dashboard content (which is the scrollable frame)
        # and look for error labels within it.
        dashboard_frame = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                dashboard_frame = widget
                break

        if dashboard_frame:
            for widget in dashboard_frame.winfo_children():
                 # Check widgets within the dashboard frame and its sub-frames
                 if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["danger"]:
                     widget.destroy()
                 # Also check within nested frames like the search frame
                 if isinstance(widget, ctk.CTkFrame):
                      for sub_widget in widget.winfo_children():
                           if isinstance(sub_widget, ctk.CTkLabel) and sub_widget.cget("text_color") == COLORS["danger"]:
                                sub_widget.destroy()


        error = ctk.CTkLabel(dashboard_frame if dashboard_frame else self.root, text=message, text_color=COLORS["danger"])
        error.pack(pady=10)
        self.root.after(3000, error.destroy)


    def show_success(self, message):
        """Show success messages on the UI."""
        # Clear existing success messages
         # Find the frame containing the dashboard content (which is the scrollable frame)
        # and look for success labels within it.
        dashboard_frame = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                dashboard_frame = widget
                break

        if dashboard_frame:
            for widget in dashboard_frame.winfo_children():
                 # Check widgets within the dashboard frame and its sub-frames
                 if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == COLORS["secondary"]:
                     widget.destroy()
                 # Also check within nested frames like the search frame
                 if isinstance(widget, ctk.CTkFrame):
                      for sub_widget in widget.winfo_children():
                           if isinstance(sub_widget, ctk.CTkLabel) and sub_widget.cget("text_color") == COLORS["secondary"]:
                                sub_widget.destroy()


        success = ctk.CTkLabel(dashboard_frame if dashboard_frame else self.root, text=message, text_color=COLORS["secondary"])
        success.pack(pady=10)
        self.root.after(3000, success.destroy)


# Main application entry point
if __name__ == "__main__":
    root = ctk.CTk()
    app = SafetyTipsApp(root)
    root.mainloop()