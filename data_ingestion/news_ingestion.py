import schedule
import time
import subprocess

def run_news_ingestion():
    print("Running news ingestion script...")
    subprocess.run(["python", "news_scraper.py"])  # Replace with your script name

# Schedule the job to run every hour
schedule.every(1).hours.do(run_news_ingestion)

print("Scheduler started. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to prevent excessive CPU usage
