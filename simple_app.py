from flask import Flask, render_template, request, jsonify
import json
import os
import openai
from datetime import datetime
import random

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY", "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")

def load_publications():
    try:
        with open('data/sample_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return generate_sample_data()

def generate_sample_data():
    return [
        {
            "id": 1, "title": "Effects of Microgravity on Arabidopsis thaliana Root Growth",
            "abstract": "This study investigated how microgravity conditions aboard the International Space Station affect the root growth and development of Arabidopsis thaliana.",
            "year": 2022, "mission": "International Space Station",
            "topics": ["Plant Biology", "Microgravity", "Root Development", "Arabidopsis"]
        },
        {
            "id": 2, "title": "Radiation Effects on Mammalian Cell Cultures in Deep Space Environment",
            "abstract": "Research examined the impact of deep space radiation on mammalian cell cultures during the Artemis I mission.",
            "year": 2023, "mission": "Artemis I",
            "topics": ["Radiation Biology", "Mammalian Cells", "DNA Repair", "Deep Space"]
        },
        {
            "id": 3, "title": "Microbial Adaptation to Spaceflight Conditions",
            "abstract": "Long-term study monitored changes in microbial communities aboard the ISS focusing on adaptation to spaceflight conditions.",
            "year": 2021, "mission": "International Space Station",
            "topics": ["Microbiology", "Adaptation", "Spacecraft Environment", "Astronaut Health"]
        },
        {
            "id": 4, "title": "Gravitational Effects on Neural Stem Cell Differentiation",
            "abstract": "Investigating how altered gravity environments influence differentiation pathways of neural stem cells.",
            "year": 2020, "mission": "SpaceX CRS-21",
            "topics": ["Stem Cells", "Neuroscience", "Gravitational Biology", "Cell Differentiation"]
        },
        {
            "id": 5, "title": "Circadian Rhythm Disruption in Space",
            "abstract": "Examined effects of spaceflight on circadian rhythms in animal models and tested countermeasures.",
            "year": 2019, "mission": "Rodent Research-5",
            "topics": ["Circadian Rhythms", "Sleep", "Animal Models", "Countermeasures"]
        },
        {
            "id": 6, "title": "Protein Crystal Growth in Microgravity for Drug Development",
            "abstract": "Utilizing microgravity to grow higher-quality protein crystals for pharmaceutical development.",
            "year": 2022, "mission": "International Space Station",
            "topics": ["Protein Crystallography", "Drug Development", "Microgravity", "Biotechnology"]
        },
        {
            "id": 7, "title": "Effects of Space Radiation on Drosophila Melanogaster Genome",
            "abstract": "Documented genomic changes in fruit flies from space radiation exposure.",
            "year": 2018, "mission": "SpaceX CRS-14",
            "topics": ["Genetics", "Radiation", "Drosophila", "Genomic Instability"]
        },
        {
            "id": 8, "title": "Tissue Engineering in Microgravity: Vascular Network Formation",
            "abstract": "Demonstrated enhanced vascular network formation in engineered tissues grown in microgravity.",
            "year": 2023, "mission": "International Space Station",
            "topics": ["Tissue Engineering", "Regenerative Medicine", "Vascular Biology", "3D Bioprinting"]
        },
        {
            "id": 9, "title": "Metabolic Changes in Plants Under Simulated Martian Conditions",
            "abstract": "Investigating plant adaptation to simulated Martian soil and atmospheric conditions.",
            "year": 2021, "mission": "Earth-based Analog",
            "topics": ["Plant Metabolism", "Mars Exploration", "Life Support Systems", "Space Agriculture"]
        },
        {
            "id": 10, "title": "Immune System Function During Long-Duration Spaceflight",
            "abstract": "Longitudinal study of astronaut immune function during 6-month missions aboard the ISS.",
            "year": 2020, "mission": "International Space Station",
            "topics": ["Immunology", "Long-duration Spaceflight", "Cytokines", "Astronaut Health"]
        }
    ]

publications = load_publications()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/publications')
def get_publications():
    keyword = request.args.get('keyword', '')
    year = request.args.get('year', '')
    mission = request.args.get('mission', '')
    
    filtered_pubs = publications
    
    if keyword:
        filtered_pubs = [p for p in filtered_pubs if keyword.lower() in p['title'].lower() or 
                        keyword.lower() in p['abstract'].lower()]
    
    if year:
        filtered_pubs = [p for p in filtered_pubs if p['year'] == int(year)]
    
    if mission:
        filtered_pubs = [p for p in filtered_pubs if mission.lower() in p['mission'].lower()]
    
    return jsonify(filtered_pubs)

@app.route('/api/summarize', methods=['POST'])
def summarize_publication():
    data = request.json
    publication_id = data.get('id')
    
    publication = next((p for p in publications if p['id'] == publication_id), None)
    
    if not publication:
        return jsonify({'error': 'Publication not found'}), 404
    
    # Mock AI summary for demo (replace with actual OpenAI call)
    mock_summaries = [
        "Key findings include significant alterations in growth patterns under microgravity conditions, suggesting adaptive mechanisms in plant biology.",
        "This research demonstrates notable cellular responses to space radiation, highlighting potential risks and protective strategies for long-duration missions.",
        "The study reveals microbial adaptation patterns that could impact spacecraft hygiene and astronaut health during extended space missions."
    ]
    
    summary = f"AI Summary for '{publication['title']}':\n\n{random.choice(mock_summaries)}"
    
    return jsonify({'summary': summary})

@app.route('/api/analyze_trends')
def analyze_trends():
    years = {}
    topics = {}
    
    for pub in publications:
        year = pub['year']
        if year not in years:
            years[year] = 0
        years[year] += 1
        
        for topic in pub['topics']:
            if topic not in topics:
                topics[topic] = 0
            topics[topic] += 1
    
    return jsonify({
        'years': years,
        'topics': topics
    })

@app.route('/api/knowledge_graph')
def get_knowledge_graph():
    graph_data = {
        'nodes': [],
        'links': []
    }
    
    topics_set = set()
    for pub in publications:
        for topic in pub['topics']:
            topics_set.add(topic)
    
    for i, topic in enumerate(topics_set):
        graph_data['nodes'].append({
            'id': topic,
            'name': topic,
            'val': sum(1 for p in publications if topic in p['topics'])
        })
    
    for pub in publications:
        for i, topic1 in enumerate(pub['topics']):
            for topic2 in pub['topics'][i+1:]:
                graph_data['links'].append({
                    'source': topic1,
                    'target': topic2
                })
    
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)

