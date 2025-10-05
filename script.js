// API Base URL
const API_BASE = 'http://localhost:5000/api';

// Global variables
let currentCategory = 'all';
let categoryChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboard();
    loadExperiments();
    initAIAssistant();
    initModal();
});

// Navigation
function initNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            showSection(section);
            
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();
        
        // Update stats
        document.getElementById('total-experiments').textContent = stats.total_experiments;
        document.getElementById('total-categories').textContent = Object.keys(stats.categories).length;
        document.getElementById('latest-date').textContent = stats.latest_date;
        
        // Create chart
        createCategoryChart(stats.categories);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function createCategoryChart(categories) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: [
                    '#00d4ff',
                    '#7b2ff7',
                    '#ff6b6b',
                    '#4ecdc4',
                    '#45b7d1',
                    '#f9ca24'
                ],
                borderColor: '#0a0e27',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
                            family: 'Roboto'
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: '#1a1f3a',
                    titleColor: '#00d4ff',
                    bodyColor: '#fff',
                    borderColor: '#00d4ff',
                    borderWidth: 2
                }
            }
        }
    });
}

// Experiments
async function loadExperiments(category = 'all') {
    try {
        const response = await fetch(`${API_BASE}/experiments?category=${category}`);
        const experiments = await response.json();
        
        const grid = document.getElementById('experiments-grid');
        grid.innerHTML = '';
        
        experiments.forEach(exp => {
            const card = createExperimentCard(exp);
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading experiments:', error);
    }
}

function createExperimentCard(exp) {
    const card = document.createElement('div');
    card.className = 'experiment-card';
    card.innerHTML = `
        <span class="experiment-category">${exp.category}</span>
        <h3>${exp.title}</h3>
        <p class="experiment-organism">📊 Organism: ${exp.organism}</p>
        <p class="experiment-summary">${exp.summary}</p>
        <p class="experiment-date">🚀 Mission: ${exp.mission}</p>
        <button class="view-details-btn" onclick="showExperimentDetails(${exp.id})">
            View Details & AI Summary
        </button>
    `;
    return card;
}

// Category filter
document.addEventListener('DOMContentLoaded', () => {
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', (e) => {
            currentCategory = e.target.value;
            loadExperiments(currentCategory);
        });
    }
});

// Modal
function initModal() {
    const modal = document.getElementById('experiment-modal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.onclick = () => {
        modal.style.display = 'none';
    };
    
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}

async function showExperimentDetails(expId) {
    const modal = document.getElementById('experiment-modal');
    const modalBody = document.getElementById('modal-body');
    
    modal.style.display = 'block';
    modalBody.innerHTML = '<div class="loading"></div><p style="text-align:center;">Loading experiment details...</p>';
    
    try {
        // Get experiment details
        const expResponse = await fetch(`${API_BASE}/experiment/${expId}`);
        const exp = await expResponse.json();
        
        // Get AI summary
        modalBody.innerHTML = '<div class="loading"></div><p style="text-align:center;">Generating AI summary...</p>';
        const summaryResponse = await fetch(`${API_BASE}/summarize/${expId}`, {
            method: 'POST'
        });
        const summaryData = await summaryResponse.json();
        
        // Display details
        modalBody.innerHTML = `
            <span class="experiment-category">${exp.category}</span>
            <h2 style="color: #00d4ff; margin: 1rem 0;">${exp.title}</h2>
            
            <div style="background: rgba(0,212,255,0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: #00d4ff;">📊 Experiment Overview</h3>
                <p style="margin: 0.5rem 0;"><strong>Organism:</strong> ${exp.organism}</p>
                <p style="margin: 0.5rem 0;"><strong>Mission:</strong> ${exp.mission}</p>
                <p style="margin: 0.5rem 0;"><strong>Date:</strong> ${exp.date}</p>
            </div>
            
            <div style="background: rgba(123,47,247,0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: #7b2ff7;">🔬 Summary</h3>
                <p style="line-height: 1.8; color: #ccc;">${exp.summary}</p>
            </div>
            
            <div style="background: rgba(0,212,255,0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: #00d4ff;">💡 Key Findings</h3>
                <p style="line-height: 1.8; color: #ccc;">${exp.findings}</p>
            </div>
            
            <div style="background: rgba(123,47,247,0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: #7b2ff7;">🤖 AI-Generated Detailed Analysis</h3>
                <p style="line-height: 1.8; color: #ccc;">${summaryData.summary}</p>
            </div>
        `;
    } catch (error) {
        modalBody.innerHTML = `<p style="color: #ff6b6b;">Error loading experiment details: ${error.message}</p>`;
    }
}

// AI Assistant
function initAIAssistant() {
    const askBtn = document.getElementById('ask-btn');
    const questionInput = document.getElementById('user-question');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    
    askBtn.addEventListener('click', () => {
        const question = questionInput.value.trim();
        if (question) {
            askAI(question);
            questionInput.value = '';
        }
    });
    
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const question = questionInput.value.trim();
            if (question) {
                askAI(question);
                questionInput.value = '';
            }
        }
    });
    
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            askAI(btn.textContent);
        });
    });
}

async function askAI(question) {
    const chatMessages = document.getElementById('chat-messages');
    
    // Add user message
    addMessage(question, 'user');
    
    // Add loading message
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant-message';
    loadingDiv.innerHTML = '<div class="loading"></div> <span>Thinking...</span>';
    loadingDiv.id = 'loading-message';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById('loading-message').remove();
        
        // Add AI response
        addMessage(data.answer, 'assistant');
    } catch (error) {
        document.getElementById('loading-message').remove();
        addMessage(`Sorry, I encountered an error: ${error.message}. Please make sure your OpenAI API key is configured.`, 'assistant');
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    if (sender === 'user') {
        messageDiv.innerHTML = `<strong>You:</strong> ${text}`;
    } else {
        messageDiv.innerHTML = `<strong>AI Assistant:</strong> ${text}`;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Expose function to global scope for onclick handlers
window.showExperimentDetails = showExperimentDetails;
