import os
import json
import re
import time
import gspread
import google.generativeai as genai
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# --- Config ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEET_NAME = "job-tracker"
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

# --- Google Sheets Auth ---
def connect_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(GOOGLE_SHEET_NAME).sheet1

# --- Load LinkedIn Job Page ---
def get_job_html_and_text(url):
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    return html, soup.get_text(separator="\n")

# --- Detect External Application Link ---
def detect_external_link(soup):
    button = soup.find("button", string=lambda s: s and "Apply" in s)
    if button:
        link = button.find_parent("a")
        if link and link.get("href"):
            return link["href"]
    return ""

# --- Clean Gemini Output ---
def clean_gemini_output(text):
    return re.sub(r"```(?:json)?\n([\s\S]*?)```", r"\1", text).strip()

# --- Gemini Extraction ---
def extract_fields_with_gemini(job_text):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    prompt = f"""
You are a helpful assistant. Extract the following fields from the **entire page content** (not just job description) of a LinkedIn job post, very carefully:

- Job Title
- Company
- Location
- Work Mode (Remote/Hybrid)
- Job Type (Full-time/Part-time/Contract)
- Application Method (Easy Apply/External) **You can check if there is "Easy Apply" or "Apply"**
- Salary (if mentioned)
- Special Note (mention if the post says "Meet the hiring team" or "reviewed by humans")

Return as JSON with keys:
"Job Title", "Company", "Location", "Work Mode", "Job Type", "Application Method", "Salary", "Special Note"

Job Description:
{job_text[:5000]}
"""
    response = model.generate_content(prompt)
    print("Gemini response:", response.text.strip())
    return response.text.strip()

# --- Save to Sheet ---
def save_to_sheet(sheet, data_dict, job_url, external_link):
    today = datetime.today().strftime('%Y-%m-%d')
    row = [
        today,
        job_url,
        data_dict.get("Job Title", ""),
        data_dict.get("Company", ""),
        data_dict.get("Location", ""),
        data_dict.get("Work Mode", ""),
        data_dict.get("Job Type", ""),
        data_dict.get("Application Method", ""),
        data_dict.get("Salary", ""),
        data_dict.get("Special Note", ""),
        external_link
    ]
    sheet.append_row(row)

# --- Main ---
if __name__ == "__main__":
    url = input("Paste LinkedIn Job URL: ")
    html, job_text = get_job_html_and_text(url)

    # Detect application external link
    soup = BeautifulSoup(html, "html.parser")
    external_link = detect_external_link(soup)

    # Extract fields from Gemini
    fields = extract_fields_with_gemini(job_text)
    cleaned = clean_gemini_output(fields)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        print("Could not parse Gemini output:")
        print(fields)
        exit(1)

    # Add job URL and external link to parsed data for printing
    parsed["Job URL"] = url
    parsed["External Link"] = external_link

    # Print JSON to terminal
    print(json.dumps(parsed, indent=2))

    # Save to Google Sheet
    sheet = connect_sheet()
    save_to_sheet(sheet, parsed, url, external_link)
    
    print("Job info saved to Google Sheet.")
