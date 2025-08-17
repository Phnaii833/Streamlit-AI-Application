import pandas as pd

csv_file = "submissions.csv"

# Define headers for your CSV
columns = ["timestamp", "name", "state", "language_selected", "category", "text", "detected_lang"]

# Read CSV without headers, assign column names
df = pd.read_csv(csv_file, header=None, names=columns, encoding="utf-8-sig")

# Insert 'region' after 'state'
insert_at = df.columns.get_loc("state") + 1
df.insert(insert_at, "region", "Unknown")  # default value

# Save back CSV with UTF-8 and headers this time
df.to_csv(csv_file, index=False, encoding="utf-8-sig")
