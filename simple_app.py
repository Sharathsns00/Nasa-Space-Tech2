from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SPACE_EXPERIMENTS = [
    {
        "id": 1,
        "title": "Effects of Microgravity on Plant Growth",
        "date": "2023-05",
        "organism": "Arabidopsis thaliana",
        "category": "Botany",
        "summary": "Study examining how microgravity affects root growth and gravitropism in plants.",
        "findings": "Plants showed altered gene expression in microgravity, affecting cell wall formation.",
        "mission": "ISS Expedition 68"
    },
    {
        "id": 2,
        "title": "Bone Density Loss in Extended Spaceflight",
        "date": "2023-08",
        "organism": "Homo sapiens",
        "category": "Human Physiology",
        "summary": "Investigation of calcium metabolism and bone density changes in astronauts.",
        "findings": "Average bone density loss of 1-2% per month in weight-bearing bones.",
        "mission": "ISS Long Duration Study"
    },
    {
        "id": 3,
        "title": "Bacterial Biofilm Formation in Microgravity",
        "date": "2023-03",
        "organism": "E. coli",
        "category": "Microbiology",
        "summary": "Analysis of bacterial behavior and antibiotic resistance in space conditions.",
        "findings": "Enhanced biofilm formation and increased antibiotic resistance observed.",
        "mission": "SpaceX CRS-27"
    }
]

RESEARCH_PAPERS = [
    {"title": "Mice in Bion-M 1 space mission: training and selection", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4136787/"},
    {"title": "Microgravity induces pelvic bone loss through osteoclastic activity, osteocytic osteolysis, and osteoblastic cell cycle inhibition by CDKN1a/p21", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3630201/"},
    {"title": "Stem Cell Health and Tissue Regeneration in Microgravity", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11988870/"},
    {"title": "Microgravity Reduces the Differentiation and Regenerative Potential of Embryonic Stem Cells", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7998608/"},
    {"title": "Microgravity validation of a novel system for RNA isolation and multiplex quantitative real time PCR analysis of gene expression on the International Space Station", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5587110/"},
    {"title": "Spaceflight Modulates the Expression of Key Oxidative Stress and Cell Cycle Related Genes in Heart", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8396460/"},
    {"title": "Dose- and Ion-Dependent Effects in the Oxidative Stress Response to Space-Like Radiation Exposure in the Skeletal System", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5666799/"},
    {"title": "From the bench to exploration medicine: NASA life sciences translational research for human exploration and habitation missions.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5460236/"},
    {"title": "High-precision method for cyclic loading of small-animal vertebrae to assess bone quality.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6222041/"},
    {"title": "Effects of ex vivo ionizing radiation on collagen structure and whole-bone mechanical properties of mouse vertebrae.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6813909/"},
    {"title": "Absence of gamma-sarcoglycan alters the response of p70S6 kinase to mechanical perturbation in murine skeletal muscle", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4095884/"},
    {"title": "AtRabD2b and AtRabD2c have overlapping functions in pollen development and pollen tube growth.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3040128/"},
    {"title": "TNO1 is involved in salt tolerance and vacuolar trafficking in Arabidopsis.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3177255/"},
    {"title": "Functional redundancy between trans-Golgi network SNARE family members in Arabidopsis thaliana.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11500582/"},
    {"title": "Root growth movements: Waving and skewing.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5387210/"},
    {"title": "Gravitropism and lateral root emergence are dependent on the trans-Golgi network protein TNO1", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4642138/"},
    {"title": "TNO1, a TGN-localized SNARE-interacting protein, modulates root skewing in Arabidopsis thaliana.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5387210/"},
    {"title": "The Drosophila SUN protein Spag4 cooperates with the coiled-coil protein Yuri Gagarin to maintain association of the basal body and spermatid nucleus.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2915878/"},
    {"title": "Toll mediated infection response is altered by gravity and spaceflight in Drosophila", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3901686/"},
    {"title": "Multi-omics analysis of multiple missions to space reveal a theme of lipid dysregulation in mouse liver", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6985101/"},
    {"title": "GeneLab database analyses suggest long-term impact of space radiation on the cardiovascular system by the activation of FYN through reactive oxygen species.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6387434/"},
    {"title": "FAIRness and usability for open-access omics data systems.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6371294/"},
    {"title": "NASA GeneLab platform utilized for biological response to space radiation in animal models", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7072278/"},
    {"title": "Circulating miRNA spaceflight signature reveals targets for countermeasure development", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8441986/"},
    {"title": "Machine learning algorithm to characterize antimicrobial resistance associated with the International Space Station surface microbiome", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9400218/"},
    {"title": "Extraterrestrial Gynecology: Could Spaceflight Increase the Risk of Developing Cancer in Female Astronauts? An Updated Review", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9267413/"},
    {"title": "Muscle atrophy phenotype gene expression during spaceflight is linked to a metabolic crosstalk in both the liver and the muscle in mice.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9576569/"},
    {"title": "Chromosomal positioning and epigenetic architecture influence DNA methylation patterns triggered by galactic cosmic radiation", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10789781/"},
    {"title": "A comprehensive SARS-CoV-2 and COVID-19 review, Part 2: Host extracellular to systemic effects of SARS-CoV-2 infection", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10772081/"},
    {"title": "Aging and putative frailty biomarkers are altered by spaceflight", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11166946/"},
    {"title": "Space radiation damage rescued by inhibition of key spaceflight associated miRNAs", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11166944/"},
    {"title": "Ethical considerations for the age of non-governmental space exploration", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11166968/"},
    {"title": "Innate immune responses of Drosophila melanogaster are altered by spaceflight.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7000411/"},
    {"title": "Prolonged Exposure to Microgravity Reduces Cardiac Contractility and Initiates Remodeling in Drosophila", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7787258/"},
    {"title": "Regulation of plant gravity sensing and signaling by the actin cytoskeleton.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8716943/"},
    {"title": "HLB1 Is a Tetratricopeptide Repeat Domain-Containing Protein That Operates at the Intersection of the Exocytic and Endocytic Pathways at the TGN/EE in Arabidopsis", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4826010/"},
    {"title": "ERULUS is a plasma membrane-localized receptor-like kinase that specifies root hair growth by maintaining tip-focused cytoplasmic calcium oscillations.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6048781/"},
    {"title": "Brassinosteroids inhibit autotropic root straightening by modifying filamentous-actin organization and dynamics.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7010715/"},
    {"title": "Cell type-specific imaging of calcium signaling in Arabidopsis thaliana seedling roots using GCaMP3.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7503278/"},
    {"title": "Spatial and temporal localization of SPIRRIG and WAVE/SCAR reveal roles for these proteins in actin-mediated root hair development.", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8364238/"},
    {"title": "Microgravity Stress: Bone and Connective Tissue", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11579474/"},
    {"title": "S. aureus MscL is a pentamer in vivo but of variable stoichiometries in vitro: implications for detergent-solubilized membrane proteins", "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2998437/"}
]

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA Space Biology Explorer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.5); }
            50% { box-shadow: 0 0 40px rgba(123, 47, 247, 0.8); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(123, 47, 247, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        
        header {
            text-align: center;
            padding: 60px 0;
            border-bottom: 3px solid #00d4ff;
            margin-bottom: 40px;
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.8) 0%, rgba(13, 17, 23, 0.6) 100%);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.8s ease-out;
        }
        
        h1 {
            font-size: 3.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            font-weight: 900;
            letter-spacing: 2px;
            animation: glow 3s ease-in-out infinite;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }
        
        .tagline {
            color: #00d4ff;
            font-size: 1.2rem;
            font-weight: 300;
            letter-spacing: 1px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(123, 47, 247, 0.1) 100%);
            border: 2px solid #00d4ff;
            border-radius: 20px;
            padding: 35px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .stat-card:hover::before {
            left: 100%;
        }
        
        .stat-card:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 15px 40px rgba(0, 212, 255, 0.4);
            border-color: #7b2ff7;
            animation: float 3s ease-in-out infinite;
        }
        
        .stat-icon {
            font-size: 3.5rem;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.6));
            animation: float 4s ease-in-out infinite;
        }
        
        .stat-value {
            font-size: 3rem;
            color: #00d4ff;
            font-weight: 900;
            margin-bottom: 12px;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.8);
        }
        
        .stat-label {
            color: #bbb;
            font-size: 1.1rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .experiments-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        
        .experiment-card {
            background: linear-gradient(135deg, rgba(123, 47, 247, 0.15) 0%, rgba(13, 17, 23, 0.8) 100%);
            border: 2px solid #7b2ff7;
            border-radius: 20px;
            padding: 30px;
            transition: all 0.4s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .experiment-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(0, 212, 255, 0.1), transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .experiment-card:hover::after {
            opacity: 1;
        }
        
        .experiment-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 40px rgba(123, 47, 247, 0.5);
            border-color: #00d4ff;
        }
        
        .experiment-category {
            display: inline-block;
            background: linear-gradient(135deg, #7b2ff7, #b47fff);
            color: #fff;
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 0.85rem;
            margin-bottom: 18px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(123, 47, 247, 0.4);
        }
        
        .experiment-card h3 {
            color: #00d4ff;
            margin-bottom: 18px;
            font-size: 1.4rem;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            line-height: 1.4;
        }
        
        .experiment-organism {
            color: #bbb;
            font-style: italic;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }
        
        .experiment-summary {
            color: #ddd;
            line-height: 1.8;
            margin-bottom: 18px;
            font-size: 1rem;
        }
        
        .experiment-mission {
            color: #999;
            font-size: 0.9rem;
            margin-top: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .ai-section {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(26, 31, 58, 0.8) 100%);
            border: 2px solid #00d4ff;
            border-radius: 25px;
            padding: 40px;
            margin-top: 50px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 40px rgba(0, 212, 255, 0.2);
            animation: slideIn 1s ease-out;
        }
        
        .ai-section h2 {
            color: #00d4ff;
            margin-bottom: 25px;
            font-size: 2.2rem;
            font-weight: 800;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .chat-container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 25px;
            max-height: 450px;
            overflow-y: auto;
            margin-bottom: 25px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
        }
        
        .chat-container::-webkit-scrollbar {
            width: 10px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00d4ff, #7b2ff7);
            border-radius: 10px;
        }
        
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #7b2ff7, #00d4ff);
        }
        
        .message {
            margin-bottom: 20px;
            padding: 18px 22px;
            border-radius: 15px;
            line-height: 1.7;
            animation: slideIn 0.4s ease-out;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .user-message {
            background: linear-gradient(135deg, #00d4ff, #00a8cc);
            color: #0a0e27;
            margin-left: 20%;
            font-weight: 500;
            border-bottom-right-radius: 5px;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #7b2ff7, #9b59d0);
            color: #fff;
            margin-right: 20%;
            border-bottom-left-radius: 5px;
        }
        
        .input-group {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        input[type="text"] {
            flex: 1;
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid #00d4ff;
            color: #fff;
            padding: 18px 22px;
            border-radius: 15px;
            font-size: 1.05rem;
            transition: all 0.3s;
            outline: none;
        }
        
        input[type="text"]:focus {
            border-color: #7b2ff7;
            box-shadow: 0 0 20px rgba(123, 47, 247, 0.4);
            background: rgba(0, 0, 0, 0.7);
        }
        
        input[type="text"]::placeholder {
            color: #888;
        }
        
        button {
            background: linear-gradient(135deg, #00d4ff, #00a8cc);
            color: #0a0e27;
            border: none;
            padding: 18px 35px;
            border-radius: 15px;
            font-weight: 700;
            cursor: pointer;
            font-size: 1.05rem;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
        }
        
        button:hover {
            background: linear-gradient(135deg, #7b2ff7, #9b59d0);
            color: #fff;
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(123, 47, 247, 0.5);
        }
        
        button:active {
            transform: translateY(-1px) scale(1.02);
        }
        
        .loading {
            text-align: center;
            color: #00d4ff;
            padding: 30px;
            font-size: 1.2rem;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        h2 {
            color: #00d4ff;
            font-size: 2rem;
            margin-bottom: 25px;
            font-weight: 800;
            text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
        }
        
        section {
            margin-bottom: 60px;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem;
            }
            
            .stat-card {
                padding: 25px;
            }
            
            .stat-icon {
                font-size: 2.5rem;
            }
            
            .stat-value {
                font-size: 2.2rem;
            }
            
            .experiments-grid {
                grid-template-columns: 1fr;
            }
            
            .user-message, .assistant-message {
                margin-left: 0 !important;
                margin-right: 0 !important;
            }
            
            button {
                padding: 15px 25px;
                font-size: 0.95rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 NASA Space Biology Explorer</h1>
            <p class="tagline">Advancing Human Space Exploration Through Science</p>
        </header>
        
        <section>
            <h2 style="color: #00d4ff; margin-bottom: 20px;">Mission Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">🧬</div>
                    <div class="stat-value" id="total-experiments">0</div>
                    <div class="stat-label">Total Experiments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🔬</div>
                    <div class="stat-value">3</div>
                    <div class="stat-label">Research Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🌍</div>
                    <div class="stat-value">ISS</div>
                    <div class="stat-label">Primary Platform</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📅</div>
                    <div class="stat-value">42</div>
                    <div class="stat-label">Research Papers</div>
                </div>
            </div>
        </section>
        
        <section>
            <h2 style="color: #00d4ff;">Space Biology Experiments</h2>
            <div class="experiments-grid" id="experiments-grid">
                <div class="loading">Loading experiments...</div>
            </div>
        </section>
        
        <section class="ai-section">
            <h2>🤖 AI Research Assistant</h2>
            <p style="margin-bottom: 20px; color: #ccc;">Ask me anything about NASA's space biology research!</p>
            
            <div class="chat-container" id="chat-messages">
                <div class="message assistant-message">
                    <strong>AI Assistant:</strong> Hello! I'm your NASA Space Biology AI Assistant. Ask me about experiments, organisms, or space biology topics!
                </div>
            </div>
            
            <div class="input-group">
                <input type="text" id="user-question" placeholder="Ask a question about space biology..." />
                <button onclick="askAI()">Send</button>
            </div>
        </section>
    </div>
    
    <script>
        // Load experiments on page load
        async function loadExperiments() {
            try {
                const response = await fetch('/api/experiments');
                const experiments = await response.json();
                
                document.getElementById('total-experiments').textContent = experiments.length;
                
                const grid = document.getElementById('experiments-grid');
                grid.innerHTML = '';
                
                experiments.forEach(exp => {
                    const card = document.createElement('div');
                    card.className = 'experiment-card';
                    card.innerHTML = `
                        <span class="experiment-category">${exp.category}</span>
                        <h3>${exp.title}</h3>
                        <p class="experiment-organism">📊 Organism: ${exp.organism}</p>
                        <p class="experiment-summary">${exp.summary}</p>
                        <p class="experiment-mission">🚀 ${exp.mission}</p>
                        <p class="experiment-mission">📅 ${exp.date}</p>
                    `;
                    grid.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading experiments:', error);
                document.getElementById('experiments-grid').innerHTML = 
                    '<p style="color: #ff6b6b;">Error loading experiments. Please check your server.</p>';
            }
        }
        
        // AI Assistant
        async function askAI() {
            const input = document.getElementById('user-question');
            const question = input.value.trim();
            
            if (!question) return;
            
            const chatMessages = document.getElementById('chat-messages');
            
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.innerHTML = `<strong>You:</strong> ${question}`;
            chatMessages.appendChild(userMsg);
            
            // Clear input
            input.value = '';
            
            // Add loading message
            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'message assistant-message';
            loadingMsg.id = 'loading-msg';
            loadingMsg.innerHTML = '<strong>AI Assistant:</strong> Thinking...';
            chatMessages.appendChild(loadingMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                
                const data = await response.json();
                
                // Remove loading message
                document.getElementById('loading-msg').remove();
                
                // Add AI response
                const aiMsg = document.createElement('div');
                aiMsg.className = 'message assistant-message';
                aiMsg.innerHTML = `<strong>AI Assistant:</strong> ${data.answer}`;
                chatMessages.appendChild(aiMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
            } catch (error) {
                document.getElementById('loading-msg').remove();
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message assistant-message';
                errorMsg.innerHTML = `<strong>AI Assistant:</strong> Sorry, I encountered an error. Make sure your OpenAI API key is configured in the .env file.`;
                chatMessages.appendChild(errorMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
        
        // Allow Enter key to send message
        document.getElementById('user-question').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') askAI();
        });
        
        // Load experiments when page loads
        loadExperiments();
    </script>
</body>
</html>
    '''

@app.route('/api/experiments')
def get_experiments():
    return jsonify(SPACE_EXPERIMENTS)

@app.route('/api/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.json
        question = data.get('question', '').lower()
        
        # Enhanced responses with research paper topics
        responses = {
            'plant': """Based on our Arabidopsis thaliana experiments from ISS Expedition 68:

**Effects on Plants:**
- Plants show altered gene expression in microgravity
- Root growth patterns change significantly (gravitropism and root skewing)
- Cell wall formation is affected
- Actin cytoskeleton regulation impacts gravity sensing
- TNO1 protein plays key role in root development

**Research Areas:**
- Pollen development and tube growth
- Salt tolerance and vacuolar trafficking
- Trans-Golgi network SNARE proteins
- Brassinosteroids and root straightening
- Calcium signaling in root hair development

**Implications:** This research helps us understand how to grow food on long-duration missions to Mars and sustain lunar bases.""",

            'bone': """From our ISS Long Duration Studies on human physiology:

**Bone Density Loss:**
- Average loss: 1-2% per month in weight-bearing bones
- Pelvic bone loss through osteoclastic activity and osteocytic osteolysis
- CDKN1a/p21 causes osteoblastic cell cycle inhibition
- Collagen structure and mechanical properties affected
- Ion-dependent effects on skeletal oxidative stress

**Research Methods:**
- High-precision cyclic loading on vertebrae
- Ex vivo ionizing radiation studies
- Mouse vertebrae mechanical testing

**Critical for:** Understanding health risks for Mars missions (6-9 months travel time).""",

            'bacteria': """E. coli research from SpaceX CRS-27 mission:

**Bacterial Behavior in Space:**
- Enhanced biofilm formation observed
- Increased antibiotic resistance
- ISS surface microbiome shows antimicrobial resistance patterns
- Machine learning algorithms characterize resistance mechanisms
- S. aureus MscL protein studies

**Important because:** Astronaut health and spacecraft cleanliness are critical for long missions.""",

            'muscle': """From Rodent Research-9 (Mus musculus studies):

**Muscle Atrophy Findings:**
- Significant muscle loss occurs in microgravity
- Gamma-sarcoglycan affects p70S6 kinase response
- Metabolic crosstalk between liver and muscle
- High-intensity interval training showed 40% better preservation
- Exercise protocols essential for astronaut health

**Countermeasures being developed for Mars missions**""",

            'stem': """Stem Cell Research in Microgravity:

**Key Findings:**
- Reduced differentiation and regenerative potential
- Tissue regeneration challenges identified
- Embryonic stem cells show altered development
- Important for long-term space health

**Applications:** Understanding stem cell behavior for medical treatments in space.""",

            'heart': """Cardiac Research in Space:

**Cardiovascular Effects:**
- Oxidative stress and cell cycle genes modulated
- Drosophila studies show cardiac contractility reduction
- Remodeling initiated by prolonged microgravity exposure
- FYN activation through reactive oxygen species
- Long-term cardiovascular impact identified

**Critical for:** Astronaut health monitoring on extended missions.""",

            'radiation': """Space Radiation Studies:

**DNA & Radiation Effects:**
- Cosmic radiation causes DNA damage
- Chromosomal positioning affects DNA methylation patterns
- Galactic cosmic radiation triggers epigenetic changes
- miRNA spaceflight signature reveals countermeasure targets
- Radiation damage can be rescued by miRNA inhibition
- Space radiation affects biological systems in animals

**Why it matters:** Mars missions expose astronauts to more radiation than ISS.""",

            'gene': """GeneLab and Gene Expression Studies:

**Key Research:**
- RNA isolation and PCR analysis on ISS
- Multi-omics analysis reveals lipid dysregulation
- Gene expression changes in heart and liver
- NASA GeneLab platform for radiation response
- FAIRness and usability of omics data systems

**Impact:** Understanding molecular changes in space environment.""",

            'immune': """Immune System in Space:

**Research Findings:**
- Drosophila melanogaster immune responses altered
- Toll-mediated infection response changed
- Gravity affects immune function
- Important for astronaut health protection

**Applications:** Developing immune countermeasures for long missions.""",

            'aging': """Aging and Frailty in Space:

**Biomarkers:**
- Putative frailty biomarkers altered by spaceflight
- Accelerated aging processes observed
- Long-term health implications identified

**Importance:** Understanding aging for multi-year space missions.""",

            'drosophila': """Drosophila (Fruit Fly) Studies:

**Research Areas:**
- SUN protein Spag4 and Yuri Gagarin protein interactions
- Cardiac contractility reduction in microgravity
- Toll-mediated infection responses
- Innate immune system alterations

**Why fruit flies:** Model organism for genetics and physiology research.""",

            'organism': """Our database includes experiments on various organisms:

**Studied Organisms:**
- **Arabidopsis thaliana** (plants) - gravitropism, root development
- **Homo sapiens** (humans) - bone density, muscle loss, cardiovascular
- **E. coli** (bacteria) - biofilm formation, resistance
- **Mus musculus** (mice) - muscle atrophy, liver metabolism
- **Drosophila** (fruit flies) - immune response, cardiac function
- **Stem cells** - regeneration and differentiation studies

Each helps us understand different aspects of life in space!""",

            'mission': """Our experiments span multiple missions:

**Mission Platforms:**
- ISS (International Space Station) - ongoing research
- SpaceX CRS missions - cargo resupply + experiments
- Bion-M 1 - Russian biosatellite mission
- Artemis program - Moon exploration biology
- Various expedition crews conduct experiments

**Research Publications:** 42+ peer-reviewed papers on NCBI

These studies prepare us for Moon bases and Mars exploration!""",

            'ethics': """Ethical Considerations:

**Space Exploration Ethics:**
- Non-governmental space exploration considerations
- Extraterrestrial gynecology and cancer risks
- Female astronaut health concerns
- Long-term health implications

**Important for:** Responsible space exploration development.""",

            'paper': """We have 42 published research papers available covering:

**Research Topics:**
- Bone and muscle physiology
- Plant biology and gravitropism
- Cardiovascular effects
- Stem cell research
- Immune system responses
- Radiation and DNA damage
- Gene expression studies
- Microbial behavior
- Aging and frailty biomarkers

**All papers available on NCBI PubMed Central**""",

            'liver': """Liver Metabolism in Space:

**Multi-omics Analysis:**
- Lipid dysregulation themes identified
- Metabolic crosstalk with muscle tissue
- Gene expression changes during spaceflight

**Importance:** Understanding metabolic changes for nutrition planning.""",

            'rna': """RNA and Gene Expression:

**Research Capabilities:**
- RNA isolation systems validated on ISS
- Multiplex quantitative real-time PCR analysis
- Gene expression monitoring in space
- miRNA spaceflight signatures identified

**Applications:** Real-time biological monitoring on missions.""",
        }
        
        # Find matching response
        answer = None
        for keyword, response in responses.items():
            if keyword in question:
                answer = response
                break
        
        # Default response if no match
        if not answer:
            answer = """I can help you learn about NASA space biology research! 

**Available Topics:**
- Plant growth and gravitropism
- Bone density and osteoporosis
- Muscle atrophy and countermeasures
- Bacterial behavior and biofilms
- Stem cell health and regeneration
- Cardiovascular effects
- Space radiation and DNA damage
- Gene expression and RNA analysis
- Immune system responses
- Aging and frailty biomarkers
- Drosophila (fruit fly) studies
- Liver metabolism changes
- Ethics in space exploration
- Research papers and publications

**Try asking:** 
"Tell me about bone loss in space"
"What happens to plants in microgravity?"
"How does radiation affect DNA?"
"What immune system changes occur?"
"Tell me about stem cell research"
"What research papers are available?" """
        
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)