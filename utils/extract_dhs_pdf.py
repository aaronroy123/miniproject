"""
DHS Kerala PDF Extractor
Extracts district-wise waterborne disease data from DHS Kerala IDSP Annual Reports.

Waterborne diseases extracted:
- ADD / Diarrhoea (most common waterborne disease in Kerala)
- Leptospirosis
- Hepatitis A
- Typhoid
- Cholera

Output: data/disease_cases_real.csv with columns:
    year, district, waterborne_cases
"""

import pdfplumber
import pandas as pd
import re

# District name mapping: abbreviation → full name matching our app's DISTRICTS dict
DISTRICT_MAP = {
    "TRIVANDRUM": "Thiruvananthapuram",
    "TVM": "Thiruvananthapuram",
    "KOLLAM": "Kollam",
    "KLM": "Kollam",
    "PATHANAMTHITTA": "Pathanamthitta",
    "PTA": "Pathanamthitta",
    "IDUKKI": "Idukki",
    "IDK": "Idukki",
    "KOTTAYAM": "Kottayam",
    "KTM": "Kottayam",
    "ALAPPUZHA": "Alappuzha",
    "ALP": "Alappuzha",
    "ERNAKULAM": "Ernakulam",
    "EKM": "Ernakulam",
    "THRISSUR": "Thrissur",
    "TSR": "Thrissur",
    "PALAKKAD": "Palakkad",
    "PKD": "Palakkad",
    "MALAPPURAM": "Malappuram",
    "MLP": "Malappuram",
    "KOZHIKODE": "Kozhikode",
    "KKD": "Kozhikode",
    "WAYANAD": "Wayanad",
    "WYD": "Wayanad",
    "KANNUR": "Kannur",
    "KNR": "Kannur",
    "KASARAGOD": "Kasaragod",
    "KSD": "Kasaragod",
}

# Diseases we consider as waterborne (fragments for robust matching)
WATERBORNE_DISEASES = [
    "ADD", "Diarrhoea", "Diarrhea",
    "Lepto", "Spirosis",  # Matches Leptospirosis/Lepto
    "Hepa", "Hepatitis",
    "Typhoid",
    "Cholera",
    "Shigella",
]


def extract_district_data_from_pdf(pdf_path, year):
    """
    Extracts district-wise waterborne disease data from a DHS Kerala PDF.
    Strategy: Pages 6+ have one district per page (district name is the first table header).
    Each page has a table with disease name + cases + deaths.
    """
    records = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"\n  PDF has {len(pdf.pages)} pages")

        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = page.extract_tables()

            # Try to identify the district from the page text
            district = None
            for line in text.split("\n"):
                line_clean = line.strip().upper()
                if line_clean in DISTRICT_MAP:
                    district = DISTRICT_MAP[line_clean]
                    break

            if district is None:
                continue  # Not a district page

            print(f"  Page {page_num+1}: Found district = {district}")

            # Now extract waterborne disease cases from the table on this page
            total_waterborne = 0

            for table in tables:
                for row in table:
                    if not row or len(row) < 3:
                        continue

                    # Row format: [sl_no, disease_name, None, cases, deaths]
                    # Find the disease name column (index 1)
                    disease_cell = row[1] if row[1] else (row[2] if len(row) > 2 else "")
                    if not disease_cell:
                        continue

                    disease_name = str(disease_cell).strip()

                    # Check if this matches a waterborne disease
                    disease_match = False
                    for wb_disease in WATERBORNE_DISEASES:
                        if wb_disease.lower() in disease_name.lower():
                            disease_match = True
                            break

                    if disease_match:
                        # Find the cases value (search all columns after the disease name)
                        cases_val = None
                        # Strategy: Look for the first integer found in the row after current disease cell
                        # Usually cases are in the next 1-3 columns
                        for col_val in row[2:]:
                            if col_val:
                                try:
                                    clean = str(col_val).replace("*", "").replace(",", "").strip()
                                    if clean.isdigit() or (clean.lstrip("-").isdigit()):
                                        val = int(clean)
                                        if val > 0:
                                            cases_val = val
                                            break
                                except:
                                    pass

                        if cases_val is not None:
                            print(f"    {disease_name}: {cases_val} cases")
                            total_waterborne += cases_val

            if total_waterborne > 0:
                records.append({
                    "year": year,
                    "district": district,
                    "waterborne_cases": total_waterborne
                })

    return records


def process_multiple_years(pdf_files_by_year):
    """
    Process multiple PDFs and combine into one DataFrame.
    pdf_files_by_year: dict of {year: pdf_path}
    """
    all_records = []

    for year, pdf_path in sorted(pdf_files_by_year.items()):
        print(f"\n{'='*50}\nProcessing year {year}: {pdf_path}\n{'='*50}")
        try:
            records = extract_district_data_from_pdf(pdf_path, year)
            print(f"  Extracted {len(records)} district records")
            all_records.extend(records)
        except Exception as e:
            print(f"  ERROR: {e}")

    return pd.DataFrame(all_records)


if __name__ == "__main__":
    import os

    # Local PDF storage directory
    base_dir = r"d:\waterborne-disease-ai\data\dhs_pdfs"
    pdf_files = {year: os.path.join(base_dir, f"cd_data_{year}.pdf") 
                 for year in range(2013, 2024)}

    print(f"Extracting genuine Kerala DHS disease data ({min(pdf_files.keys())}-{max(pdf_files.keys())})...")
    df = process_multiple_years(pdf_files)

    if df.empty:
        print("\n⚠ No data extracted. Check PDF structure.")
    else:
        print(f"\n✅ Extracted {len(df)} records total")
        print(df.to_string())

        # Save to the project data folder
        out_path = r"d:\waterborne-disease-ai\data\disease_cases_real.csv"
        df.to_csv(out_path, index=False)
        print(f"\n💾 Saved to: {out_path}")
