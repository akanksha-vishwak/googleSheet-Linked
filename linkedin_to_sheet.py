import os
import json
import re
import time
import gspread
import google.generativeai as genai
from openai import OpenAI
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime

# --- Load environment variables ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

# --- Google Sheets Authentication ---
def connect_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(GOOGLE_SHEET_NAME).sheet1

# --- Load LinkedIn Job Page ---
def get_job_soup_and_text(url):
    
    options = Options()
    # notes for myself: By default, Selenium launches a visible Chrome window unless specified otherwise
    # added a few lined to make it headless
    options.add_argument("--headless=new")  # Use new headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup, soup.get_text(separator="\n")

# --- Detect External Application Link ---
def detect_external_link(soup):
    button = soup.find("button", string=lambda s: s and "Apply" in s)
    if button:
        link = button.find_parent("a")
        if link and link.get("href"):
            return link["href"]
    return ""

# --- Clean Output JSON Code Block ---
def clean_model_output(text):
    return re.sub(r"```(?:json)?\n([\s\S]*?)```", r"\1", text).strip()

# --- Shared Prompt ---
def get_extraction_prompt(job_text):
    return f"""
You are a helpful assistant. Extract the following fields from the entire page content of a LinkedIn job post:

- Job Title
- Company
- Location
- Work Mode (Remote/Hybrid)
- Job Type (Full-time/Part-time/Contract)
- Application Method (Easy Apply/External)
- Salary (if mentioned)
- Special Note (e.g. "Meet the hiring team", "reviewed by humans")

Return as JSON with keys:
"Job Title", "Company", "Location", "Work Mode", "Job Type", "Application Method", "Salary", "Special Note"

Job Description:
{job_text[:10000]}
"""

# --- Extract Fields with Gemini ---
def extract_with_gemini(job_text):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = get_extraction_prompt(job_text)
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Extract Fields with OpenAI (modern SDK) ---
def extract_with_openai(job_text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = get_extraction_prompt(job_text)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    reply = response.choices[0].message.content.strip()
    return reply

# --- Save to Google Sheet ---
def save_to_sheet(sheet, data_dict, job_url, external_link):
    today = datetime.today().strftime('%Y-%m-%d')
    fields = ["Job Title", "Company", "Location", "Work Mode", "Job Type", "Application Method", "Salary", "Special Note"]
    row = [today, job_url] + [data_dict.get(field, "") for field in fields] + [external_link]
    sheet.append_row(row)

# --- Main ---
if __name__ == "__main__":
    url = input("Paste LinkedIn Job URL: ").strip()
    model_choice = input("Which model do you want to use? [gemini/openai] (default: gemini): ").strip().lower()

    soup, job_text = get_job_soup_and_text(url)
    external_link = detect_external_link(soup)

    # Choose model
    if model_choice == "openai":
        raw_output = extract_with_openai(job_text)
    else:
        raw_output = extract_with_gemini(job_text)

    cleaned_output = clean_model_output(raw_output)

    try:
        parsed_data = json.loads(cleaned_output)
    except json.JSONDecodeError:
        print("Could not parse model output:")
        print(raw_output)
        exit(1)

    parsed_data["Job URL"] = url
    parsed_data["External Link"] = external_link

    print(json.dumps(parsed_data, indent=2))

    sheet = connect_sheet()
    save_to_sheet(sheet, parsed_data, url, external_link)

    print("Job info saved to Google Sheet.")
