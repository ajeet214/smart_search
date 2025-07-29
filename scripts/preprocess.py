import pandas as pd

# Define input and output file paths
input_excel_path = "D:\\LifeLongLearning\\temp\\raw\\people_data_1000.xlsx"
output_excel_path = "D:\\LifeLongLearning\\temp\\processed\\people_data_1000_with_textchunk.xlsx"

# Load the Excel file
df = pd.read_excel(input_excel_path)

# Clean and standardize column names
df.columns = [col.strip().capitalize() for col in df.columns]

# Drop rows with missing values
df.dropna(inplace=True)


# Create a descriptive TextChunk for each row
def row_to_text(row):
    return (
        f"{row['People']} is part of the {row['Families']} team, "
        f"based in {row['Locations']}, and recently "
        f"{row['Events'].lower()}."
    )


# Apply the transformation
df["TextChunk"] = df.apply(row_to_text, axis=1)

# Save the new Excel file with the additional column
df.to_excel(output_excel_path, index=False)

print(f"✅ Processed file saved to: {output_excel_path}")
