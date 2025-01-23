import pandas as pd
from faker import Faker
import random

fake = Faker()

# Predefined niche-to-column mappings
NICHE_TEMPLATES = {
    "job_candidates": ["job_role", "years_experience", "salary", "skills", "education_level", "application_date"],
    "medical_sales": ["product_name", "quantity_sold", "unit_price", "sales_region", "salesperson_id", "sale_date"],
    "real_estate": ["property_type", "square_feet", "price", "bedrooms", "listing_date", "zip_code"],
    "default": ["id", "name", "value", "date", "category", "status"]  # Fallback for unknown niches
}

# Data generators for specific columns
COLUMN_GENERATORS = {
    # Job Candidates
    "job_role": lambda rows: [fake.job() for _ in range(rows)],
    "years_experience": lambda rows: [random.randint(0, 20) for _ in range(rows)],
    "salary": lambda rows: [round(random.uniform(30000, 150000), 2) for _ in range(rows)],
    "education_level": lambda rows: [random.choice(["Bachelor's", "Master's", "PhD"]) for _ in range(rows)],
    
    # Medical Sales
    "product_name": lambda rows: [fake.word() + " Capsule" for _ in range(rows)],
    "sales_region": lambda rows: [fake.state() for _ in range(rows)],
    
    # Default
    "date": lambda rows: [fake.date_this_year() for _ in range(rows)],
}

def get_columns_for_niche(niche):
    """Get relevant column names based on niche."""
    niche_key = niche.lower().replace(" ", "_")
    for template in NICHE_TEMPLATES:
        if template in niche_key:  # Partial match (e.g., "sales" in "medical_sales")
            return NICHE_TEMPLATES[template]
    return NICHE_TEMPLATES["default"]

def generate_data_for_column(col_name, rows):
    """Generate realistic data for a column based on its name."""
    if col_name in COLUMN_GENERATORS:
        return COLUMN_GENERATORS[col_name](rows)
    
    # Fallback logic based on column name keywords
    if "date" in col_name:
        return [fake.date_this_year() for _ in range(rows)]
    elif "price" in col_name or "salary" in col_name:
        return [round(random.uniform(10, 10000), 2) for _ in range(rows)]
    elif "id" in col_name:
        return [fake.uuid4() for _ in range(rows)]
    elif "name" in col_name:
        return [fake.word() for _ in range(rows)]
    else:
        return [fake.random_int(1, 100) for _ in range(rows)]

def main():
    niche = input("niche name :- ").strip()
    rows = int(input("no of rows :- "))
    cols = int(input("no of columns :- "))
    
    # Get columns for the niche (trim to user's requested column count)
    columns = get_columns_for_niche(niche)[:cols]
    
    # Generate data
    data = {col: generate_data_for_column(col, rows) for col in columns}
    
    # Save to CSV
    df = pd.DataFrame(data)
    filename = f"{niche.replace(' ', '_')}-data.csv"
    df.to_csv(filename, index=False)
    print(f"\n✅ Generated '{filename}' with columns: {', '.join(columns)}")

if __name__ == "__main__":
    main()


