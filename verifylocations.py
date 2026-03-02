import re
from playwright.sync_api import sync_playwright # type: ignore
from dataclasses import dataclass, asdict, field
import pandas as pd # type: ignore
import os
import sys

@dataclass
class Entry:
    name: str

def read_excel(file_path):
    df = pd.read_excel(file_path)
    entries = [Entry(row['name']) for index, row in df.iterrows()]
    return entries

def search_in_google_maps(page, entry):
    page.goto("https://maps.google.com")
    page.locator('//input[@id="searchboxinput"]').fill(entry.name)
    page.keyboard.press("Enter")

def main():
    # Set the file path directly here
    file_path = 'data.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)

    entries = read_excel(file_path)
    
    try:
        start_row = int(input("Enter the starting row number (minus one to account for header): "))
        if start_row < 1 or start_row > len(entries):
            raise ValueError("Invalid row number.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        for entry in entries[start_row-1:]:
            search_in_google_maps(page, entry)
            while True:
                user_input = input("Press 'n' to move to the next entry: ")
                if user_input.strip().lower() == 'n':
                    break
        browser.close()
        print("List Finished")

if __name__ == "__main__":
    main()
