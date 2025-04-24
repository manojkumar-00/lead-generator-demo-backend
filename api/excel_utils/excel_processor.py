import pandas as pd
import os

def process_excel_file(file_path):

    try:
        # Determine file type by extension
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension in ['xlsx', 'xls']:
            # Read Excel file
            df = pd.read_excel(file_path)
        elif file_extension == 'csv':
            # Read CSV file
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Try to find the column containing company names
        # Common column names for company data
        possible_company_columns = ['company', 'company name', 'organization', 'business', 'firm', 'corporation']
        
        # Try to find a matching column (case-insensitive)
        company_column = None
        for col in df.columns:
            if col.lower() in possible_company_columns:
                company_column = col
                break
        
        # If we didn't find a specific company column, use the first column
        if company_column is None:
            company_column = df.columns[0]
            
        # Extract company names from the identified column
        companies = df[company_column].dropna().unique().tolist()
        
        # Clean up the companies list (remove duplicates and empty values)
        companies = [company.strip() for company in companies if company and isinstance(company, str)]
        companies = list(filter(None, companies))
        
        return companies
    except Exception as e:
        # Log error for debugging
        print(f"Error processing Excel file: {str(e)}")
        raise e
