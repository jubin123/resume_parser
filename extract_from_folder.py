import re
import os
import spacy
from pyresparser import ResumeParser
from pdfminer.high_level import extract_text
from spacy.matcher import Matcher

class Parser:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def extract_text_from_pdf(self, pdf_path):
        return extract_text(pdf_path)

    def extract_contact_number_from_resume(self, text):
        contact_number = None

        # Use regex pattern to find a potential contact number
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        if match:
            contact_number = match.group()

        return contact_number

    def extract_email_from_resume(self, text):
        email = None

        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        if match:
            email = match.group()

        return email

    def extract_name(self, resume_text):
        nlp = spacy.load('en_core_web_sm')
        matcher = Matcher(nlp.vocab)

        # Define name patterns
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
            # Add more patterns as needed
        ]

        for pattern in patterns:
            matcher.add('NAME', patterns=[pattern])

        doc = nlp(resume_text)
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None
    
    def create_df(self):
        resume_paths=[]
        for resume in os.listdir(self.folder_path):
            resume_path = f"{self.folder_path}/{resume}"
            resume_paths.append(resume_path)

        columns = ['Resume', 'Name', 'Contact', 'Email', 'Skills', 'Education']
        df = pd.DataFrame(columns=columns)

        for resume_path in resume_paths:
            text = self.extract_text_from_pdf(resume_path)
            data = ResumeParser(resume_path).get_extracted_data()

            resume_path = resume_path
            name = self.extract_name(text)
            contact_number = self.extract_contact_number_from_resume(text)
            email = self.extract_email_from_resume(text)
            extracted_skills = data['skills']
            extracted_education = data['degree']
            new_data = {
                'Resume': resume_path,
                'Name': name,
                'Contact': contact_number,
                'Email': email,
                'Skills': extracted_skills,
                'Education': extracted_education
            }
            df = df.append(new_data, ignore_index=True)

        return df