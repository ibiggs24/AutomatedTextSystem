import csv
import os
import subprocess

SCRIPT_PATH = os.path.expanduser("~/Documents/TextAutomation/sendText.scpt")
CSV_PATH = os.path.expanduser("~/Documents/TextAutomation/contacts.csv")

# Open and read the CSV
with open(CSV_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    successCount = 0
    failCount = 0
    for row in reader:
        phone = row["Phone Number"].strip()
        message = row["SMS Message"].strip()
        attachment = row.get("attachment", "").strip()

        # Build the osascript command
        cmd = ["osascript", SCRIPT_PATH, "--to", phone]

        # Split message into lines (AppleScript handles multi-line parts)
        for line in message.split("\\n"):
            cmd.append(line.strip())

        if attachment:
            cmd.append("--attachment")
            cmd.append(attachment)

        print(f"Sending to {phone}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print("Result:", result.stdout.strip())
            successCount += 1
            if result.stderr:
                print("Error:", result.stderr.strip())
                failCount += 1
        except Exception as e:
            print(f"Failed to send to {phone}: {e}")
            failCount += 1
    print("Summary: \n Sent: " + successCount + "/" + (successCount + failCount) + " messages")
