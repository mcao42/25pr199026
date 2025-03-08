#!/usr/bin/env python3
import glob
import sys
import re
import datetime
from bs4 import BeautifulSoup

# Function to extract timestamp from filename
def extract_timestamp(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}Z)', filename)
    if match:
        # Convert the timestamp string to a datetime object for sorting
        timestamp_str = match.group(1)
        # Replace underscores with colons for proper datetime parsing
        timestamp_str = timestamp_str.replace('_', ':').replace('Z', '')
        return datetime.datetime.fromisoformat(timestamp_str)
    return datetime.datetime.min  # Default for files without timestamp

# Get all files matching the patterns
files = glob.glob("Group*.html") + glob.glob("**/*Text*.html", recursive=True)

# Sort files by timestamp in the filename
files.sort(key=extract_timestamp)

# Process files in chronological order
for filename in files:
    try:
        # Print the filename as a header
        print(f"{filename}:")
        
        with open(filename, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
            # Extract group conversation participants if present
            participants_div = soup.find('div', class_='participants')
            if participants_div:
                print(participants_div.get_text(strip=True))
            
            # Extract each message
            for message_div in soup.find_all('div', class_='message'):
                # Extract timestamp
                timestamp = message_div.find('abbr', class_='dt')['title']
                
                # Extract sender - handle "Me" case
                sender_elem = message_div.find('cite', class_='sender')
                if sender_elem.find('abbr', class_='fn', title=''):
                    sender = "Me"
                else:
                    sender = sender_elem.get_text(strip=True)
                
                # Extract message content - handle <br> tags
                q_elem = message_div.find('q')
                for br in q_elem.find_all('br'):
                    br.replace_with(' ')
                message = q_elem.get_text(strip=True)
                
                # Print in the requested format
                print(f"{timestamp}: {sender}: {message}")
            
            print()  # Add blank line between files
    except Exception as e:
        print(f"Error processing {filename}: {e}", file=sys.stderr)

