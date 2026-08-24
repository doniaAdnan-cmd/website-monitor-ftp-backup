System Requirements & Setup Instructions
========================================

Operating System
----------------
- Windows 10

Running Apache/XAMPP
--------------------
- Start Apache through the XAMPP Control Panel by clicking the Start button next to Apache.

Local Website URL
-----------------
- http://localhost/mywebsite/index.html

Command to Start the Local FTP Server
-------------------------------------
python -m pyftpdlib --interface=127.0.0.1 --port=2121 --directory "C:\ftp_storage" --write

How to Run main.py
------------------
1. Open the project folder: final_project
2. Start Apache from XAMPP and make sure the website is running.
3. Open a terminal (Command Prompt or PowerShell) and start the FTP server.
4. Navigate to the project folder using:
   cd final_project
5. Run the program:
   python main.py
6. Enter your Gmail email address.
7. Enter your Gmail App Password (not your regular password).
8. Choose an option from the menu:
   - Option 1: Check Website Status
   - Option 2: Create a ZIP backup and upload it to the FTP server
   - Option 3: Exit the program

Important Notes
---------------
- Your Gmail password or App Password must never be included in any files or screenshots.
- All operations run locally, using only localhost and 127.0.0.1.
