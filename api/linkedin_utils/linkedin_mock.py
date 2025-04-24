from dotenv import load_dotenv
import os
import requests
import time
import re
import random

load_dotenv()  
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
HUNTER_API_KEY =os.getenv("HUNTER_API_KEY")

def extractNameFromURL(linkedin_url):
    name_part = linkedin_url.split("linkedin.com/in/")[-1].split("/")[0]
    name_part = name_part.replace("-", " ").replace("_", " ")
    name = ' '.join([word.capitalize() for word in name_part.split()])
    return name

def getDomainFromCompany(company_name):
    cleaned = re.sub(r'[^a-zA-Z]', '', company_name.lower())
    return f"{cleaned}.com"

def getEmail(full_name, company_domain):
    hunter_url = "https://api.hunter.io/v2/email-finder"
    first_name, *last = full_name.split()
    last_name = ' '.join(last) if last else ''

    params = {
        "domain": company_domain,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": HUNTER_API_KEY
    }

    response = requests.get(hunter_url, params=params)
    if response.status_code == 200:
        return response.json().get("data", {}).get("email")
    return None

def generate_mock_skills(designation):
    """Generate relevant skills based on designation"""
    common_skills = ["Leadership", "Strategic Planning", "Team Management", "Communication"]
    
    designation_lower = designation.lower()
    if 'market' in designation_lower:
        return common_skills + ["Digital Marketing", "Brand Strategy", "Market Research", "SEO", "Content Strategy"]
    elif 'sales' in designation_lower:
        return common_skills + ["Negotiation", "Client Relationships", "Sales Strategy", "Business Development", "CRM"]
    elif 'tech' in designation_lower or 'it' in designation_lower:
        return common_skills + ["Project Management", "Software Development", "Cloud Services", "Cybersecurity", "IT Infrastructure"]
    elif 'finance' in designation_lower:
        return common_skills + ["Financial Analysis", "Budgeting", "Forecasting", "Risk Management", "Investment Strategy"]
    elif 'hr' in designation_lower or 'human' in designation_lower:
        return common_skills + ["Recruitment", "Employee Relations", "Performance Management", "Talent Development", "Compliance"]
    else:
        return common_skills + ["Strategic Planning", "Business Analysis", "Project Management", "Innovation", "Problem Solving"]

def generate_mock_about(first_name, last_name, designation, company):
    """Generate a mock about section for the profile"""
    templates = [
        f"Experienced {designation} at {company} with a proven track record of delivering results and driving business growth.",
        f"As the {designation} at {company}, {first_name} leads strategic initiatives and fosters innovation across the organization.",
        f"Forward-thinking {designation} at {company} with expertise in building high-performing teams and optimizing operational efficiency.",
        f"{first_name} {last_name} is a seasoned {designation} at {company}, passionate about leveraging technology to solve complex business challenges.",
        f"Results-driven {designation} at {company} with a focus on sustainable growth and customer-centric strategies."
    ]

def fetchEmployeesFromCompany(company_name, role):
    query = f"site:linkedin.com/in/ {role} {company_name}"
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": "5"
    }

    response = requests.get(url, params=params)
    results = response.json().get("organic_results", [])

    domain = getDomainFromCompany(company_name)
    employee_data = []

    for res in results:
        linkedin_url = res.get("link")
        if "linkedin.com/in/" not in linkedin_url:
            continue

        # Extract raw title, e.g., "James Dolan - Sales Director - IBM"
        title = res.get("title", "")
        name = title.split(" - ")[0] if " - " in title else extractNameFromURL(linkedin_url)
        designation = " - ".join(title.split(" - ")[1:-1]) if " - " in title else role
        location = res.get("rich_snippet", {}).get("top", {}).get("extensions", [None])[0]

        # Split name if possible
        name_parts = name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else "John"
        last_name = name_parts[-1] if len(name_parts) > 1 else "Doe"

        # email = getEmail(name, domain)

        employee_data.append({
            "id": random.randint(10000, 99999),
            "name": name,
            "linkedin": linkedin_url,
            "company": company_name,
            "email": 'dummy@gmail.com',
            "designation": designation,
            "domain": domain,
            "connections": res.get('displayed_link'),
            'experience': random.randint(2, 20),
            "location": location if location else random.choice([
                "New York", "San Francisco", "Chicago", "Boston", "Seattle", "Austin", "Los Angeles"
            ]),
            "skills": generate_mock_skills(designation),
            "about": generate_mock_about(first_name, last_name, designation, company_name)
        })

        time.sleep(1.5)  # to avoid rate limiting

    return employee_data

def get_linkedin_profiles(companies, role):
    all_employees = []
    for company in companies:
        print(f"\n🔍 Processing Company: {company}")
        employees = fetchEmployeesFromCompany(company, role)
        all_employees.extend(employees)
    return all_employees


