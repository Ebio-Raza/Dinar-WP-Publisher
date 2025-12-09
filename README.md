# DinarGuru Bot

A desktop application for scraping financial blog posts from Dinar-related websites and publishing them to WordPress.

## Overview

DinarGuru Bot is a Python-based GUI application that automates the extraction of blog posts from financial news websites (DinarGuru and DinarRecaps) and enables one-click publishing to WordPress. The application features a modern dark-themed interface built with CustomTkinter.

## Features

- **Multi-Site Scraping**: Extract posts from DinarGuru and DinarRecaps websites
- **WordPress Publishing**: Automated post publishing with anti-detection measures
- **Data Export**: Download extracted posts as JSON or CSV files
- **Modern GUI**: Dark-themed interface with real-time status indicators
- **Standalone Executable**: Can be compiled into a portable executable

## Directory Structure

```
Final/
├── app.py                    # Main GUI application entry point
├── dinar_guru_bot.py         # DinarGuru website scraper module
├── dinar_recaps_bot.py       # DinarRecaps website scraper module
├── word_press_bot.py         # WordPress publishing automation
├── utils.py                  # Utility functions (export, file handling)
├── requirements.txt          # Python dependencies
├── DinarGuruBot.spec         # PyInstaller build configuration
├── build.ipynb               # Jupyter notebook for building executable
├── build/                    # PyInstaller build artifacts
├── dist/                     # Compiled executable output
└── __pycache__/              # Python bytecode cache
```

## Installation

### Prerequisites

- Python 3.12 or higher
- Google Chrome browser (required for web scraping)

### Setup

1. Clone or download the project to your local machine

2. Navigate to the Final folder:
   ```bash
   cd Final
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Additional dependency (for WordPress publishing):
   ```bash
   pip install undetected-chromedriver
   ```

## Usage

### Running the Application

```bash
python app.py
```

### GUI Interface

The application window displays:

- **Status Indicator**: Color-coded dot showing current state
  - Green: Ready/Success
  - Yellow: Processing
  - Red: Error

- **Bot Buttons**:
  - `DinarGuru`: Scrape posts from dinarguru.com
  - `DinarRecaps`: Scrape posts from dinarrecaps.com
  - `DinarTiru`: Placeholder (not implemented)

- **Posts Display**: Scrollable area showing extracted posts

- **Action Buttons**:
  - `Download`: Export posts to JSON or CSV format
  - `Publish to WordPress`: Publish extracted posts to your WordPress site

### Workflow

1. Click a bot button (DinarGuru or DinarRecaps) to start scraping
2. Wait for extraction to complete (status indicator turns yellow during processing)
3. Review extracted posts in the display area
4. Either:
   - Download posts using the Download dropdown (JSON/CSV)
   - Publish posts to WordPress

### WordPress Publishing

The WordPress bot publishes to `investmentindicator.com` by default. On first run:

1. A Chrome browser window will open
2. Log in to WordPress manually (you have up to 5 minutes)
3. The bot will detect successful login and begin publishing
4. Posts are published sequentially with error handling

## Module Details

### app.py
Main application with CustomTkinter GUI. Handles:
- Window layout and theming
- Button callbacks with threading
- Status management
- Post display rendering

### dinar_guru_bot.py
Scrapes posts from https://www.dinarguru.com/
- Uses Selenium for dynamic content loading
- BeautifulSoup for HTML parsing
- Regex-based post extraction

### dinar_recaps_bot.py
Scrapes posts from https://dinarrecaps.com/our-blog
- Metadata extraction (title, date, link)
- Full content fetching for each post
- Date filtering support

### word_press_bot.py
Automates WordPress post creation:
- Uses undetected-chromedriver for bot protection bypass
- Persistent Chrome profile for session management
- TinyMCE editor integration
- Error recovery mechanisms

### utils.py
Utility functions:
- `get_downloads_dir()`: Get OS downloads folder path
- `download_json()`: Export posts to JSON format
- `download_csv()`: Export posts to CSV format

## Building Executable

To create a standalone executable:

### Using PyInstaller directly:
```bash
pyinstaller DinarGuruBot.spec
```

### Using the build notebook:
Open `build.ipynb` in Jupyter and run all cells.

The compiled executable will be available in the `dist/` folder.

## Dependencies

| Package | Purpose |
|---------|---------|
| customtkinter | Modern GUI framework |
| selenium | Browser automation |
| webdriver-manager | Automatic ChromeDriver management |
| beautifulsoup4 | HTML parsing |
| undetected-chromedriver | Anti-detection browser automation |

## Technical Notes

- **Python Version**: 3.12+
- **Browser**: Chrome (automatically managed by webdriver-manager)
- **Platform**: Cross-platform (Windows/Linux/macOS)
- **Architecture**: Modular design with separate concerns for scraping, publishing, and UI

## Data Format

### Extracted Post Structure
```json
{
  "number": 1,
  "date": "2024-01-15",
  "title": "Post Title",
  "content": "<p>HTML content...</p>"
}
```

### Export Formats
- **JSON**: Full structured data with all fields
- **CSV**: Tabular format with columns: number, date, title, content

## Troubleshooting

### Chrome Driver Issues
The application uses `webdriver-manager` to automatically download and manage ChromeDriver. Ensure you have a stable internet connection on first run.

### WordPress Login Timeout
If the 5-minute login window expires, restart the WordPress publishing process.

### Scraping Failures
Website structure changes may break scrapers. Check console output for error details.

## License

This project is for educational and personal use only. Ensure compliance with website terms of service when scraping.

## Disclaimer

This tool is designed for legitimate content aggregation purposes. Users are responsible for ensuring their use complies with applicable laws and website terms of service.
