#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from db import DBConnect
import sqlite3

class ListComp:
    def __init__(self):
        self._dbconnect = DBConnect()
        self._root = Toplevel()
        self._root.title('Complaints List')
        self._root.geometry('1000x600')
        self._root.configure(background='#f5f6fa')
        
        self.setup_styles()
        self.create_widgets()
        self.load_data()
        
    def setup_styles(self):
        style = Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       background='#f5f6fa',
                       foreground='#2c3e50')
        
        style.configure('Treeview',
                       font=('Segoe UI', 10),
                       rowheight=30,
                       background='white',
                       fieldbackground='white',
                       foreground='#2c3e50')
        
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       background='#34495e',
                       foreground='white',
                       relief=FLAT)
        
        style.map('Treeview.Heading',
                 background=[('active', '#2c3e50')])
        
        style.map('Treeview',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
    
    def create_widgets(self):
        # Header
        header_frame = Frame(self._root)
        header_frame.pack(fill=X, pady=20, padx=30)
        
        title = Label(header_frame,
                     text='📊 All Complaints',
                     style='Title.TLabel')
        title.pack(side=LEFT)
        
        # Buttons
        btn_frame = Frame(header_frame)
        btn_frame.pack(side=RIGHT)
        
        refresh_btn = Button(btn_frame,
                            text='🔄 Refresh',
                            command=self.load_data)
        refresh_btn.pack(side=LEFT, padx=5)
        
        delete_btn = Button(btn_frame,
                           text='🗑️ Delete Selected',
                           command=self.delete_selected)
        delete_btn.pack(side=LEFT, padx=5)
        
        # Treeview Frame
        tree_frame = Frame(self._root)
        tree_frame.pack(fill=BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Scrollbars
        vsb = Scrollbar(tree_frame, orient=VERTICAL)
        vsb.pack(side=RIGHT, fill=Y)
        
        hsb = Scrollbar(tree_frame, orient=HORIZONTAL)
        hsb.pack(side=BOTTOM, fill=X)
        
        # Treeview
        self.tv = Treeview(tree_frame,
                          columns=('Name', 'Gender', 'Comment', 'Date'),
                          show='headings',
                          yscrollcommand=vsb.set,
                          xscrollcommand=hsb.set)
        
        vsb.config(command=self.tv.yview)
        hsb.config(command=self.tv.xview)
        
        # Configure columns
        self.tv.heading('Name', text='Name', anchor=W)
        self.tv.heading('Gender', text='Gender', anchor=CENTER)
        self.tv.heading('Comment', text='Complaint', anchor=W)
        self.tv.heading('Date', text='Date Submitted', anchor=CENTER)
        
        self.tv.column('Name', width=150, anchor=W)
        self.tv.column('Gender', width=100, anchor=CENTER)
        self.tv.column('Comment', width=500, anchor=W)
        self.tv.column('Date', width=150, anchor=CENTER)
        
        self.tv.pack(fill=BOTH, expand=True)
        
        # Status bar
        self.status_frame = Frame(self._root)
        self.status_frame.pack(fill=X, side=BOTTOM, pady=(0, 10), padx=30)
        
        self.status_label = Label(self.status_frame,
                                 text='',
                                 font=('Segoe UI', 9),
                                 background='#f5f6fa',
                                 foreground='#7f8c8d')
        self.status_label.pack(side=LEFT)
        
        # Bind double-click to view details
        self.tv.bind('<Double-1>', self.view_details)
    
    def load_data(self):
        # Clear existing data
        for item in self.tv.get_children():
            self.tv.delete(item)
        
        # Load from database
        cursor = self._dbconnect.ListRequest()
        count = 0
        
        for row in cursor:
            # Store ID in tags for later retrieval
            self.tv.insert('', 'end',
                          values=(row['Name'],
                                 row['Gender'],
                                 row['Comment'][:100] + '...' if len(row['Comment']) > 100 else row['Comment'],
                                 row['DateSubmitted'] if 'DateSubmitted' in row.keys() else 'N/A'),
                          tags=(row['ID'],))
            count += 1
        
        self.status_label.config(text=f'Total Complaints: {count}')
    
    def delete_selected(self):
        selected = self.tv.selection()
        if not selected:
            showwarning('No Selection', 'Please select a complaint to delete.')
            return
        
        if askyesno('Confirm Delete', 'Are you sure you want to delete the selected complaint?'):
            for item in selected:
                tags = self.tv.item(item, 'tags')
                if tags:
                    complaint_id = tags[0]
                    self._dbconnect.Delete(complaint_id)
                    self.tv.delete(item)
            
            showinfo('Success', 'Complaint deleted successfully!')
            self.load_data()
    
    def view_details(self, event):
        selected = self.tv.selection()
        if not selected:
            return
        
        item = selected[0]
        values = self.tv.item(item, 'values')
        
        # Create detail window
        detail_window = Toplevel(self._root)
        detail_window.title('Complaint Details')
        detail_window.geometry('600x400')
        detail_window.configure(background='#f5f6fa')
        
        # Header
        Label(detail_window,
              text='Complaint Details',
              font=('Segoe UI', 16, 'bold'),
              background='#f5f6fa',
              foreground='#2c3e50').pack(pady=20)
        
        # Details frame
        details_frame = Frame(detail_window)
        details_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)
        
        fields = [
            ('Name:', values[0]),
            ('Gender:', values[1]),
            ('Date:', values[3]),
        ]
        
        for label, value in fields:
            frame = Frame(details_frame)
            frame.pack(fill=X, pady=5)
            
            Label(frame,
                  text=label,
                  font=('Segoe UI', 10, 'bold'),
                  background='#f5f6fa',
                  width=15,
                  anchor=W).pack(side=LEFT)
            
            Label(frame,
                  text=value,
                  font=('Segoe UI', 10),
                  background='#f5f6fa',
                  anchor=W).pack(side=LEFT, fill=X, expand=True)
        
        # Comment
        Label(details_frame,
              text='Complaint:',
              font=('Segoe UI', 10, 'bold'),
              background='#f5f6fa',
              anchor=W).pack(fill=X, pady=(10, 5))
        
        comment_text = Text(details_frame,
                           font=('Segoe UI', 10),
                           wrap=WORD,
                           height=10,
                           relief=SOLID,
                           borderwidth=1)
        comment_text.pack(fill=BOTH, expand=True)
        comment_text.insert(1.0, values[2].replace('...', ''))
        comment_text.config(state=DISABLED)
        
        # Close button
        Button(detail_window,
               text='Close',
               command=detail_window.destroy).pack(pady=20)