#!/usr/bin/python3
import sqlite3

class DBConnect:
    def __init__(self):
        self._db = sqlite3.connect('information.db')
        self._db.row_factory = sqlite3.Row
        self._db.execute('''
            CREATE TABLE IF NOT EXISTS Comp(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                Name VARCHAR(255), 
                Gender VARCHAR(255), 
                Comment TEXT,
                DateSubmitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self._db.commit()
    
    def Add(self, name, gender, comment):
        if not name or not gender or not comment.strip():
            return 'Error: All fields are required.'
        self._db.execute(
            'INSERT INTO Comp (Name, Gender, Comment) VALUES (?,?,?)',
            (name, gender, comment)
        )
        self._db.commit()
        return 'Your complaint has been submitted successfully!'
    
    def ListRequest(self):
        cursor = self._db.execute('SELECT * FROM Comp ORDER BY ID DESC')
        return cursor
    
    def Delete(self, id):
        self._db.execute('DELETE FROM Comp WHERE ID=?', (id,))
        self._db.commit()
        return 'Complaint deleted successfully!'
    
    def close(self):
        self._db.close()