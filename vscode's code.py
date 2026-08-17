import pandas as pd
import time

from pathlib import Path

file_path = Path(_file_).parent / "2019-Nov.csv"
chunk_size = 500000

print("Starting pandas processing...")
print(f"Chunk size: {chunk_size:,} rows")

all_category_counts = []

total_rows = 0
rows_with_category = 0

# Store missing value counts
missing_values = None

# Start total execution timer
total_start = time.time()

for chunk_number, chunk in enumerate(
    pd.read_csv(file_path, chunksize=chunk_size),
    start=1
):
    total_rows += len(chunk)



    # Remove duplicate records within the current chunk
    chunk = chunk.drop_duplicates()

    # Check missing values in each chunk
    chunk_missing = chunk.isnull().sum()

    if missing_values is None:
        missing_values = chunk_missing
    else:
        missing_values = missing_values.add(
            chunk_missing,
            fill_value=0
        )

    # Remove rows with missing category_code
    chunk = chunk.dropna(subset=["category_code"])

    rows_with_category += len(chunk)

    # Count category frequency in each chunk
    chunk_counts = chunk["category_code"].value_counts()

    all_category_counts.append(chunk_counts)

    print(
        f"Chunk {chunk_number} completed - "
        f"{total_rows:,} rows read"
    )

print("\nAll chunks have been processed.")
print("\nMissing values:")
print(missing_values.astype(int))


# Combine the category counts from all chunks
category_counts = (
    pd.concat(all_category_counts)
    .groupby(level=0)
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

category_counts.columns = ["category_code", "count"]

# End total execution timer
total_end = time.time()

print("\nNumber of unique categories:")
print(len(category_counts))

print("\nCategory frequency:")
print(category_counts.to_string(index=False))


print(
    f"Total pandas execution time: "
    f"{total_end - total_start:.3f} seconds"
)

print(f"Total rows read: {total_rows:,}")
print(f"Rows used in category analysis: {rows_with_category:,}")
