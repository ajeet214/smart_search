"""
preprocess.py

This script reads a raw Excel file containing structured people/event/location data,
cleans the data, and generates a human-readable "TextChunk" for each row.

The output is saved to a new Excel file and used later for semantic search and embedding.

Usage:
    python scripts/preprocess.py
"""

import pandas as pd

# Define input and output file paths
input_excel_path = "D:\\LifeLongLearning\\temp\\raw\\people_data_1000.xlsx"
output_excel_path = "D:\\LifeLongLearning\\temp\\processed\\people_data_1000_with_textchunk.xlsx"

# Load the raw Excel data
df = pd.read_excel(input_excel_path)

# Standardize column names (capitalize and strip whitespace)
df.columns = [col.strip().capitalize() for col in df.columns]

# Drop any rows that contain missing values
df.dropna(inplace=True)


def row_to_text(row):
    """
    Convert a structured row to a natural-language text chunk.

    Args:
        row (pd.Series): A row containing 'People', 'Families', 'Locations', 'Events'

    Returns:
        str: A formatted sentence describing the row
    """
    return (
        f"{row['People']} is part of the {row['Families']} team, "
        f"based in {row['Locations']}, and recently "
        f"{row['Events'].lower()}."
    )


# Generate 'TextChunk' column for every row
df["Textchunk"] = df.apply(row_to_text, axis=1)

# Save the processed DataFrame to Excel
df.to_excel(output_excel_path, index=False)

print(f"✅ Processed file saved to: {output_excel_path}")
