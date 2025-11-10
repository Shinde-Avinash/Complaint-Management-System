#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from db import DBConnect
from listComp import ListComp

class ComplaintApp:
    def __init__(self):
        self.conn = DBConnect()
        self.root = Tk()
        self.root.geometry('700x550')
        self.root.title('Complaint Management System')
        self.root.configure(background='#f5f6fa')
        self.root.resizable(False, False)
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       background='#f5f6fa',
                       foreground='#2c3e50')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 10),
                       background='#f5f6fa',
                       foreground='#7f8c8d')
        
        style.configure('Field.TLabel',
                       font=('Segoe UI', 11),
                       background='#f5f6fa',
                       foreground='#34495e')
        
        style.configure('Submit.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=10)
        
        style.configure('List.TButton',
                       font=('Segoe UI', 11),
                       padding=10)
        
        style.configure('TRadiobutton',
                       font=('Segoe UI', 10),
                       background='#f5f6fa')
        
        style.map('Submit.TButton',
                 background=[('active', '#27ae60'), ('!active', '#2ecc71')],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
        style.map('List.TButton',
                 background=[('active', '#2980b9'), ('!active', '#3498db')],
                 foreground=[('active', 'white'), ('!active', 'white')])
    
    def create_widgets(self):
        # Header Frame
        header_frame = Frame(self.root)
        header_frame.configure(style='TFrame')
        header_frame.pack(fill=X, pady=(20, 10))
        
        title = Label(header_frame, 
                     text='📋 Complaint Management',
                     style='Title.TLabel')
        title.pack()
        
        subtitle = Label(header_frame,
                        text='Submit your complaints and feedback',
                        style='Subtitle.TLabel')
        subtitle.pack()
        
        # Main Content Frame
        content_frame = Frame(self.root)
        content_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)
        
        # Full Name
        name_frame = Frame(content_frame)
        name_frame.pack(fill=X, pady=10)
        
        Label(name_frame, text='Full Name *', style='Field.TLabel').pack(anchor=W, pady=(0, 5))
        self.fullname = Entry(name_frame, font=('Segoe UI', 11), width=50)
        self.fullname.pack(fill=X, ipady=8)
        
        # Gender
        gender_frame = Frame(content_frame)
        gender_frame.pack(fill=X, pady=10)
        
        Label(gender_frame, text='Gender *', style='Field.TLabel').pack(anchor=W, pady=(0, 5))
        
        radio_container = Frame(gender_frame)
        radio_container.pack(anchor=W)
        
        self.gender_var = StringVar(value='')
        
        Radiobutton(radio_container, 
                   text='Male', 
                   value='Male', 
                   variable=self.gender_var).pack(side=LEFT, padx=(0, 20))
        
        Radiobutton(radio_container,
                   text='Female',
                   value='Female',
                   variable=self.gender_var).pack(side=LEFT, padx=(0, 20))
        
        Radiobutton(radio_container,
                   text='Other',
                   value='Other',
                   variable=self.gender_var).pack(side=LEFT)
        
        # Comment
        comment_frame = Frame(content_frame)
        comment_frame.pack(fill=BOTH, expand=True, pady=10)
        
        Label(comment_frame, text='Your Complaint *', style='Field.TLabel').pack(anchor=W, pady=(0, 5))
        
        # Text widget with scrollbar
        text_container = Frame(comment_frame)
        text_container.pack(fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(text_container)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.comment = Text(text_container,
                           font=('Segoe UI', 10),
                           wrap=WORD,
                           yscrollcommand=scrollbar.set,
                           height=8,
                           relief=SOLID,
                           borderwidth=1)
        self.comment.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.comment.yview)
        
        # Button Frame
        button_frame = Frame(content_frame)
        button_frame.pack(fill=X, pady=(20, 0))
        
        self.submit_btn = Button(button_frame,
                                text='Submit Complaint',
                                style='Submit.TButton',
                                command=self.save_data)
        self.submit_btn.pack(side=RIGHT, padx=5)
        
        self.list_btn = Button(button_frame,
                              text='View All Complaints',
                              style='List.TButton',
                              command=self.show_list)
        self.list_btn.pack(side=RIGHT, padx=5)
        
        clear_btn = Button(button_frame,
                          text='Clear Form',
                          command=self.clear_form)
        clear_btn.pack(side=RIGHT, padx=5)
    
    def save_data(self):
        name = self.fullname.get().strip()
        gender = self.gender_var.get()
        comment = self.comment.get(1.0, END).strip()
        
        if not name:
            showwarning('Validation Error', 'Please enter your full name.')
            self.fullname.focus()
            return
        
        if not gender:
            showwarning('Validation Error', 'Please select your gender.')
            return
        
        if not comment:
            showwarning('Validation Error', 'Please enter your complaint.')
            self.comment.focus()
            return
        
        msg = self.conn.Add(name, gender, comment)
        showinfo('Success', msg)
        self.clear_form()
    
    def show_list(self):
        ListComp()
    
    def clear_form(self):
        self.fullname.delete(0, END)
        self.gender_var.set('')
        self.comment.delete(1.0, END)
        self.fullname.focus()
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ComplaintApp()
    app.run()