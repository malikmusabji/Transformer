import os
from PyPDF2 import PdfReader
import shutil
import sqlite3

# Database setup
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS files (
    FileName TEXT,
    FileType TEXT
)
''')

# Login functionality
def login(username, password):
    # Placeholder for actual credential check
    # Example: You could add logic to verify user credentials from a database
    return username == "admin" and password == "password"

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')

if st.sidebar.checkbox("Login"):
    if login(username, password):
        st.success("You are now logged in as " + username)

        # Allow file upload
        uploaded_file = st.file_uploader(label='Choose a PDF')

        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
            c.execute('INSERT INTO files (FileName, FileType) VALUES (:FileName, :FileType)', file_details)

            # Save file to 'uploads' directory
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process PDF
            reader = PdfReader(file_path)
            text = [page.extract_text() for page in reader.pages]

            # Detect courses using AI or NLP (placeholder for actual course detection logic)
            courses = []  # Replace with actual NLP/ML to identify course names
            for page_text in text:
                # Assuming we add a detected course for example purposes
                courses.append("Example Course")  # This is a placeholder for course detection

            # Make folders for courses and save pages that mention the course
            for course in set(courses):
                course_path = os.path.join("courses", course)
                os.makedirs(course_path, exist_ok=True)
                
                # Copy relevant pages to the course folder
                for page_index, page_text in enumerate(text):
                    if course in page_text:
                        dest_path = os.path.join(course_path, f"{uploaded_file.name}_page_{page_index+1}.txt")
                        with open(dest_path, "w") as page_file:
                            page_file.write(page_text)

            conn.commit()
            st.success("PDF has been processed!")

    else:
        st.error("Incorrect username/password")
else:
    st.info("Please log in to upload and process files.")

# Close the database connection at the end of the script
conn.close()
