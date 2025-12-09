"""
Browser Profile Approach - Reuses your existing Chrome profile with saved login session.

FIRST TIME SETUP:
1. Run this script once
2. Manually log into investmentindicator.com in the browser that opens
3. Check "Remember Me" when logging in
4. Close the browser
5. Run the script again - you'll be automatically logged in!
"""

import undetected_chromedriver as uc
import os

# Path to store the browser profile (persists cookies/sessions)
PROFILE_DIR = os.path.expanduser("~/Desktop/DinarGuru/Working/chrome_profile")

# Create profile directory if it doesn't exist
os.makedirs(PROFILE_DIR, exist_ok=True)

# Create undetected Chrome driver with persistent profile
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={PROFILE_DIR}")

driver = uc.Chrome(options=options, version_main=142)

# Navigate directly to wp-admin (will redirect to login if not authenticated)
driver.get("https://investmentindicator.com/wp-admin/post-new.php")

# If this is the first run, you'll see the login page - log in manually
# On subsequent runs, you'll be automatically logged in via saved cookies
print("Browser opened!")
print(f"Profile saved at: {PROFILE_DIR}")
print("If you see login page, log in manually with 'Remember Me' checked.")
print("Next time, you'll be auto-logged in.")

