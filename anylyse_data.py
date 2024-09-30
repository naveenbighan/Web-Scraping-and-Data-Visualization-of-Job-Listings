import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
import re
import spacy
from spacy.matcher import PhraseMatcher
import seaborn as sns


nlp = spacy.load("en_core_web_sm")

df = pd.read_csv('new_all_cleaned.csv')

# print(df.info())

# print(df.isnull().sum())

# print(df.describe())
# print(df.describe(include=['object']))

df['Company-Name'] = df['Company-Name'].str.upper()

graph_dir = 'graphs'
if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)
    

color_list = [
    '#FF5733',  # Red-Orange
    '#33FFBD',  # Aqua
    '#FFC300',  # Yellow
    '#DAF7A6',  # Light Green
    '#C70039',  # Crimson
    '#900C3F',  # Dark Red
    '#581845',  # Purple
    '#1E90FF',  # Dodger Blue
    '#FF69B4',  # Hot Pink
    '#8A2BE2',  # Blue Violet
    '#00FF7F',  # Spring Green
    '#FFD700',  # Gold
    '#FF4500',  # Orange Red
    '#7FFFD4',  # Aquamarine
    '#4B0082',  # Indigo
    '#ADFF2F',  # Green Yellow
    '#FF6347',  # Tomato
    '#4682B4',  # Steel Blue
    '#32CD32',  # Lime Green
    '#FF1493'   # Deep Pink
]

plt.figure(figsize=(12, 8))
df['Title'].value_counts().head(20).plot(kind='bar',color=color_list )
plt.title("Top 20 Most Common Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Count")
plt.xticks(rotation=60)
plt.savefig(os.path.join(graph_dir, 'top_20_job_titles.png'), bbox_inches='tight')  
plt.close()  

plt.figure(figsize=(12, 8))
df['Company-Name'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Companies by Job Listings")
plt.xlabel("Company")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.savefig(os.path.join(graph_dir, 'top_10_companies.png'), bbox_inches='tight')  # Save the graph
plt.close()

df['skills_split'] = df['skills'].str.split(',')
skills_df = df.explode('skills_split')
skills_df['skills_split'] = skills_df['skills_split'].str.lower().str.strip()

plt.figure(figsize=(12, 8))
skills_df['skills_split'].value_counts().head(10).plot(kind='pie')
plt.title("Top 10 Skills in Job Listings")
plt.xlabel("Skills")
# plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.savefig(os.path.join(graph_dir, 'top_10_skills.png'), bbox_inches='tight')
plt.close()


pivot_table = pd.pivot_table(df, index='Title', columns='Company-Name', aggfunc='size', fill_value=0)

software_dev_jobs = df[df['Title'].str.contains('Software Developer', case=False, na=False)]

all_skills = software_dev_jobs['skills'].str.split(',').explode().str.strip().str.lower()

skill_counts = all_skills.value_counts()

plt.figure(figsize=(10,6))
skill_counts.head(10).plot(kind='barh', color='skyblue')
plt.title('Top 10 Skills for Software Developers',fontsize=16)
plt.xlabel('Number of Job Postings', fontsize=12)
plt.ylabel('Skills',fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.savefig( os.path.join( graph_dir, 'software_dev_skills.png'), bbox_inches='tight')


wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skill_counts)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  
plt.title('Skills Word Cloud for Software Developers')
plt.savefig( os.path.join( graph_dir, 'cloud_skills.png'), bbox_inches='tight')


def clean_experience(exp):
    if pd.isna(exp) or 'No' in exp:  # Handle missing or "No Experience" entries
        return pd.Series([None, None])
    
    exp_cleaned = exp.replace(' Yrs', '').replace('+', '').replace('-', ' ').replace('Years','').replace('to', ' ').split()
    
    exp_cleaned = [int(e) for e in exp_cleaned if e.isdigit()]
    
    if len(exp_cleaned) == 1: 
        return pd.Series([exp_cleaned[0], exp_cleaned[0]])
    elif len(exp_cleaned) == 2:  
        return pd.Series([exp_cleaned[0], exp_cleaned[1]])
    
    return pd.Series([None, None])
  
df[['Min_Experience', 'Max_Experience']] = df['Experience'].apply(clean_experience)

analyzed_data_cleaned = df.drop(columns=['Experience'])

plt.figure(figsize=(12, 6))
df['Min_Experience'].value_counts().head(10).plot(kind='bar',  color='skyblue', edgecolor='black')
plt.title('Distribution of Minimum Experience')
plt.xlabel('Minimum Experience (Years)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(graph_dir, 'distribution_min_experience.png'), bbox_inches='tight')
plt.show()


plt.figure(figsize=(12, 6))
df['Max_Experience'].value_counts().head(10).plot(kind='bar',  color='skyblue', edgecolor='black')
plt.title('Distribution of Maximum Experience')
plt.xlabel('Maximum Experience (Years)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(graph_dir, 'distribution_max_experience.png'), bbox_inches='tight')
plt.show()


cities_list = [
    'Bengaluru', 'Hyderabad', 'Delhi', 'Gurugram', 'Pune', 
    'Noida', 'Mumbai', 'Kolkata', 'Chennai', 'Remote', 'Vijayawada', 
    'Lucknow', 'Thiruvananthapuram', 'Tirupati', 'Ahmedabad', 'Mohali', 
    'Surat', 'Kochi', 'Jaipur', 'Belgaum', 'Hubli', 'Bhopal', 
    'Coimbatore', 'Jalandhar', 'Patna', 'Indore', 'Thane', 'Chandigarh',
    'Sainikpuri','Arakkonam','Malappuram','Adyar','Tirunelveli','Nagpur',
    'Ranchi','Roorkee','Visakhapatnam','Amritsar','Jabalpur','Raipur','Jaipur',
    'Jammu','Srinagar','Kota','Udaipur','Phagwara ','Trivandrum','Bareilly','Nagercoil'
    
]

matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
patterns = [nlp(city) for city in cities_list]
matcher.add("Cities", None, *patterns)

replace_dict = {
    r",Other": "Bengaluru",   # Comma replacement
    r"\+": " ",               # Escape '+' in regex
    r"-": " ",                # Hyphen replacement
    r"India": "Remote",       # Replace 'India' with 'Remote'
    r"All India": "Gurugram", # Replace 'All India'
    r"/": " ",                # Replace '/' with space
    r"\(": " ",               # Escape '('
    r"\)": " ",               # Escape ')'
    r"Hybrid": "Bengaluru"
}

def clean_and_extract_cities(location):
    location_cleaned = location.lower().strip()

    for key, value in replace_dict.items():
        try:
            location_cleaned = re.sub(re.escape(key), value, location_cleaned)
        except re.error as e:
            print(f"Regex error with pattern {key}: {e}")
            continue

    cities_in_location = re.split(r'[\s,/]+', location_cleaned)
    
    location_found = set()
    for city in cities_in_location:
        doc = nlp(city.strip())
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            location_found.add(span.text.title())

    if len(location_found) > 1:
        return 'All Metro City'
    
    return location_found.pop() if location_found else 'Remote'

df['Locations'] = df['Location'].apply(lambda x: clean_and_extract_cities(str(x)))

df['Locations'] = df['Locations'].replace('', 'Unknown').fillna('Remote')

empty_locations = df[df['Locations'] == 'Remote']
if not empty_locations.empty:
    print("Rows with empty or unrecognized Locations:")
    print(empty_locations[['Location', 'Locations']])



plt.figure(figsize=(10, 6))
df['Locations'].value_counts().head(10).plot(kind='bar',  color='skyblue', edgecolor='black')
plt.title('Frequency of Cities', fontsize=16)
plt.xlabel('City', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=60, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(graph_dir, 'top-10-cities-.png'), bbox_inches='tight')
plt.show()


bengaluru_jobs = df[df['Locations'].str.contains('Bengaluru', case=False, na=False)]

job_counts = bengaluru_jobs['Title'].value_counts().nlargest(10) 

plt.figure(figsize=(10, 6))
sns.barplot(x=job_counts.values, y=job_counts.index, palette='Blues_d')
plt.title('Top 10 Jobs in Bengaluru')
plt.xlabel('Number of Jobs')
plt.ylabel('Job Titles')
plt.tight_layout()
plt.savefig(os.path.join(graph_dir, 'bengaluru-top-10-jobs.png'), bbox_inches='tight')
plt.show()


bengaluru_jobs = df[df['Locations'].str.contains('Remote', case=False, na=False)]

job_counts = bengaluru_jobs['Title'].value_counts().nlargest(10) 

plt.figure(figsize=(10, 6))
sns.barplot(x=job_counts.values, y=job_counts.index, palette='Blues_d')
plt.title('Top 10 Jobs in Remote')
plt.xlabel('Number of Jobs')
plt.ylabel('Job Titles')
plt.tight_layout()
plt.savefig(os.path.join(graph_dir, 'Remote-top-10-jobs.png'), bbox_inches='tight')
plt.show()

columns_to_delete = ['Location', 'Requirement', 'original-titles', 'skills_split']
df = df.drop(columns=columns_to_delete)



df.to_csv("analyzed_data.csv", index=False)


print(f"Graphs saved in the '{graph_dir}' folder.")
