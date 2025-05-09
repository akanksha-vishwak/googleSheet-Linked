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
   git clone <repository-url>
   cd <repository-directory>
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

## Dependencies
- `os`, `json`, `re`, `time`, `datetime` (standard library)
- `gspread` - Google Sheets API client
- `google-auth` - Google API authentication
- `google-generativeai` - Google Gemini API
- `openai` - OpenAI API client
- `beautifulsoup4` - HTML parsing
- `selenium` - Browser automation
- `python-dotenv` - Environment variable management

Install via:
```bash
pip install gspread google-auth google-generativeai openai beautifulsoup4 selenium python-dotenv
```

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

## Script Workflow
1. **Load Environment Variables**: Reads API keys and configuration from `.env`.
2. **Google Sheets Authentication**: Connects to the specified Google Sheet using service account credentials.
3. **Web Scraping**: Uses Selenium to load the LinkedIn job page and BeautifulSoup to parse the HTML.
4. **External Link Detection**: Checks for external application links in the job page.
5. **Data Extraction**: Sends the job page text to the chosen AI model (Gemini or OpenAI) to extract structured data in JSON format.
6. **Data Cleaning**: Removes markdown code fences from the AI model output.
7. **Save to Google Sheet**: Appends the extracted data, timestamp, job URL, and external link to the Google Sheet.
8. **Output**: Prints the extracted data in JSON format.

## Notes
- The script truncates job text to 10,000 characters to avoid exceeding AI model input limits.
- Ensure ChromeDriver matches your Chrome browser version.
- The Google Sheet must have write permissions for the service account.
- The script assumes the Google Sheet has a header row; data is appended as new rows.
- Error handling is minimal; invalid JSON output from the AI model will cause the script to exit.

## Limitations
- LinkedIn's dynamic content may require adjusting the Selenium wait time (`time.sleep(5)`).
- AI models may occasionally misinterpret fields or return malformed JSON.
- Rate limits on API calls (Gemini, OpenAI, or Google Sheets) may affect performance.
- The script is designed for single job URLs; batch processing is not supported.

## Troubleshooting
- **ChromeDriver Errors**: Ensure ChromeDriver is installed and matches your Chrome version.
- **API Key Issues**: Verify API keys in `.env` and ensure they are active.
- **Google Sheets Access**: Confirm the service account has edit access to the Google Sheet.
- **JSON Parsing Errors**: Check the AI model output (printed to console) for formatting issues.

## License
This project is licensed under the Apache-2.0 License.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.