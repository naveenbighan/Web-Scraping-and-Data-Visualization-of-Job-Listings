import pandas as pd
import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
# Load data
df = pd.read_csv("all_cleaned.csv")
pd.options.display.max_rows = 50999

# Title mapping dictionary
title_mappings = {
    r'(?i)mechanical\s+engineer': 'Mechanical Engineering',
    r'(?i)electrical\s+engineer': 'Electrical Engineering',
    r'(?i)developer|software|python|application|it|ai/ml|data engineer|cloud|oracle|saas|machine|web|linux|devops|data scientist|Angular|Database|Generative|Computer|Azure|Development|AI|UI UX|data|sql|c++|Technology|Artificial Intelligence|Backend|frontend|ODOO|iOS|android|MongoDB|Internet of Things|iot|java|aws|Firmware|Node.js|express.js|mern|UI/UX': 'Software Developer',
    r'(?i)business': 'Business Development',
    r'(?i)account manager': 'Account Manager',
    r'(?i)b2b': 'Sales Manager',
    r'(?i)automation': 'Automation Engineering',
    r'(?i)piping': 'Piping Engineering',
    r'(?i)product': 'Product Engineer',
    r'(?i)site': 'Site Engineer',
    r'(?i)test': 'Testing Engineer',
    r'(?i)engineering operations|abroad|systems': 'Engineering Operations',
    r'(?i)network': 'Network Engineer',
    r'(?i)project': 'Project Manager',
    r'(?i)process': 'Process Engineer',
    r'(?i)technical': 'Technical Engineer',
    r'(?i)supply chain': 'Supply-Chain Engineer',
    r'(?i)structural': 'Structural Engineer',
    r'(?i)lead': 'Lead Operator',
    r'(?i)staff': 'Staff Engineer',
    r'(?i)industrial|hardware|operations': 'Operation Engineer',
    r'(?i)support': 'Support Engineer',
    r'(?i)ping': 'Ping Engineer',
    r'(?i)principal': 'Principal Engineer',
    r'(?i)ci/cd': 'Software Developer',
    r'(?i)electronics': 'Electronics Engineer',
    r'(?i)sap': 'Product Manager',
    r'(?i)analytics': 'Software Developer',
    r'(?i)program': 'Program Manager',
    r'(?i)assistant': 'Assistant',
    r'(?i)accountant': 'Accountant',
    r'(?i)director|hod': 'Director',
    r'(?i)interior': 'Interior Designer',
    r'(?i)finance': 'Finance Manager',
    r'(?i)iam': 'IAM Implementation Specialist',
    r'(?i)manager': 'Manager',
    r'(?i)tax': 'Tax Analyst',
    r'(?i)administrator': 'System Administrator',
    r'(?i)silicon': 'Silicon Engineer',
    r'(?i)draftsman': 'Draftsman',
    r'(?i)banking': 'Banking Professional',
    r'(?i)human': 'Human Resource',
    r'(?i)pipeline': 'Pipeline Engineer',
    r'(?i)associate': 'Associate',
    r'(?i)coordinator': 'Coordinator',
    r'(?i)planning': 'Planning Engineer',
    r'(?i)specialist': 'Specialist',
    r'(?i)delivery': 'Delivery Specialist',
    r'(?i)automobile': 'Automobile Engineer',
    r'(?i)fp&a': 'FP&A Specialist',
    r'(?i)instrumentation': 'Instrumentation Engineer',
}

# Function to clean the title using the dictionary
def clean_title(title):
    if isinstance(title, str):
        for pattern, new_title in title_mappings.items():
            if re.search(pattern, title):
                return new_title
    return title

# Create new columns for original and cleaned titles
df['original-titles'] = df['Title']
df['Title'] = df['original-titles'].apply(clean_title)

df['salary_package'].fillna('N/A', inplace=True)
df['Timings'].fillna('N/A', inplace=True)
df['Timings'] = df['Timings'].replace("Permanent", "Full-Time")

for index, row in df.iterrows():
    if row['original-titles'] != row['Title']:  
          f"Original: {row['original-titles']} -> Cleaned: {row['Title']}"
skills_list = [
    "Python", "Java", "SQL", "JavaScript", "HTML", "CSS", "AWS", "Node.js", 
    "Docker", "Kubernetes", "Angular", "React", "Machine Learning", "DevOps",
    "Cloud", "C++", "Linux", "Git", "Agile", "Data Science", "MongoDB"
]

# Use PhraseMatcher to find skill-related keywords in the requirements
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(skill) for skill in skills_list]
matcher.add("Skills", None, *patterns)

# Function to extract skills from requirements
def extract_skills(requirement):
    doc = nlp(requirement)
    matches = matcher(doc)
    skills_found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills_found.add(span.text)
    return ', '.join(skills_found) if skills_found else 'N/A'

# Apply the function to the 'Requirement' column and store in 'skills' column
df['skills'] = df['Requirement'].apply(lambda x: extract_skills(str(x)))


# df.drop(columns=['Requirement'], inplace=True)



# Print the updated dataframe
print(df[['skills']].head(50))       



# df.to_csv("new_csv_title.csv", index=False, encoding='utf-8-sig')
