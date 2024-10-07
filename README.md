# Project Title: Web Scraping and Data Visualization of Job Listings

# Description:

This project is a comprehensive tool for extracting, analyzing, and visualizing job listings data. It combines two major components:

# Job Listings Scraper from Major Job Portals:

Scrapes job listings from various portals like Indeed, Naukri.com, Shine.com, and Foundit.
Collects key information such as job title, company name, location, skills, and experience.
Merges data from different sources into a single master dataset.
Cleans and preprocesses the data, preparing it for analysis.

# Job Data Visualization and Filtering with Flask:

A Flask-based web application connected to MongoDB for storing and querying job listings.
Users can filter job listings by job title and location.
The application generates bar charts to visualize the top 10 distributions of key columns such as job skills, minimum experience, maximum experience, and company names.
All visualizations are generated dynamically using Matplotlib, and the results are displayed on the web interface.

# Technologies Used:

Python: For web scraping, data cleaning, and processing.
Flask: To build the web application for user interaction and data visualization.
MongoDB: As a database to store and retrieve the job listing data.
Matplotlib: For generating charts and visualizations.
Pandas: For data manipulation and analysis.
Selenium: For web scraping automation across multiple job sites.


This project enables users to easily explore and visualize job data, offering insights into the skills, experience, and companies prevalent in the job market


































# project data Anaylisis of Job listing

Data Cleaning & Processing: used pandas to clean and manipulate the data from a CSV file containing job information. You standardized the company names, handled missing values, and split skills into a more structured format.

Skill Extraction: Using spaCy and its PhraseMatcher tool, you built a skill extraction system. A predefined list of skills was used to match and extract skills from the job descriptions (Requirements column) and stored them in a new column.

Visualization: created several visualizations using matplotlib and seaborn to display common job titles, companies with the most listings, and the most in-demand skills.

Saving Results:exported the cleaned and analyzed data into CSV and Excel files, and saved graphs as PNG files.
