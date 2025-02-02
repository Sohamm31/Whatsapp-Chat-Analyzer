import re
import pandas as pd

def preprocessor(data):
    def convert_whatsapp_format(data):
        # Regular expression to match the original format
        pattern = r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)"
        # Replace with the new format
        converted_text = re.sub(pattern, r"\1 - \2: \3", data)
        return converted_text

    # Convert the original data to a new format
    data = convert_whatsapp_format(data)

    # Regex to capture date, time, sender, and message
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\s-\s([^:]+):\s(.*)"

    # Initialize lists for date-time and sender-message
    date_time_list = []
    sender_message_list = []

    # Process the text line by line
    for line in data.split('\n'):
        # Apply regex only on non-empty lines
        if line.strip():
            matches = re.findall(pattern, line)
            if matches:
                # Extract and store date-time and sender-message pairs
                for match in matches:
                    date_time_list.append(f"{match[0]}, {match[1]}")
                    sender_message_list.append(f"{match[2]}: {match[3]}")

    # Create DataFrame from the extracted data
    df = pd.DataFrame({"User Messages": sender_message_list, "Messages_date": date_time_list})

    # Convert 'Messages_date' to datetime
    df["Messages_date"] = pd.to_datetime(df["Messages_date"], format="%d/%m/%y, %H:%M:%S")

    # Rename 'Messages_date' column to 'date'
    df.rename(columns={"Messages_date": "date"}, inplace=True)

    # Extract 'Username' and 'Message' columns
    df['Username'] = df['User Messages'].str.extract(r"([^:]+):")  # Extract username (sender)
    df['Message'] = df['User Messages'].str.extract(r":\s*(.*)")  # Extract message

    # Select the necessary columns
    df = df[["date", "Username", "Message"]]

    # Extract additional time components
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    return df
