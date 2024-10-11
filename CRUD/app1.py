from flask import Flask, render_template, request, send_file
from pymongo import MongoClient
import matplotlib
import matplotlib.pyplot as plt
import os
from collections import Counter
import pandas as pd

matplotlib.use('Agg')

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['Job_Listing']
collection = db['Job_Listing_data']

CHART_FOLDER = 'static/charts'
if not os.path.exists(CHART_FOLDER):
    os.makedirs(CHART_FOLDER)

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    pipeline = [
        {"$group": {"_id": "$Title", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 250}
    ]
    title_data = list(collection.aggregate(pipeline))
    titles = [item['_id'] for item in title_data]  
    locations = collection.distinct('Locations')

    return render_template('index.html', titles=titles, locations=locations)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    selected_title = request.form.get('title').strip()
    selected_location = request.form.get('location').strip()

    filtered_data = list(collection.find(
        {
            'Title': {"$regex": f"^{selected_title}$", "$options": "i"},
            'Locations': {"$regex": f"^{selected_location}$", "$options": "i"}
        },
        {'_id': 0}  
    ))

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        csv_filename = 'filtered_data.csv'
        csv_filepath = os.path.join('static', csv_filename)
        df.to_csv(csv_filepath, index=False)  

        columns_to_plot = ['skills', 'Min_Experience', 'Max_Experience', 'Company-Name']
        chart_paths = {}

        for column in columns_to_plot:
            column_data = [job.get(column) for job in filtered_data if job.get(column)]
            
            if column_data:
                value_counts = Counter(column_data).most_common(10)

                labels = [str(item[0]) for item in value_counts]
                sizes = [item[1] for item in value_counts]

                plt.figure(figsize=(10, 6))
                plt.bar(labels, sizes, color='skyblue')
                plt.xlabel(column.replace('_', ' '))
                plt.ylabel('Count')
                plt.title(f'Top 10 {column.replace("_", " ")} Distribution')

                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()

                chart_filename = f'{column}_bar_chart.png'
                chart_path = os.path.join(CHART_FOLDER, chart_filename)
                plt.savefig(chart_path)
                plt.close()  

                chart_paths[column] = chart_path

        return render_template('results.html', chart_paths=chart_paths, csv_file=csv_filename)

    return render_template('results.html', chart_paths=None, message="No data found for the selected Title and Location.")

@app.route('/download_csv')
def download_csv():
    return send_file(os.path.join('static', 'filtered_data.csv'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
