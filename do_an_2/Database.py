import tkinter as tk
from tkinter import messagebox
from Module import DatabaseManager  # Ensure you import DatabaseManager

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Create an instance of DatabaseManager
        self.db_manager = DatabaseManager()

        # Database connection fields
        self.db_name = tk.StringVar(value='')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='danhsach')
        self.selected_stt = tk.StringVar()

        # Input fields for hoten and nganh_hoc
        self.column1 = tk.StringVar()  # hoten
        self.column2 = tk.StringVar()  # nganh_hoc
        self.column_mssv = tk.StringVar()  # mssv

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Table operation section
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        tk.Button(table_frame, text="Create New Table", command=self.create_table).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(table_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(table_frame, text="Select Table", command=self.select_table).grid(row=1, column=0, pady=5)
        tk.Button(table_frame, text="Delete Table", command=self.delete_table).grid(row=1, column=1, pady=5)

        # Data input section
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="STT:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.selected_stt).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="MSSV:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.column_mssv).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Ho Ten:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.column1).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Nganh Hoc:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.column2).grid(row=3, column=1, padx=5, pady=5)

        # Data display and action section
        data_frame = tk.Frame(self.root)
        data_frame.pack(pady=10)

        # Scrollable Textbox
        self.scroll_text = tk.Text(data_frame, height=10, width=50)
        self.scroll_text.pack(side=tk.LEFT, padx=5, pady=5)

        scrollbar = tk.Scrollbar(data_frame, command=self.scroll_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_text.config(yscrollcommand=scrollbar.set)

        # Buttons to add, update, delete
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Update Entry", command=self.update_entry).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Delete Entry", command=self.delete_entry).pack(side=tk.LEFT, padx=5, pady=5)

    def connect_db(self):
        result = self.db_manager.connect(
            self.db_name.get(),
            self.user.get(),
            self.password.get(),
            self.host.get(),
            self.port.get()
        )
        messagebox.showinfo("Info", result)

    def create_table(self):
        result = self.db_manager.create_table(self.table_name.get())
        messagebox.showinfo("Info", result)

    def select_table(self):
        result, rows = self.db_manager.select_table(self.table_name.get())
        self.scroll_text.delete(1.0, tk.END)  # Clear previous text
        if result == "Success":
            for row in rows:
                self.scroll_text.insert(tk.END, str(row) + "\n")
        else:
            messagebox.showerror("Error", result)

    def add_entry(self):
        result = self.db_manager.add_entry(
            self.table_name.get(),
            self.column_mssv.get(),
            self.column1.get(),
            self.column2.get()
        )
        messagebox.showinfo("Info", result)

    def update_entry(self):
        result = self.db_manager.update_entry(
            self.table_name.get(),
            self.column_mssv.get(),
            self.column1.get(),
            self.column2.get(),
            self.selected_stt.get()
        )
        messagebox.showinfo("Info", result)

    def delete_entry(self):
        result = self.db_manager.delete_entry(self.table_name.get(), self.selected_stt.get())
        messagebox.showinfo("Info", result)

    def delete_table(self):
        result = self.db_manager.delete_table(self.table_name.get())
        messagebox.showinfo("Info", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

