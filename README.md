# LinkedIn to Sheet: AI-Powered Job Tracker

I created this python script to automate the extraction of key details from LinkedIn job postings and organizing them neatly in a Google Sheet, saving time and effort for job seekers.

## Features
- Scrapes LinkedIn job pages for key details: Job Title, Company, Location, Work Mode, Job Type, Application Method, Salary, and Special Notes.
- Supports two AI models for data extraction: Google Gemini and OpenAI GPT-4.
- Saves extracted data to a Google Sheet with a timestamp and job URL.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/akanksha-vishwak/googleSheet-Linked.git
   cd googleSheet-Linked
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env` and fill in the required values

4. Ensure ChromeDriver is installed and accessible in your system PATH or specify its path in the script.

## Usage
1. Run the script:
   ```bash
   python linkedin_to_sheet.py
   ```
2. When prompted, paste the LinkedIn job URL.
3. Choose the AI model (`gemini` or `openai`). Press Enter to default to Gemini.
4. The script will:
   - Scrape the job page.
   - Extract details using the chosen AI model.
   - Save the data to the specified Google Sheet.
   - Print the extracted data in JSON format.

## Prerequisites
- Python 3.8+
- Google Chrome and ChromeDriver (compatible versions)
- A Google Cloud project with Google Sheets and Drive APIs enabled
- A service account key file for Google Sheets authentication
- API keys for Google Gemini and/or OpenAI (depending on the model used)

## Configuration
- **Google Sheets Setup**:
  - Create a Google Sheet and note its name.
  - Generate a service account key from the Google Cloud Console.
  - Share the Google Sheet with the service account email.

### My local set up 
```bash
avishwak@S44-936JLVDM googleSheet-Linked % which python     
/Users/avishwak/apps/anaconda3/bin/python
avishwak@S44-936JLVDM googleSheet-Linked % which pip   
/Users/avishwak/apps/anaconda3/bin/pip
avishwak@S44-936JLVDM googleSheet-Linked % /usr/local/bin/python3.11 -m venv .venv
avishwak@S44-936JLVDM googleSheet-Linked % source .venv/bin/activate
(.venv) avishwak@S44-936JLVDM googleSheet-Linked % which python
/Users/avishwak/Documents/gitHub/googleSheet-Linked/.venv/bin/python
(.venv) avishwak@S44-936JLVDM googleSheet-Linked % which pip
/Users/avishwak/Documents/gitHub/googleSheet-Linked/.venv/bin/pip
(.venv) avishwak@S44-936JLVDM googleSheet-Linked % pip install -r requirements.txt
python linkedin_to_sheet.py    
Paste LinkedIn Job URL: https://www.linkedin.com/jobs/view/4234395663/
Which model do you want to use? [gemini/openai] (default: gemini):  
```