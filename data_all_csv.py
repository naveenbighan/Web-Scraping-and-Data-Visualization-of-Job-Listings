import pandas as pd
import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("all_cleaned.csv")
pd.options.display.max_rows = 50999

df['Company-Name'] = df['Company-Name'].str.upper()

title_mappings = {
    r'(?i)mechanical': 'Mechanical Engineering',
    r'(?i)electrical|electronic': 'Electrical Engineering',
    r'(?i)developer|software|python|it|ai/ml|cloud|oracle|web|linux|devops|data\s+scientist|angular|database|azure|sql|c\+\+|backend|frontend|ios|android|mongodb|iot|java|aws|node\.js|express\.js|mern|ui/ux|.NET|data|application|stack|ai|ml': 'Software Developer',
    r'(?i)business': 'Business Development',
    r'(?i)account': 'Account Manager',
    r'(?i)b2b|sales': 'Sales Manager',
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

def clean_title(title):
    if isinstance(title, str):
        for pattern, new_title in title_mappings.items():
            if re.search(pattern, title):
                return new_title
    return title

df['original-titles'] = df['Title'].str.upper()
df['Title'] = df['original-titles'].apply(clean_title)

df['salary_package'].fillna('N/A', inplace=True)
df['Timings'].fillna('N/A', inplace=True)
df['Timings'] = df['Timings'].replace("Permanent", "Full-Time")

for index, row in df.iterrows():
    if row['original-titles'] != row['Title']:  
        f" Cleaned: {row['Title']}"

skills_list = [
    "Python", "Java", "SQL", "JavaScript", "HTML", "CSS", "AWS", "Node.js", "Node", 
    "Docker", "Kubernetes", "Angular", "React", "Machine Learning", "DevOps", "Web apis",
    "Cloud", "C++", "Linux", "Git", "Agile", "Data Science", "MongoDB", "Express.js", "Express js",
    "No SQL", "Springboot", "C#", "OOPS", ".NET", "FastAPI", "PHP", "Django", "Flask", "ASP.NET", "MySQL"," Technical "
    "Jquery", "Ajax", "Laravel", "GIT", "Git", "Phalcon", "SnowSQL", "Ethernet", "PostgreSQL", "Perl", "Ruby","Product Knowledge",
    "IoT", "AI", "Github", "Data Analysis", "Digital Marketing", "Communication", "Sales", "Leadership", "Management","SaaS",
    "Event Planning", "Social Media Marketing", "Media Management", "Content Marketing", "Email Marketing", "Google Ads","Microsoft Office"
    "Interpersonal skills", "Multitasking", "MS Office", "PowerPoint", "CQF", "PRM", "MS Teams", "SAP", "TypeScript", "Cyber security",
    "Machine Learning", "Problem solving", "Project Management", "Power BI", "Statistics", "AV programming", "Tensorflow", "NLP",
    "Proposal Writing","Content Creation","Analytical","Computer","Market Research","B2B marketing","CPQ","LWC Development","Account Management",
    "Lead Generation","CRM","Negotiation","Presentation"," Market Analysis","Automation","Distribution","Customer Service","MIS Management",
    "Technical Support","Security domain","Real Estate","Enterprise sales ","Relationship Management","Business Development","Distribution",
    "Industrial Sales","Cybersecurity","Supply Chain","Journalism","Content writing","Marketing","Creativity"
]

matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
patterns = [nlp(skill) for skill in skills_list]
matcher.add("Skills", None, *patterns)

def extract_skills(requirement):
    doc = nlp(requirement)
    matches = matcher(doc)
    skills_found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills_found.add(span.text)
    return ', '.join(skills_found) if skills_found else 'N/A'

df['skills'] = df['Requirement'].apply(lambda x: extract_skills(str(x)))


df.to_csv("new_all_cleaned.csv", index=False, encoding='utf-8-sig')
