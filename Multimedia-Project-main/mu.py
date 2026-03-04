import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
import shutil
import hashlib
import webbrowser
import tempfile


class AccountManager:
    """Manages user accounts and authentication"""
    def __init__(self, accounts_file="accounts_data.json"):
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        """Load existing accounts from file"""
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_accounts(self):
        """Save accounts to file"""
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def account_exists(self, username):
        """Check if account exists"""
        return any(acc['username'] == username for acc in self.accounts)
    
    def register(self, username, password):
        """Create new account"""
        if self.account_exists(username):
            return False, "Username already exists!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters!"
        
        account = {
            'username': username,
            'password': self.hash_password(password),
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.accounts.append(account)
        self.save_accounts()
        return True, "Account created successfully!"
    
    def login(self, username, password):
        """Verify login credentials"""
        for account in self.accounts:
            if account['username'] == username:
                if account['password'] == self.hash_password(password):
                    return True, "Login successful!"
                else:
                    return False, "Incorrect password!"
        return False, "Username not found!"


class LoginWindow:
    """Login and Registration window"""
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Alley - Login")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        self.root.minsize(400, 500)
        
        self.account_manager = AccountManager()
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display login screen"""
        self.clear_window()
        
        # Main container
        container = tk.Frame(self.root, bg="#2c3e50")
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=60)
        
        # Title
        title = tk.Label(container, text="🎬 Asset Alley", 
                        font=("Arial", 28, "bold"), 
                        fg="white", bg="#2c3e50")
        title.pack(pady=(0, 20))
        
        # Subtitle
        subtitle = tk.Label(container, text="Multimedia Project Manager", 
                           font=("Arial", 12), 
                           fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack(pady=(0, 40))
        
        # Username
        tk.Label(container, text="Username", font=("Arial", 11, "bold"), 
                fg="white", bg="#2c3e50").pack(anchor=tk.W)
        self.login_username = tk.Entry(container, font=("Arial", 12), 
                                       relief=tk.FLAT, bg="#ecf0f1")
        self.login_username.pack(fill=tk.X, pady=(5, 20), ipady=8)
        self.login_username.focus()
        
        # Password
        tk.Label(container, text="Password", font=("Arial", 11, "bold"), 
                fg="white", bg="#2c3e50").pack(anchor=tk.W)
        self.login_password = tk.Entry(container, font=("Arial", 12), 
                                       relief=tk.FLAT, bg="#ecf0f1", show="•")
        self.login_password.pack(fill=tk.X, pady=(5, 30), ipady=8)
        self.login_password.bind('<Return>', lambda e: self.do_login())
        
        # Login button
        login_btn = tk.Button(container, text="Login", 
                             font=("Arial", 12, "bold"),
                             bg="#3498db", fg="white", 
                             relief=tk.FLAT, cursor="hand2",
                             command=self.do_login, padx=20, pady=10)
        login_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Register link
        register_btn = tk.Button(container, text="Create New Account", 
                                font=("Arial", 10),
                                bg="#27ae60", fg="white", 
                                relief=tk.FLAT, cursor="hand2",
                                command=self.show_register_screen, padx=20, pady=10)
        register_btn.pack(fill=tk.X)
        
        # Error message label
        self.error_label = tk.Label(container, text="", 
                                   font=("Arial", 10), 
                                   fg="#e74c3c", bg="#2c3e50")
        self.error_label.pack(pady=(20, 0))
    
    def show_register_screen(self):
        """Display registration screen"""
        self.clear_window()
        
        # Main container
        container = tk.Frame(self.root, bg="#2c3e50")
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(container, text="Create Account", 
                        font=("Arial", 24, "bold"), 
                        fg="white", bg="#2c3e50")
        title.pack(pady=(0, 30))
        
        # Username
        tk.Label(container, text="Username", font=("Arial", 11, "bold"), 
                fg="white", bg="#2c3e50").pack(anchor=tk.W)
        self.reg_username = tk.Entry(container, font=("Arial", 12), 
                                     relief=tk.FLAT, bg="#ecf0f1")
        self.reg_username.pack(fill=tk.X, pady=(5, 20), ipady=8)
        self.reg_username.focus()
        
        # Password
        tk.Label(container, text="Password", font=("Arial", 11, "bold"), 
                fg="white", bg="#2c3e50").pack(anchor=tk.W)
        self.reg_password = tk.Entry(container, font=("Arial", 12), 
                                     relief=tk.FLAT, bg="#ecf0f1", show="•")
        self.reg_password.pack(fill=tk.X, pady=(5, 20), ipady=8)
        
        # Confirm Password
        tk.Label(container, text="Confirm Password", font=("Arial", 11, "bold"), 
                fg="white", bg="#2c3e50").pack(anchor=tk.W)
        self.reg_confirm = tk.Entry(container, font=("Arial", 12), 
                                    relief=tk.FLAT, bg="#ecf0f1", show="•")
        self.reg_confirm.pack(fill=tk.X, pady=(5, 30), ipady=8)
        self.reg_confirm.bind('<Return>', lambda e: self.do_register())
        
        # Register button
        register_btn = tk.Button(container, text="Create Account", 
                                font=("Arial", 12, "bold"),
                                bg="#27ae60", fg="white", 
                                relief=tk.FLAT, cursor="hand2",
                                command=self.do_register, padx=20, pady=10)
        register_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_btn = tk.Button(container, text="Back to Login", 
                            font=("Arial", 10),
                            bg="#3498db", fg="white", 
                            relief=tk.FLAT, cursor="hand2",
                            command=self.show_login_screen, padx=20, pady=10)
        back_btn.pack(fill=tk.X)
        
        # Error message label
        self.error_label = tk.Label(container, text="", 
                                   font=("Arial", 10), 
                                   fg="#e74c3c", bg="#2c3e50")
        self.error_label.pack(pady=(20, 0))
    
    def do_login(self):
        """Process login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            self.error_label.config(text="Please fill in all fields!")
            return
        
        success, message = self.account_manager.login(username, password)
        
        if success:
            # Close login window and open main app
            self.root.destroy()
            main_root = tk.Tk()
            app = MultimediaProjectManager(main_root, username)
            main_root.mainloop()
        else:
            self.error_label.config(text=message)
    
    def do_register(self):
        """Process registration"""
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not username or not password or not confirm:
            self.error_label.config(text="Please fill in all fields!")
            return
        
        if password != confirm:
            self.error_label.config(text="Passwords don't match!")
            return
        
        success, message = self.account_manager.register(username, password)
        
        if success:
            self.error_label.config(text="✓ " + message)
            self.root.after(1500, self.show_login_screen)
        else:
            self.error_label.config(text=message)


class MultimediaProjectManager:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Asset Alley - Multimedia Project Manager")
        self.root.geometry("1200x700")
        # give the window an icon if you have one
        # self.root.iconbitmap('assets/icon.ico')

        # make resizing more polished
        self.root.minsize(900, 600)
        self.root.configure(bg="#f0f0f0")
        
        # apply a modern ttk theme and custom styles
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        # general font
        default_font = ("Segoe UI", 10)
        self.style.configure('TLabel', font=default_font)
        self.style.configure('TEntry', font=default_font)
        self.style.configure('TCombobox', font=default_font)
        self.style.configure('Accent.TButton', background='#3498db', foreground='white', font=("Segoe UI", 10, "bold"), focuscolor='none')
        self.style.configure('Success.TButton', background='#27ae60', foreground='white', font=("Segoe UI", 10, "bold"), focuscolor='none')
        self.style.configure('Danger.TButton', background='#e74c3c', foreground='white', font=("Segoe UI", 10, "bold"), focuscolor='none')
        self.style.configure('Header.TFrame', background='#2c3e50')
        self.style.configure('Header.TLabel', background='#2c3e50', foreground='white', font=("Segoe UI", 20, "bold"))
        self.style.configure('Card.TFrame', background='white')
        
        # Data storage - user-specific
        self.projects = []
        self.current_project = None
        self.data_file = f"projects_{username}.json"  # User-specific projects file
        self.media_folder = f"project_media_{username}"  # User-specific media folder
        
        # Store widget references for theme switching
        self.theme_labels = []
        self.theme_frames = []
        self.theme_entries = []
        self.theme_text_widgets = []
        self.theme_canvases = []
        self.info_tab_frames = []  # Special tracking for info tab frames
        
        # Create media folder if it doesn't exist
        if not os.path.exists(self.media_folder):
            os.makedirs(self.media_folder)
        
        # Load existing data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ttk.Frame(self.root, style='Header.TFrame', height=60)
        header.pack(fill=tk.X)
        
        title_label = ttk.Label(header, text=f"🎬 Asset Alley - Welcome {self.username}!", style='Header.TLabel')
        title_label.pack(pady=15)
        
        # theme toggle
        self.dark_mode = False
        theme_btn = ttk.Button(header, text="🌙", width=3, command=self.toggle_theme, style='Accent.TButton')
        theme_btn.place(relx=0.90, rely=0.5, anchor='e')
        
        # Logout button
        logout_btn = ttk.Button(header, text="🚪 Logout", width=10, command=self.logout, style='Danger.TButton')
        logout_btn.place(relx=0.98, rely=0.5, anchor='e')
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Project List
        left_panel = tk.Frame(main_container, bg="white", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Project list header
        list_header = tk.Frame(left_panel, bg="#34495e")
        list_header.pack(fill=tk.X)
        
        tk.Label(list_header, text="Projects", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="white").pack(pady=10)
        
        # Add project button
        add_btn = ttk.Button(left_panel, text="+ New Project", 
                             command=self.add_project,
                             style='Success.TButton',
                             cursor="hand2")
        add_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Search bar
        tk.Label(left_panel, text="Search projects:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor=tk.W, padx=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(left_panel, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, padx=10, pady=(0,10))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_project_list())
        
        # Projects treeview instead of listbox
        tree_frame = tk.Frame(left_panel, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.projects_tree = ttk.Treeview(tree_frame, columns=('name','status'), show='headings', selectmode='browse')
        self.projects_tree.heading('name', text='Project')
        self.projects_tree.heading('status', text='Status')
        self.projects_tree.column('name', anchor='w')
        self.projects_tree.column('status', width=80, anchor='center')
        self.projects_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.projects_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.projects_tree.configure(yscrollcommand=scrollbar.set)
        
        self.projects_tree.bind('<<TreeviewSelect>>', self.on_project_select)
        
        # Right panel - Project Details
        right_panel = tk.Frame(main_container, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Project Info
        self.info_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.info_tab, text="📋 Info")
        self.setup_info_tab()
        
        # Tab 2: Tasks
        self.tasks_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tasks_tab, text="✅ Tasks")
        self.setup_tasks_tab()
        
        # Tab 3: Media
        self.media_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.media_tab, text="🎨 Media")
        self.setup_media_tab()
        
        # Tab 4: Notes
        self.notes_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.notes_tab, text="📝 Notes")
        self.setup_notes_tab()
        
        # Tab 5: Students Contact
        self.students_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.students_tab, text="👥 Students Contact")
        self.setup_students_tab()
        
        # Refresh project list
        self.refresh_project_list()
        
    def setup_info_tab(self):
        # Create a scrollable content frame
        content_frame = tk.Frame(self.info_tab, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.theme_frames.append(content_frame)
        self.info_tab_frames.append(content_frame)
        
        # Scrollable canvas
        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        self.theme_frames.append(scrollable_frame)
        self.info_tab_frames.append(scrollable_frame)
        self.theme_canvases.append(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Project name
        name_label = tk.Label(scrollable_frame, text="Project Name:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        name_label.pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.theme_labels.append(name_label)
        
        self.project_name_var = tk.StringVar()
        name_entry = tk.Entry(scrollable_frame, textvariable=self.project_name_var, 
                font=("Arial", 12), relief=tk.FLAT, bg="#ecf0f1", fg="black")
        name_entry.pack(fill=tk.X, padx=20, pady=(0, 15), ipady=5)
        self.theme_entries.append(name_entry)
        
        # Description
        desc_label = tk.Label(scrollable_frame, text="Description:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        desc_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.theme_labels.append(desc_label)
        
        card_bg = '#f0f0f0'
        self.description_text = scrolledtext.ScrolledText(scrollable_frame, 
                                                         height=4, font=("Arial", 10),
                                                         relief=tk.FLAT, bg=card_bg, fg="black")
        self.description_text.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.theme_text_widgets.append(self.description_text)
        
        # Status
        status_label = tk.Label(scrollable_frame, text="Status:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        status_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.theme_labels.append(status_label)
        
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(scrollable_frame, textvariable=self.status_var,
                                   values=["Planning", "In Progress", "On Hold", "Completed"],
                                   state="readonly", font=("Arial", 10))
        status_combo.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Priority
        priority_label = tk.Label(scrollable_frame, text="Priority:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        priority_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.theme_labels.append(priority_label)
        
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(scrollable_frame, textvariable=self.priority_var,
                                     values=["Low", "Medium", "High", "Critical"],
                                     state="readonly", font=("Arial", 10))
        priority_combo.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Progress Section
        progress_label_title = tk.Label(scrollable_frame, text="Project Progress:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        progress_label_title.pack(anchor=tk.W, padx=20, pady=(10, 8))
        self.theme_labels.append(progress_label_title)
        
        # Progress percentage label
        self.progress_label = tk.Label(scrollable_frame, text="Progress: 0%", 
                font=("Arial", 10), bg="white", fg="#3498db")
        self.progress_label.pack(anchor=tk.W, padx=20, pady=(0, 5))
        self.theme_labels.append(self.progress_label)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(scrollable_frame, mode='determinate', 
                value=0, length=250)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Languages Section
        languages_label_title = tk.Label(scrollable_frame, text="Technologies Used:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        languages_label_title.pack(anchor=tk.W, padx=20, pady=(20, 8))
        self.theme_labels.append(languages_label_title)
        
        # Frontend Language
        frontend_label = tk.Label(scrollable_frame, text="Frontend Language:", font=("Arial", 10, "bold"),
                bg="white", fg="black")
        frontend_label.pack(anchor=tk.W, padx=20, pady=(5, 5))
        self.theme_labels.append(frontend_label)
        
        self.frontend_var = tk.StringVar()
        frontend_options = [
            "HTML/CSS/JavaScript", "React", "Vue.js", "Angular", "Svelte",
            "Bootstrap", "Tailwind CSS", "Webpack", "Babel", "TypeScript"
        ]
        frontend_combo = ttk.Combobox(scrollable_frame, textvariable=self.frontend_var,
                                     values=frontend_options, state="readonly", font=("Arial", 10))
        frontend_combo.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.frontend_var.set("HTML/CSS/JavaScript")
        
        # Backend Language
        backend_label = tk.Label(scrollable_frame, text="Backend Language:", font=("Arial", 10, "bold"),
                bg="white", fg="black")
        backend_label.pack(anchor=tk.W, padx=20, pady=(5, 5))
        self.theme_labels.append(backend_label)
        
        self.backend_var = tk.StringVar()
        backend_options = [
            "Python", "Node.js", "Java", "C#", "PHP", "Ruby", "Go", "Rust",
            "Django", "Flask", "Express.js", "Spring", "ASP.NET", "Laravel"
        ]
        backend_combo = ttk.Combobox(scrollable_frame, textvariable=self.backend_var,
                                    values=backend_options, state="readonly", font=("Arial", 10))
        backend_combo.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.backend_var.set("Python")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame at bottom (stays fixed)
        button_frame = tk.Frame(self.info_tab, bg="white")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=20)
        self.theme_frames.append(button_frame)
        self.info_tab_frames.append(button_frame)
        
        # Buttons frame with Save and Statistics
        buttons_row = tk.Frame(button_frame, bg="white")
        buttons_row.pack(fill=tk.X)
        self.theme_frames.append(buttons_row)
        
        # Save button
        save_btn = ttk.Button(buttons_row, text="💾 Save Project Info",
                                command=self.save_project_info,
                                style='Accent.TButton')
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Statistics button
        stats_btn = ttk.Button(buttons_row, text="📊 Statistics",
                                command=self.show_statistics,
                                style='Accent.TButton')
        stats_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def setup_tasks_tab(self):
        # Task input frame
        input_frame = tk.Frame(self.tasks_tab, bg="white")
        input_frame.pack(fill=tk.X, padx=20, pady=20)
        self.theme_frames.append(input_frame)
        
        task_label = tk.Label(input_frame, text="New Task:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        task_label.pack(anchor=tk.W)
        self.theme_labels.append(task_label)
        
        task_entry_frame = tk.Frame(input_frame, bg="white")
        task_entry_frame.pack(fill=tk.X, pady=(5, 10))
        self.theme_frames.append(task_entry_frame)
        
        self.task_entry = tk.Entry(task_entry_frame, font=("Arial", 11),
                                   relief=tk.FLAT, bg="#ecf0f1", fg="black")
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.theme_entries.append(self.task_entry)
        
        add_task_btn = ttk.Button(task_entry_frame, text="Add", 
                                   command=self.add_task,
                                   style='Success.TButton')
        add_task_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Tasks list frame
        tasks_list_frame = tk.Frame(self.tasks_tab, bg="#ecf0f1")
        tasks_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.theme_frames.append(tasks_list_frame)
        
        # Scrollable canvas for tasks
        canvas = tk.Canvas(tasks_list_frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(tasks_list_frame, orient="vertical", command=canvas.yview)
        self.tasks_frame = tk.Frame(canvas, bg="#ecf0f1")
        self.theme_canvases.append(canvas)
        self.theme_frames.append(self.tasks_frame)
        
        self.tasks_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_media_tab(self):
        # Buttons frame
        buttons_frame = tk.Frame(self.media_tab, bg="white")
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        self.theme_frames.append(buttons_frame)
        
        ttk.Button(buttons_frame, text="📷 Add Image", 
                   command=self.add_image,
                   style='Danger.TButton').pack(
                   side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="🎵 Add Audio", 
                   command=self.add_audio,
                   style='Accent.TButton').pack(
                   side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="📄 Add Document", 
                   command=self.add_document,
                   style='Accent.TButton').pack(
                   side=tk.LEFT)
        
        # Media list frame
        media_list_frame = tk.Frame(self.media_tab, bg="#ecf0f1")
        media_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.theme_frames.append(media_list_frame)
        
        # Scrollable canvas for media
        canvas = tk.Canvas(media_list_frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(media_list_frame, orient="vertical", command=canvas.yview)
        self.media_frame = tk.Frame(canvas, bg="#ecf0f1")
        self.theme_canvases.append(canvas)
        self.theme_frames.append(self.media_frame)
        
        self.media_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.media_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_notes_tab(self):
        # Button frame at top (stays fixed)
        button_frame = tk.Frame(self.notes_tab, bg="white")
        button_frame.pack(fill=tk.X, side=tk.TOP, padx=20, pady=(20, 10))
        self.theme_frames.append(button_frame)
        
        notes_label = tk.Label(button_frame, text="Project Notes:", font=("Arial", 11, "bold"),
                bg="white", fg="black")
        notes_label.pack(anchor=tk.W)
        self.theme_labels.append(notes_label)
        
        # Content frame with limited height
        content_frame = tk.Frame(self.notes_tab, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        self.theme_frames.append(content_frame)
        
        card_bg = '#f0f0f0'
        self.notes_text = scrolledtext.ScrolledText(content_frame, 
                                                   height=12,
                                                   font=("Arial", 11),
                                                   relief=tk.FLAT, bg=card_bg, fg="black",
                                                   wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=False, padx=0, pady=0)
        self.theme_text_widgets.append(self.notes_text)
        
        # Save button frame at bottom
        save_frame = tk.Frame(self.notes_tab, bg="white")
        save_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(10, 20))
        self.theme_frames.append(save_frame)
        
        save_notes_btn = ttk.Button(save_frame, text="💾 Save Notes",
                                     command=self.save_notes,
                                     style='Accent.TButton')
        save_notes_btn.pack(fill=tk.X)
        
    def setup_students_tab(self):
        # Header frame
        header_frame = tk.Frame(self.students_tab, bg="white")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        self.theme_frames.append(header_frame)
        
        header_label = tk.Label(header_frame, text="Project Students Contact Management", 
                               font=("Arial", 12, "bold"), bg="white", fg="black")
        header_label.pack(anchor=tk.W)
        self.theme_labels.append(header_label)
        
        # Add student frame
        add_student_frame = tk.Frame(self.students_tab, bg="white")
        add_student_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        self.theme_frames.append(add_student_frame)
        
        # Student name
        tk.Label(add_student_frame, text="Student Name:", font=("Arial", 10, "bold"),
                bg="white", fg="black").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.student_name_entry = tk.Entry(add_student_frame, font=("Arial", 10),
                                           relief=tk.FLAT, bg="#ecf0f1", fg="black")
        self.student_name_entry.grid(row=0, column=1, sticky=tk.EW, padx=(5, 10))
        self.theme_entries.append(self.student_name_entry)
        
        # Student email
        tk.Label(add_student_frame, text="Email:", font=("Arial", 10, "bold"),
                bg="white", fg="black").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.student_email_entry = tk.Entry(add_student_frame, font=("Arial", 10),
                                            relief=tk.FLAT, bg="#ecf0f1", fg="black")
        self.student_email_entry.grid(row=1, column=1, sticky=tk.EW, padx=(5, 10))
        self.theme_entries.append(self.student_email_entry)
        
        # Student phone
        tk.Label(add_student_frame, text="Phone:", font=("Arial", 10, "bold"),
                bg="white", fg="black").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.student_phone_entry = tk.Entry(add_student_frame, font=("Arial", 10),
                                            relief=tk.FLAT, bg="#ecf0f1", fg="black")
        self.student_phone_entry.grid(row=2, column=1, sticky=tk.EW, padx=(5, 10))
        self.theme_entries.append(self.student_phone_entry)
        
        # Add button
        add_btn = ttk.Button(add_student_frame, text="➕ Add Student",
                             command=self.add_student,
                             style='Success.TButton')
        add_btn.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(10, 0))
        
        add_student_frame.columnconfigure(1, weight=1)
        
        # Students list frame
        list_frame = tk.Frame(self.students_tab, bg="#ecf0f1")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.theme_frames.append(list_frame)
        
        # Scrollable canvas for students
        canvas = tk.Canvas(list_frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.students_frame = tk.Frame(canvas, bg="#ecf0f1")
        self.theme_canvases.append(canvas)
        self.theme_frames.append(self.students_frame)
        
        self.students_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.students_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def add_student(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
        
        name = self.student_name_entry.get().strip()
        email = self.student_email_entry.get().strip()
        phone = self.student_phone_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter student name!")
            return
        
        if not email and not phone:
            messagebox.showwarning("Warning", "Please enter email or phone number!")
            return
        
        student = {
            "id": len(self.current_project.get("students", [])) + 1,
            "name": name,
            "email": email,
            "phone": phone,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if "students" not in self.current_project:
            self.current_project["students"] = []
        
        self.current_project["students"].append(student)
        self.save_data()
        
        # Clear entries
        self.student_name_entry.delete(0, tk.END)
        self.student_email_entry.delete(0, tk.END)
        self.student_phone_entry.delete(0, tk.END)
        
        self.refresh_students()
        messagebox.showinfo("Success", f"Student '{name}' added!")
        
    def refresh_students(self):
        # Clear existing student widgets
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        
        if not self.current_project or not self.current_project.get("students"):
            no_students_label = tk.Label(self.students_frame, text="No students added yet",
                                        font=("Arial", 10), bg="#ecf0f1", fg="#7f8c8d")
            no_students_label.pack(pady=20)
            return
        
        for student in self.current_project["students"]:
            student_card = tk.Frame(self.students_frame, bg="white", relief=tk.RAISED, 
                                   bd=1)
            student_card.pack(fill=tk.X, pady=5, padx=5)
            self.theme_frames.append(student_card)
            
            # Student info
            info_frame = tk.Frame(student_card, bg="white")
            info_frame.pack(fill=tk.X, padx=10, pady=10)
            self.theme_frames.append(info_frame)
            
            # Name
            name_label = tk.Label(info_frame, text=f"📌 {student['name']}", 
                                 font=("Arial", 11, "bold"), bg="white", fg="black", 
                                 justify=tk.LEFT)
            name_label.pack(anchor=tk.W, pady=(0, 5))
            self.theme_labels.append(name_label)
            
            # Email and Phone
            contact_info = f"📧 {student['email']}" if student.get('email') else ""
            if student.get('phone'):
                if contact_info:
                    contact_info += f"  |  ☎️ {student['phone']}"
                else:
                    contact_info = f"☎️ {student['phone']}"
            
            contact_label = tk.Label(info_frame, text=contact_info,
                                    font=("Arial", 9), bg="white", fg="#34495e")
            contact_label.pack(anchor=tk.W, pady=(0, 10))
            self.theme_labels.append(contact_label)
            
            # Buttons frame
            buttons_frame = tk.Frame(student_card, bg="white")
            buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            self.theme_frames.append(buttons_frame)
            
            # Contact via email button
            if student.get('email'):
                email_btn = ttk.Button(buttons_frame, text="✉️ Send Email",
                                       command=lambda e=student['email'], n=student['name']: 
                                       self.contact_via_email(e, n),
                                       style='Accent.TButton')
                email_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Show phone button
            if student.get('phone'):
                phone_btn = ttk.Button(buttons_frame, text="☎️ Call",
                                       command=lambda p=student['phone'], n=student['name']: 
                                       self.show_phone_dialog(p, n),
                                       style='Accent.TButton')
                phone_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Delete button
            delete_btn = ttk.Button(buttons_frame, text="🗑️ Remove",
                                    command=lambda s_id=student['id']: self.remove_student(s_id),
                                    style='Danger.TButton')
            delete_btn.pack(side=tk.LEFT)
    
    def contact_via_email(self, email, name):
        """Open default email client to send email to student"""
        try:
            email_subject = f"Project Communication - {self.current_project['name']}"
            email_body = f"Hello {name},\n\nThis is regarding the project: {self.current_project['name']}\n\n"
            
            # URL encode the subject and body
            import urllib.parse
            subject_encoded = urllib.parse.quote(email_subject)
            body_encoded = urllib.parse.quote(email_body)
            
            mailto_link = f"mailto:{email}?subject={subject_encoded}&body={body_encoded}"
            
            webbrowser.open(mailto_link)
            messagebox.showinfo("Success", f"Opening email client to send email to {name}...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open email client: {str(e)}")
    
    def show_phone_dialog(self, phone, name):
        """Show a dialog with the phone number for copying"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Contact {name}")
        dialog.geometry("500x250")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f0f0")
        
        # Header
        header = tk.Label(dialog, text=f"📞 Call {name}", font=("Arial", 14, "bold"),
                         bg="white", fg="black")
        header.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        # Phone number with copy button
        phone_frame = tk.Frame(dialog, bg="white")
        phone_frame.pack(fill=tk.X, padx=20, pady=(5, 20), expand=True)
        
        phone_label = tk.Label(phone_frame, text="Phone Number:", font=("Arial", 11, "bold"),
                              bg="white", fg="black")
        phone_label.pack(anchor=tk.W, pady=(0, 10))
        
        phone_text = tk.Entry(phone_frame, font=("Arial", 13), relief=tk.FLAT,
                             bg="#ecf0f1", fg="black", justify=tk.CENTER)
        phone_text.insert(0, phone)
        phone_text.config(state=tk.DISABLED)
        phone_text.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Copy button
        def copy_phone():
            self.root.clipboard_clear()
            self.root.clipboard_append(phone)
            messagebox.showinfo("Success", "Phone number copied!")
        
        copy_btn = ttk.Button(phone_frame, text="📋 Copy Phone Number", command=copy_phone,
                             style='Success.TButton')
        copy_btn.pack(fill=tk.X, pady=(0, 10), ipady=8)
    
    def remove_student(self, student_id):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
        
        if messagebox.askyesno("Confirm", "Remove this student?"):
            self.current_project["students"] = [s for s in self.current_project.get("students", [])
                                               if s["id"] != student_id]
            self.save_data()
            self.refresh_students()
            messagebox.showinfo("Success", "Student removed!")
        
    def add_project(self):
        name = tk.simpledialog.askstring("New Project", "Enter project name:")
        if name:
            project = {
                "id": len(self.projects) + 1,
                "name": name,
                "description": "",
                "status": "Planning",
                "priority": "Medium",
                "tasks": [],
                "media": [],
                "notes": "",
                "students": [],
                "progress": 0,
                "frontend_language": "HTML/CSS/JavaScript",
                "backend_language": "Python",
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.projects.append(project)
            self.save_data()
            self.refresh_project_list()
            messagebox.showinfo("Success", f"Project '{name}' created!")
            
    def on_project_select(self, event):
        # treeview selection
        sel = event.widget.selection()
        if sel:
            item = sel[0]
            index = int(self.projects_tree.index(item))
            self.current_project = self.filtered_projects[index]
            self.load_project_details()
            
    def load_project_details(self):
        if not self.current_project:
            return
            
        # Load info
        self.project_name_var.set(self.current_project["name"])
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, self.current_project["description"])
        self.status_var.set(self.current_project["status"])
        self.priority_var.set(self.current_project["priority"])
        
        # Load languages
        self.frontend_var.set(self.current_project.get("frontend_language", "HTML/CSS/JavaScript"))
        self.backend_var.set(self.current_project.get("backend_language", "Python"))
        
        # Refresh tasks
        self.refresh_tasks()
        # Refresh media
        self.refresh_media()
        # Refresh students
        self.refresh_students()
        
        # Calculate and display progress
        self.update_project_progress()
        
        # Load tasks
        self.refresh_tasks()
        
        # Load media
        self.refresh_media()
        
        # Load notes
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(1.0, self.current_project["notes"])
        
    def save_project_info(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
            
        self.current_project["name"] = self.project_name_var.get()
        self.current_project["description"] = self.description_text.get(1.0, tk.END).strip()
        self.current_project["status"] = self.status_var.get()
        self.current_project["priority"] = self.priority_var.get()
        self.current_project["frontend_language"] = self.frontend_var.get()
        self.current_project["backend_language"] = self.backend_var.get()
        
        self.save_data()
        self.refresh_project_list()
        messagebox.showinfo("Success", "Project information saved!")
        
    def add_task(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
            
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.current_project["tasks"]) + 1,
                "text": task_text,
                "completed": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.current_project["tasks"].append(task)
            self.task_entry.delete(0, tk.END)
            self.update_project_progress()
            self.save_data()
            self.refresh_tasks()
            self.refresh_project_list()
            
    def toggle_task(self, task_id):
        if not self.current_project:
            return
            
        for task in self.current_project["tasks"]:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
                
        self.update_project_progress()
        self.save_data()
        self.refresh_tasks()
        self.refresh_project_list()
        
    def delete_task(self, task_id):
        if not self.current_project:
            return
            
        self.current_project["tasks"] = [t for t in self.current_project["tasks"] 
                                        if t["id"] != task_id]
        self.update_project_progress()
        self.save_data()
        self.refresh_tasks()
        self.refresh_project_list()
        
    def refresh_tasks(self):
        # Clear existing task widgets
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
            
        if not self.current_project:
            return
            
        for task in self.current_project["tasks"]:
            task_frame = ttk.Frame(self.tasks_frame, style='Card.TFrame', relief=tk.RAISED)
            task_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Checkbox
            var = tk.IntVar(value=1 if task["completed"] else 0)
            check = tk.Checkbutton(task_frame, variable=var,
                                  command=lambda t=task["id"]: self.toggle_task(t),
                                  bg="white")
            check.pack(side=tk.LEFT, padx=5)
            
            # Task text
            text_style = ("Arial", 10, "overstrike") if task["completed"] else ("Arial", 10)
            tk.Label(task_frame, text=task["text"], font=text_style,
                    bg="white", anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, 
                                                  expand=True, padx=5, pady=5)
            
            # Delete button
            ttk.Button(task_frame, text="🗑", 
                       command=lambda t=task["id"]: self.delete_task(t),
                       style='Danger.TButton').pack(side=tk.RIGHT, padx=5)
            
    def add_image(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
            
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if filename:
            # Copy file to media folder
            dest_folder = os.path.join(self.media_folder, f"project_{self.current_project['id']}")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            dest_path = os.path.join(dest_folder, os.path.basename(filename))
            shutil.copy2(filename, dest_path)
            
            media = {
                "id": len(self.current_project["media"]) + 1,
                "type": "image",
                "name": os.path.basename(filename),
                "path": dest_path,
                "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.current_project["media"].append(media)
            self.save_data()
            self.refresh_media()
            messagebox.showinfo("Success", "Image added!")
            
    def add_audio(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
            
        filename = filedialog.askopenfilename(
            title="Select Audio",
            filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.m4a"), ("All files", "*.*")]
        )
        
        if filename:
            dest_folder = os.path.join(self.media_folder, f"project_{self.current_project['id']}")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            dest_path = os.path.join(dest_folder, os.path.basename(filename))
            shutil.copy2(filename, dest_path)
            
            media = {
                "id": len(self.current_project["media"]) + 1,
                "type": "audio",
                "name": os.path.basename(filename),
                "path": dest_path,
                "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.current_project["media"].append(media)
            self.save_data()
            self.refresh_media()
            messagebox.showinfo("Success", "Audio added!")
            
    def add_document(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
            
        filename = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("Documents", "*.pdf *.doc *.docx *.txt"), ("All files", "*.*")]
        )
        
        if filename:
            dest_folder = os.path.join(self.media_folder, f"project_{self.current_project['id']}")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            dest_path = os.path.join(dest_folder, os.path.basename(filename))
            shutil.copy2(filename, dest_path)
            
            media = {
                "id": len(self.current_project["media"]) + 1,
                "type": "document",
                "name": os.path.basename(filename),
                "path": dest_path,
                "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.current_project["media"].append(media)
            self.save_data()
            self.refresh_media()
            messagebox.showinfo("Success", "Document added!")
            
    def delete_media(self, media_id):
        if not self.current_project:
            return
            
        media_item = next((m for m in self.current_project["media"] if m["id"] == media_id), None)
        if media_item and os.path.exists(media_item["path"]):
            os.remove(media_item["path"])
            
        self.current_project["media"] = [m for m in self.current_project["media"] 
                                        if m["id"] != media_id]
        self.save_data()
        self.refresh_media()
        
    def open_media(self, path):
        if os.path.exists(path):
            os.startfile(path) if os.name == 'nt' else os.system(f'open "{path}"')
            
    def refresh_media(self):
        # Clear existing media widgets
        for widget in self.media_frame.winfo_children():
            widget.destroy()
            
        if not self.current_project:
            return
            
        for media in self.current_project["media"]:
            media_frame = ttk.Frame(self.media_frame, style='Card.TFrame', relief=tk.RAISED)
            media_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Icon based on type
            icon = "📷" if media["type"] == "image" else "🎵" if media["type"] == "audio" else "📄"
            
            tk.Label(media_frame, text=icon, font=("Arial", 16),
                    bg="white").pack(side=tk.LEFT, padx=10, pady=5)
            
            # Media name
            tk.Label(media_frame, text=media["name"], font=("Arial", 10),
                    bg="white", anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, 
                                                expand=True, padx=5, pady=5)

            # Open button
            ttk.Button(media_frame, text="Open",
                    command=lambda p=media["path"]: self.open_media(p),
                    style='Accent.TButton').pack(side=tk.RIGHT, padx=(5, 5))

            # Delete button
            ttk.Button(media_frame, text="🗑",
                    command=lambda m=media["id"]: self.delete_media(m),
                    style='Danger.TButton').pack(side=tk.RIGHT, padx=5)

    def save_notes(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "No project selected!")
            return

        self.current_project["notes"] = self.notes_text.get(1.0, tk.END).strip()
        self.save_data()
        messagebox.showinfo("Success", "Notes saved!")

    def update_project_progress(self):
        """Calculate progress percentage based on completed tasks"""
        if not self.current_project:
            return
        
        tasks = self.current_project['tasks']
        if not tasks:
            self.current_project['progress'] = 0
            return
        
        completed = sum(1 for task in tasks if task['completed'])
        progress = int((completed / len(tasks)) * 100)
        self.current_project['progress'] = progress
        
        # Update progress label if it exists
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=f"Progress: {progress}%")
        
        # Update progress bar if it exists
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = progress
    
    def refresh_project_list(self):
        # filter based on search
        query = self.search_var.get().lower() if hasattr(self, 'search_var') else ''
        self.filtered_projects = []
        for proj in self.projects:
            if query in proj['name'].lower():
                self.filtered_projects.append(proj)
        
        # rebuild tree
        for i in self.projects_tree.get_children():
            self.projects_tree.delete(i)
        for proj in self.filtered_projects:
            status = proj['status']
            progress = proj.get('progress', 0)
            # Show name with progress percentage
            display_name = f"{proj['name']} ({progress}%)"
            self.projects_tree.insert('', tk.END, values=(display_name, status))

    def toggle_theme(self):
        """Switch between light and dark mode by updating style colors and widget colors."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            bg = '#2c3e50'
            fg = 'white'
            card = '#34495e'
            label_bg = '#34495e'
            label_fg = 'white'
            text_bg = '#3f5568'
            text_fg = 'white'
            entry_bg = '#3f5568'
            entry_fg = 'white'
            light_bg = '#3f5568'
        else:
            bg = '#f0f0f0'
            fg = 'black'
            card = 'white'
            label_bg = 'white'
            label_fg = 'black'
            text_bg = '#f0f0f0'
            text_fg = 'black'
            entry_bg = '#ecf0f1'
            entry_fg = 'black'
            light_bg = '#ecf0f1'
        
        # Update root and main containers
        self.root.configure(bg=bg)
        self.style.configure('Header.TFrame', background=bg)
        self.style.configure('Header.TLabel', background=bg, foreground=fg)
        self.style.configure('Card.TFrame', background=card)
        
        # Update button styles with all states
        if self.dark_mode:
            self.style.configure('Accent.TButton', background='#2980b9', foreground='white')
            self.style.map('Accent.TButton', background=[('active', '#1f618d')])
            self.style.configure('Success.TButton', background='#229954', foreground='white')
            self.style.map('Success.TButton', background=[('active', '#1a7a3d')])
            self.style.configure('Danger.TButton', background='#c0392b', foreground='white')
            self.style.map('Danger.TButton', background=[('active', '#a93226')])
        else:
            self.style.configure('Accent.TButton', background='#3498db', foreground='white')
            self.style.map('Accent.TButton', background=[('active', '#2980b9')])
            self.style.configure('Success.TButton', background='#27ae60', foreground='white')
            self.style.map('Success.TButton', background=[('active', '#229954')])
            self.style.configure('Danger.TButton', background='#e74c3c', foreground='white')
            self.style.map('Danger.TButton', background=[('active', '#c0392b')])
        
        # Update all labels
        for label in self.theme_labels:
            label.configure(bg=label_bg, fg=label_fg)
        
        # Special handling for progress label - use a visible color for dark mode
        if hasattr(self, 'progress_label'):
            if self.dark_mode:
                self.progress_label.configure(bg=label_bg, fg='#5dade2')  # Light blue for dark mode
            else:
                self.progress_label.configure(bg=label_bg, fg='#3498db')  # Original blue for light mode
        
        # Update all frames
        for frame in self.theme_frames:
            try:
                if frame in [self.info_tab, self.tasks_tab, self.media_tab, self.notes_tab]:
                    frame.configure(bg=card)
                # Special handling for info_tab internal frames
                elif hasattr(self, 'info_tab_frames') and frame in self.info_tab_frames:
                    frame.configure(bg=card)
                else:
                    # Regular frame - update to match light/dark backgrounds
                    try:
                        current_bg = frame.cget('bg')
                        # Check if it's a white/light background
                        if current_bg in ('white', '#ffffff', 'white smoke', 'snow'):
                            frame.configure(bg=label_bg)
                        # Check if it's a grey/light background
                        elif current_bg in ('#ecf0f1', '#f0f0f0', '#f5f5f5'):
                            frame.configure(bg=light_bg)
                        else:
                            # Default - update to card background
                            frame.configure(bg=card)
                    except:
                        # Try with label_bg if error occurs
                        try:
                            frame.configure(bg=label_bg)
                        except:
                            pass
            except:
                pass
        
        # Update all entry fields
        for entry in self.theme_entries:
            entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        
        # Update all text widgets
        for text_widget in self.theme_text_widgets:
            text_widget.configure(bg=text_bg, fg=text_fg, insertbackground=text_fg)
        
        # Update all canvases
        for canvas in self.theme_canvases:
            try:
                current_bg = canvas.cget('bg')
                if current_bg in ('#ecf0f1', '#f0f0f0', '#f5f5f5'):
                    canvas.configure(bg=light_bg)
                elif current_bg in ('white', '#ffffff'):
                    canvas.configure(bg=label_bg)
            except:
                pass
            
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.projects, f, indent=2)
            
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.projects = json.load(f)
            except:
                self.projects = []
    
    def calculate_statistics(self):
        """Calculate all project statistics"""
        stats = {
            'total_projects': len(self.projects),
            'total_students': 1,  # Current user
            'frontend_languages': {},
            'backend_languages': {},
            'all_languages': {},
            'status_distribution': {},
            'priority_distribution': {},
            'progress_data': [],
            'projects_by_status': {}
        }
        
        # Process each project
        for project in self.projects:
            # Frontend Languages
            frontend = project.get('frontend_language', 'Unknown')
            stats['frontend_languages'][frontend] = stats['frontend_languages'].get(frontend, 0) + 1
            stats['all_languages'][frontend] = stats['all_languages'].get(frontend, 0) + 1
            
            # Backend Languages
            backend = project.get('backend_language', 'Unknown')
            stats['backend_languages'][backend] = stats['backend_languages'].get(backend, 0) + 1
            stats['all_languages'][backend] = stats['all_languages'].get(backend, 0) + 1
            
            # Status Distribution
            status = project.get('status', 'Unknown')
            stats['status_distribution'][status] = stats['status_distribution'].get(status, 0) + 1
            stats['projects_by_status'][status] = stats['projects_by_status'].get(status, []) + [project['name']]
            
            # Priority Distribution
            priority = project.get('priority', 'Unknown')
            stats['priority_distribution'][priority] = stats['priority_distribution'].get(priority, 0) + 1
            
            # Progress Data
            stats['progress_data'].append({
                'name': project['name'],
                'progress': project.get('progress', 0)
            })
        
        # Calculate average completion
        avg_completion = 0
        if stats['progress_data']:
            avg_completion = round(
                sum(p['progress'] for p in stats['progress_data']) / len(stats['progress_data'])
            )
        
        stats['avg_completion'] = avg_completion
        stats['total_languages'] = len(stats['all_languages'])
        
        return stats
    
    def show_statistics(self):
        """Show statistics in web browser"""
        try:
            stats = self.calculate_statistics()
            
            # Create HTML content
            html_content = self.generate_statistics_html(stats)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            
            # Open in default browser
            webbrowser.open('file://' + temp_file.name)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show statistics: {str(e)}")
    
    def generate_statistics_html(self, stats):
        """Generate HTML for statistics dashboard"""
        
        # Helper function to get colors
        colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#16a085', '#2c3e50', '#34495e', '#1abc9c', '#e67e22']
        
        # Create labels and data for frontend languages
        frontend_labels = list(stats['frontend_languages'].keys())
        frontend_data = list(stats['frontend_languages'].values())
        frontend_colors = colors[:len(frontend_labels)]
        
        # Create labels and data for backend languages
        backend_labels = list(stats['backend_languages'].keys())
        backend_data = list(stats['backend_languages'].values())
        backend_colors = colors[:len(backend_labels)]
        
        # Create labels and data for status
        status_labels = list(stats['status_distribution'].keys())
        status_data = list(stats['status_distribution'].values())
        status_colors = {
            'Planning': '#95a5a6',
            'In Progress': '#f39c12',
            'Completed': '#27ae60',
            'On Hold': '#e67e22'
        }
        status_chart_colors = [status_colors.get(label, '#3498db') for label in status_labels]
        
        # Create labels and data for priority
        priority_labels = list(stats['priority_distribution'].keys())
        priority_data = list(stats['priority_distribution'].values())
        
        # Create labels and data for progress
        progress_labels = [p['name'] for p in stats['progress_data']]
        progress_values = [p['progress'] for p in stats['progress_data']]
        
        # Create labels and data for all languages
        lang_labels = list(stats['all_languages'].keys())
        lang_data = list(stats['all_languages'].values())
        lang_colors = colors[:len(lang_labels)]
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Statistics - {self.username}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        header h1 {{
            font-size: 32px;
            margin-bottom: 5px;
        }}
        
        header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            text-align: center;
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            color: #2c3e50;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .stat-card p {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }}
        
        .chart-card h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            margin-bottom: 20px;
        }}
        
        .project-list {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            margin-top: 30px;
        }}
        
        .project-list h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .project-item {{
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            border-radius: 5px;
        }}
        
        .project-item strong {{
            color: #2c3e50;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .badge-planning {{
            background: #95a5a6;
            color: white;
        }}
        
        .badge-in-progress {{
            background: #f39c12;
            color: white;
        }}
        
        .badge-completed {{
            background: #27ae60;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Project Statistics & Analytics</h1>
            <p>User: {self.username}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>{stats['total_projects']}</h3>
                <p>Total Projects</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_students']}</h3>
                <p>Active Student(s)</p>
            </div>
            <div class="stat-card">
                <h3>{stats['total_languages']}</h3>
                <p>Languages Used</p>
            </div>
            <div class="stat-card">
                <h3>{stats['avg_completion']}%</h3>
                <p>Avg. Completion</p>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <h3>Frontend Languages Distribution</h3>
                <div class="chart-container">
                    <canvas id="frontendChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>Backend Languages Distribution</h3>
                <div class="chart-container">
                    <canvas id="backendChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>Project Status Overview</h3>
                <div class="chart-container">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>Project Priority Distribution</h3>
                <div class="chart-container">
                    <canvas id="priorityChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card" style="grid-column: 1 / -1;">
                <h3>Projects Progress</h3>
                <div class="chart-container" style="height: 400px;">
                    <canvas id="progressChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card" style="grid-column: 1 / -1;">
                <h3>All Languages Used (Combined)</h3>
                <div class="chart-container" style="height: 400px;">
                    <canvas id="languageChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="project-list">
            <h3>📋 Projects Overview</h3>
            <div id="projectsList"></div>
        </div>
    </div>
    
    <script>
        const chartColors = {json.dumps(colors)};
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: true,
                    position: 'bottom'
                }}
            }}
        }};
        
        // Frontend Chart
        const frontendCtx = document.getElementById('frontendChart').getContext('2d');
        new Chart(frontendCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(frontend_labels)},
                datasets: [{{
                    data: {json.dumps(frontend_data)},
                    backgroundColor: {json.dumps(frontend_colors)},
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: chartOptions
        }});
        
        // Backend Chart
        const backendCtx = document.getElementById('backendChart').getContext('2d');
        new Chart(backendCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(backend_labels)},
                datasets: [{{
                    data: {json.dumps(backend_data)},
                    backgroundColor: {json.dumps(backend_colors)},
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: chartOptions
        }});
        
        // Status Chart
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(status_labels)},
                datasets: [{{
                    data: {json.dumps(status_data)},
                    backgroundColor: {json.dumps(status_chart_colors)},
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: chartOptions
        }});
        
        // Priority Chart
        const priorityCtx = document.getElementById('priorityChart').getContext('2d');
        new Chart(priorityCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(priority_labels)},
                datasets: [{{
                    label: 'Number of Projects',
                    data: {json.dumps(priority_data)},
                    backgroundColor: '#3498db',
                    borderRadius: 8
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Progress Chart
        const progressCtx = document.getElementById('progressChart').getContext('2d');
        new Chart(progressCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(progress_labels)},
                datasets: [{{
                    label: 'Progress %',
                    data: {json.dumps(progress_values)},
                    backgroundColor: ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#16a085'],
                    borderRadius: 8
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Language Chart
        const languageCtx = document.getElementById('languageChart').getContext('2d');
        new Chart(languageCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(lang_labels)},
                datasets: [{{
                    label: 'Times Used',
                    data: {json.dumps(lang_data)},
                    backgroundColor: {json.dumps(lang_colors)},
                    borderRadius: 8
                }}]
            }},
            options: {{
                ...chartOptions,
                indexAxis: 'y',
                scales: {{
                    x: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
        
        // Project List
        const projectsList = document.getElementById('projectsList');
        const projects = {json.dumps(self.projects)};
        projects.forEach((project, index) => {{
            const statusBadge = `<span class="badge badge-${{project.status.toLowerCase().replace(' ', '-')}}">${{project.status}}</span>`;
            const html = `
                <div class="project-item">
                    <strong>${{project.name}}</strong> ${{statusBadge}}
                    <br><small>
                        Frontend: <strong>${{project.frontend_language}}</strong> | 
                        Backend: <strong>${{project.backend_language}}</strong> |
                        Progress: <strong>${{project.progress}}%</strong>
                    </small>
                </div>
            `;
            projectsList.innerHTML += html;
        }});
    </script>
</body>
</html>
        """
        return html
    
    def logout(self):
        """Save current data and return to login screen"""
        self.save_data()
        self.root.destroy()
        # Create new login window
        new_root = tk.Tk()
        login_app = LoginWindow(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()