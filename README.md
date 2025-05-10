# LinkedIn to Sheet: AI-Powered Job Tracker

Searching for a job can be an overwhelming journey, especially when applying to over 100 opportunities each month. Manually tracking job details, application methods, and outcomes is exhausting and time-consuming. This Python script was created to streamline the process by automating the extraction of key details from LinkedIn job postings and organizing them neatly in a Google Sheet, saving time and effort for job seekers.

## Features
- Scrapes LinkedIn job pages for key details: Job Title, Company, Location, Work Mode, Job Type, Application Method, Salary, and Special Notes.
- Supports two AI models for data extraction: Google Gemini and OpenAI GPT-4.
- Detects external application links (if the job requires applying on an external site).
- Saves extracted data to a Google Sheet with a timestamp and job URL.
- Configurable via environment variables.

## Prerequisites
- Python 3.8+
- Google Chrome and ChromeDriver (compatible versions)
- A Google Cloud project with Google Sheets and Drive APIs enabled
- A service account key file for Google Sheets authentication
- API keys for Google Gemini and/or OpenAI (depending on the model used)

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

3. Copy the `.env.example` file to `.env` and fill in the required values:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to include:
   ```plaintext
   GEMINI_API_KEY=<your-gemini-api-key>
   OPENAI_API_KEY=<your-openai-api-key>
   GOOGLE_SHEET_NAME=<your-google-sheet-name>
   SERVICE_ACCOUNT_FILE=<path-to-service-account-json>
   ```

4. Ensure ChromeDriver is installed and accessible in your system PATH or specify its path in the script.

## Usage
1. Run the script:
   ```bash
   python script.py
   ```

2. When prompted, paste the LinkedIn job URL.
3. Choose the AI model (`gemini` or `openai`). Press Enter to default to Gemini.
4. The script will:
   - Scrape the job page.
   - Extract details using the chosen AI model.
   - Detect external application links.
   - Save the data to the specified Google Sheet.
   - Print the extracted data in JSON format.


## Configuration
- **Google Sheets Setup**:
  - Create a Google Sheet and note its name.
  - Generate a service account key from the Google Cloud Console.
  - Share the Google Sheet with the service account email.
- **Environment Variables** (defined in `.env`):
  - `GEMINI_API_KEY`: Obtain from Google AI Studio.
  - `OPENAI_API_KEY`: Obtain from OpenAI platform.
  - `GOOGLE_SHEET_NAME`: Name of the target Google Sheet.
  - `SERVICE_ACCOUNT_FILE`: Path to the service account JSON key file.