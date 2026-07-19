#!/usr/bin/env python3
import sqlite3
from pathlib import Path
p=Path(__file__).with_name('demo.sqlite3')
p.unlink(missing_ok=True)
con=sqlite3.connect(p)
con.executescript('''
CREATE TABLE records(title TEXT NOT NULL, summary TEXT NOT NULL);
CREATE TABLE files(id TEXT PRIMARY KEY, download_name TEXT NOT NULL, content BLOB NOT NULL);
INSERT INTO records VALUES ('Synthetic cohort', 'Demonstration data only; no clinical interpretation.');
INSERT INTO records VALUES ('Quality summary', 'A safe read-only database query example.');
INSERT INTO files VALUES ('0123456789abcdef0123456789abcdef', 'example.txt', X'5243435F50524F5445435445445F46494C455F4F4B0A');
''')
con.commit(); con.close()
print(p)
