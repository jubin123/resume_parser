import sqlite3
import pandas as pd
import streamlit as st

# Connect to the SQLite database
conn = sqlite3.connect('resumes.db')

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Function to insert values into the 'resumes' table
def insert_resume(name, email, phone_number, previous_job_history, education, skills, resume_path):
    query = """INSERT INTO resumes (name, email, phone_number, previous_job_history, education, skills, resume_path) 
               VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(query, (name, email, phone_number, previous_job_history, education, skills, resume_path))
    conn.commit()

# Insert sample values into the 'resumes' table
insert_resume("John Doe", "john.doe@example.com", "123-456-7890", "Software Engineer at XYZ Corp", "Bachelor's in Computer Science", "Python, JavaScript, SQL", "/path/to/resume1.pdf")
insert_resume("Jane Smith", "jane.smith@example.com", "987-654-3210", "Data Analyst at ABC Inc", "Master's in Statistics", "Data Analysis, Python, R", "/path/to/resume2.pdf")

# Fetch data from the 'resumes' table into a DataFrame

# Close the connection
conn.close()

# Streamlit app to display the DataFrame

