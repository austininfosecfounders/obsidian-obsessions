#!/Users/pedram/venv3-20241001/bin/python3

"""
This script is designed to ingest self-texts from your iMessage history into a local Markdown file.
URLs will be fetched and processed into separate files in the specified content directory.
Newest notes to self will appear at the top of the Notes to Self.md file.

Note that the above Python interpreter has been authorized for full disk access, which actually maps to this binary:

/opt/homebrew/Cellar/python@3.12/3.12.3/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/

If the Python environment is changed, the binary will change, and this script will stop working.
"""

import os
import sqlite3
import requests
import subprocess
import datetime

from concurrent.futures import ThreadPoolExecutor

MY_NUMBER   = "+1xxxxxxxxxx"
CONTENT_DIR = "/Users/pedram/Pedsidian/Content Farm/Web"
NOTES2SELF  = "/Users/pedram/Pedsidian/Notes to Self.md"
MODEL       = "gpt-4o-2024-08-06"
DEBUG       = os.getenv("DEBUG", True)

# Executes the fabric command with the specified pattern and returns the stdout.
def execute_fabric_command (content, pattern_name):
    try:
        fabric_command = ["fabric", "--pattern", pattern_name, "--model", MODEL]
        process = subprocess.Popen(fabric_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=content)

        if process.returncode != 0:
            raise Exception(f"Error running fabric command: {stderr}")

        return stdout

    except Exception as e:
        raise Exception(f"An error occurred while processing the content: {e}")

# Takes an Apple News URL and follows the redirect to return the actual URL.
def get_actual_url (apple_news_url):
    try:
        # Follow the redirect from the Apple News URL
        response = requests.get(apple_news_url, allow_redirects=True)

        # Check if the request was successful
        if response.status_code == 200:
            # The final URL after all redirects
            return response.url

        else:
            print(f"Failed to resolve the URL. Status code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Helper function to write a note to self to the markdown file if that note doesn't already exist.
def note_to_self (message, iso8601):
    with open(NOTES2SELF, "r") as f:
        content = f.read()

    # Check if the message already exists
    if f"{iso8601}: {message}" in content:
        if DEBUG:
            print(f"Note already exists: {iso8601}: {message}")

        return

    # Prepare the new note
    new_note = f"{iso8601}: {message}\n\n"

    # Add the new note at the beginning of the content
    updated_content = new_note + content

    # Write the updated content back to the file
    with open(NOTES2SELF, "w") as f:
        f.write(updated_content)

    if DEBUG:
        print(f"Added new note: {iso8601}: {message}")

# Helper function to get the content of a web page via jina.ai service.
def web_get (url):
    if "apple.news" in url.lower():
        url = get_actual_url(url)

        if DEBUG:
            print(f"Actual URL: {url}")

    wrapped_url = f"https://r.jina.ai/{url}"

    return requests.get(wrapped_url).text

# Path to the Messages database on macOS
# NOTE: Requires Full Disk Access to be enabled for this binary.
db_path = os.path.expanduser("~/Library/Messages/chat.db")

# Connect to the database
try:
    conn   = sqlite3.connect(db_path)
    cursor = conn.cursor()

except sqlite3.OperationalError as e:
    print(f"Error: Unable to access the Messages database. {e}")
    print("This script may not have the necessary permissions to access the Messages directory.")
    print("Please ensure you have the required permissions or try running the script with elevated privileges.")
    print("If you have not granted full disk access to this Python binary, you will need to do so by following these steps:")
    print("  1. Open 'System Preferences' > 'Security & Privacy' > 'Full Disk Access'.")
    print("  2. Click the '+' button and select 'Python.app' from the list.")
    print("3. Relaunch the script.")
    exit(1)

# Query to fetch messages sent to yourself over the past 24 hours.
query = f"""
    SELECT
        date,
        datetime(message.date / 1000000000 + 978307200, 'unixepoch', 'localtime') AS iso8601,
        message.text
    FROM
        message
    JOIN
        handle ON message.handle_id = handle.ROWID
    WHERE
        handle.id = '{MY_NUMBER}'
        AND message.is_from_me = 0
        AND message.date > (strftime('%s', 'now') - 86400) - 978307200
    ORDER BY
        message.date DESC
"""

try:
    cursor.execute(query)

    # Convert results to dictionaries from of array.
    messages = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()

for msg in messages:
    # Skip over empty messages.
    if not msg['text']:
        continue

    # Remove newlines from the message.
    message = msg['text'].replace("\n", " ")

    if DEBUG:
        print(f"{msg['iso8601']}: {message}")

    if not message.lower().startswith("http"):
        print("Not a URL, processing as note to self...")
        note_to_self(message, msg['iso8601'])
        continue

    # Message is actually a URL, so fetch the content.
    url     = message
    content = web_get(url)

    if "Open this story in Apple News." in content:
        print("Unable to retrieve original content from Apple News URL, skipping...")
        continue

    if DEBUG:
        print(f"Fetched {len(content)} characters of content from {url}")

    # Execute Fabric patterns in parallel.
    with ThreadPoolExecutor() as executor:
        print("Generating sitrep, summary, and slug...")
        futures = [executor.submit(execute_fabric_command, content, cmd) for cmd in ["ped_sitrep", "ped_summarize", "ped_slugify"]]
        sitrep, summary, slug = [f.result() for f in futures]
        print("Fabric commands completed.")

    # Create the filename using the current date and the generated slug
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename     = f"{current_date}-{slug.strip()}.md"
    filepath     = os.path.join(CONTENT_DIR, filename)

    # Check if the file already exists
    if os.path.exists(filepath):
        print(f"File {filename} already exists. Skipping...")
        continue

    # Create the content for the markdown file
    md_content = f"""{url}

# ped_sitrep

{sitrep}

# summarize

{summary}
"""

    # Write the content to the file
    with open(filepath, "w") as f:
        f.write(md_content.strip())

    print(f"Created file: {filename}")
