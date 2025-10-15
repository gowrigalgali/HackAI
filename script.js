// HackAI Frontend JavaScript

class HackAIApp {
    constructor() {
        this.initializeApp();
        this.setupEventListeners();
        this.baseUrl = this.detectApiUrl();
        this.agentOrder = ['ideation','research','planning','coding','presentation'];
        this.currentAgentIndex = 0;
    }

    initializeApp() {
        console.log('🚀 HackAI Frontend initialized');
    }

    detectApiUrl() {
        // Auto-detect API URL based on environment
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000';
        }
        return ''; // Relative URLs for production
    }

    setupEventListeners() {
        const form = document.getElementById('projectForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const title = document.getElementById('title').value.trim();
        const brief = document.getElementById('brief').value.trim();
        const timeHours = parseInt(document.getElementById('timeHours').value);

        if (!title || !brief) {
            this.showNotification('Please fill in all required fields', 'error');
            return;
        }

        try {
            await this.generateProject({ title, brief, time_hours: timeHours });
        } catch (error) {
            console.error('Error generating project:', error);
            this.showNotification('Failed to generate project. Please try again.', 'error');
        }
    }

    async generateProject(data) {
        const generateBtn = document.getElementById('generateBtn');
        this.setLoadingState(generateBtn, true);

        try {
            const response = await fetch(`${this.baseUrl}/create_project`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResults(result);
            this.showNotification('Project generated successfully! 🎉', 'success');

        } catch (error) {
            console.error('API Error:', error);
            this.showNotification(`API Error: ${error.message}`, 'error');
        } finally {
            this.setLoadingState(generateBtn, false);
        }
    }

    async runDemo() {
        console.log("Am I running???")
        const demoBtn = document.querySelector('.demo-btn');
        const originalText = demoBtn.textContent;
        demoBtn.textContent = 'Running Demo...';
        demoBtn.disabled = true;

        try {
            await this.generateProject({
                title: "AI-Powered Recipe Assistant",
                brief: "Create an AI assistant that helps users find recipes based on available ingredients and dietary preferences",
                time_hours: 24
            });
            this.showNotification('Demo completed! ✨', 'success');
        } catch (error) {
            console.error('Demo Error:', error);
            this.showNotification('Demo failed. Please check your connection.', 'error');
        } finally {
            demoBtn.textContent = originalText;
            demoBtn.disabled = false;
        }
    }

    displayResults(data) {
        const resultsSection = document.getElementById('resultsSection');
        const projectTitle = document.getElementById('projectTitle');
        const projectBrief = document.getElementById('projectBrief');
        const projectId = document.getElementById('projectId');
        const projectTime = document.getElementById('projectTime');
        const agentsGrid = document.getElementById('agentsGrid');

        // Populate project info
        projectTitle.textContent = data.title;
        projectBrief.textContent = data.brief;
        projectId.textContent = data.project_id;
        projectTime.textContent = data.time_hours || '24';

        // Clear and render agents as tabs with one visible card
        agentsGrid.innerHTML = '';
        this.renderTabbedAgents(data.agents);

        // If presentation agent has slides_link, show a download button at top
        const presentation = data.agents && data.agents.presentation;
        const slidesLink = presentation && (presentation.slides_link || (presentation.parsed && presentation.parsed.slides_link));
        this.renderSlidesDownload(slidesLink);
        this._lastProjectId = data.project_id;

        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    renderAgentNavigator(agents) {
        // legacy (kept in case of fallback); not used now
        const agentsGrid = document.getElementById('agentsGrid');
        this._agentsCache = agents;
        const agentConfigs = {
            ideation: {
                icon: 'fas fa-lightbulb',
                color: 'icon-ideation',
                title: 'Brainstorming Ideas'
            },
            research: {
                icon: 'fas fa-search',
                color: 'icon-research',
                title: 'Research & Discovery'
            },
            planning: {
                icon: 'fas fa-tasks',
                color: 'icon-planning',
                title: 'Project Planning'
            },
            coding: {
                icon: 'fas fa-code',
                color: 'icon-coding',
                title: 'Technical Implementation'
            },
            presentation: {
                icon: 'fas fa-presentation',
                color: 'icon-presentation',
                title: 'Presentation & Demo'
            }
        };

        // Determine first available agent index
        this.currentAgentIndex = 0;
        this.showAgentAtIndex(this.currentAgentIndex, agentConfigs);
    }

    renderTabbedAgents(agents) {
        const agentsGrid = document.getElementById('agentsGrid');
        const agentConfigs = {
            ideation: { icon: 'fas fa-lightbulb', color: 'icon-ideation', title: 'Brainstorming Ideas' },
            research: { icon: 'fas fa-search', color: 'icon-research', title: 'Research & Discovery' },
            planning: { icon: 'fas fa-tasks', color: 'icon-planning', title: 'Project Planning' },
            coding: { icon: 'fas fa-code', color: 'icon-coding', title: 'Technical Implementation' },
            presentation: { icon: 'fas fa-chalkboard', color: 'icon-presentation', title: 'Presentation & Demo' }
        };

        const tabs = document.createElement('div');
        tabs.className = 'tabs';
        agentsGrid.appendChild(tabs);

        const cards = {};

        this.agentOrder.forEach((name) => {
            if (!agents[name]) return;
            const data = agents[name];
            const config = agentConfigs[name];
            const card = this.createAgentCard(name, data, config);
            card.classList.add('agent-card');
            if (name !== 'ideation') card.classList.add('hidden');

            // Presentation tools
            if (name === 'presentation') {
                const toolbar = document.createElement('div');
                toolbar.className = 'slides-toolbar';
                toolbar.innerHTML = `<button class="slides-btn" data-action="open-slides">Present Slides</button>`;
                card.prepend(toolbar);
                toolbar.querySelector('[data-action="open-slides"]').addEventListener('click', () => {
                    this.presentSlides(data);
                });
            }

            // Coding tools
            if (name === 'coding') {
                const tools = document.createElement('div');
                tools.className = 'code-tools';
                tools.innerHTML = `
                    <input type="text" placeholder="Search (regex)" data-role="search" />
                    <input type="text" placeholder="Replace with" data-role="replace" />
                    <button class="btn secondary" data-action="search">Find</button>
                    <button class="btn" data-action="replace">Replace All</button>
                    <textarea placeholder="Describe the edit. e.g., Rename variable foo to userName" data-role="prompt"></textarea>
                    <button class="btn" data-action="apply-prompt">Apply Prompted Edit</button>
                    <button class="btn" data-action="save-artifact">Save Artifact</button>
                `;
                card.prepend(tools);
                this.wireCodeTools(tools, card, data);
            }

            const btn = document.createElement('button');
            btn.className = 'tab-btn' + (name === 'ideation' ? ' active' : '');
            btn.innerHTML = `<i class="${config.icon}"></i> ${name}`;
            btn.addEventListener('click', () => {
                Object.values(cards).forEach(c => c.classList.add('hidden'));
                card.classList.remove('hidden');
                tabs.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
            tabs.appendChild(btn);

            agentsGrid.appendChild(card);
            cards[name] = card;
        });
    }

    renderHorizontalAgents(agents) {
        const agentsGrid = document.getElementById('agentsGrid');
        const agentConfigs = {
            ideation: { icon: 'fas fa-lightbulb', color: 'icon-ideation', title: 'Brainstorming Ideas' },
            research: { icon: 'fas fa-search', color: 'icon-research', title: 'Research & Discovery' },
            planning: { icon: 'fas fa-tasks', color: 'icon-planning', title: 'Project Planning' },
            coding: { icon: 'fas fa-code', color: 'icon-coding', title: 'Technical Implementation' },
            presentation: { icon: 'fas fa-chalkboard', color: 'icon-presentation', title: 'Presentation & Demo' }
        };

        this.agentOrder.forEach((name) => {
            if (!agents[name]) return;
            const data = agents[name];
            const config = agentConfigs[name];
            const card = this.createAgentCard(name, data, config);
            if (name === 'presentation') {
                // add slides toolbar
                const toolbar = document.createElement('div');
                toolbar.className = 'slides-toolbar';
                toolbar.innerHTML = `
                    <button class="slides-btn" data-action="open-slides">Present Slides</button>
                `;
                card.prepend(toolbar);
                toolbar.querySelector('[data-action="open-slides"]').addEventListener('click', () => {
                    this.presentSlides(data);
                });
            }
            agentsGrid.appendChild(card);
        });
    }

    showAgentAtIndex(index, agentConfigs) {
        const agentsGrid = document.getElementById('agentsGrid');
        const name = this.agentOrder[index];
        const data = this._agentsCache[name];
        const config = agentConfigs[name];

        agentsGrid.innerHTML = '';

        // Navigation bar
        const nav = document.createElement('div');
        nav.className = 'agent-nav';
        nav.innerHTML = `
            <div class="nav-left">
                <button class="nav-btn" id="prevAgent"><i class="fas fa-arrow-left"></i> Prev</button>
            </div>
            <div class="nav-counter">${name} (${index + 1} / ${this.agentOrder.length})</div>
            <div class="nav-right">
                <button class="nav-btn" id="nextAgent">Next <i class="fas fa-arrow-right"></i></button>
            </div>
        `;
        agentsGrid.appendChild(nav);

        // Card
        const card = this.createAgentCard(name, data, config);
        agentsGrid.appendChild(card);

        // Wire buttons
        document.getElementById('prevAgent').onclick = () => this.prevAgent(agentConfigs);
        document.getElementById('nextAgent').onclick = () => this.nextAgent(agentConfigs);

        // Disable edges
        if (this.currentAgentIndex === 0) {
            document.getElementById('prevAgent').disabled = true;
        }
        if (this.currentAgentIndex === this.agentOrder.length - 1) {
            document.getElementById('nextAgent').disabled = true;
        }
    }

    prevAgent(agentConfigs) {
        if (this.currentAgentIndex > 0) {
            this.currentAgentIndex -= 1;
            this.showAgentAtIndex(this.currentAgentIndex, agentConfigs);
        }
    }

    nextAgent(agentConfigs) {
        if (this.currentAgentIndex < this.agentOrder.length - 1) {
            this.currentAgentIndex += 1;
            this.showAgentAtIndex(this.currentAgentIndex, agentConfigs);
        }
    }

    createAgentCard(agentName, agentData, config) {
        const card = document.createElement('div');
        card.className = 'agent-card fade-in';

        const hasError = agentData.error;
        const preferred = !hasError && (agentData.parsed ? agentData.parsed : null);
        const content = hasError ? agentData.error : (preferred || agentData.raw || 'No content generated');

        card.innerHTML = `
            <div class="agent-header">
                <div class="agent-icon ${config.color}">
                    <i class="${config.icon}"></i>
                </div>
                <h3 class="agent-title">${config.title}</h3>
            </div>
            <div class="agent-content">
                ${hasError ? 
                    `<div class="error-message">${content}</div>` :
                    `<pre><code>${this.formatContent(content)}</code></pre>`
                }
            </div>
        `;

        return card;
    }

    async presentSlides(presentationData) {
        // Build slides from structured JSON or markdown headings
        let slides = [];
        const parsed = presentationData && (presentationData.parsed || presentationData);
        const raw = presentationData && (presentationData.raw || presentationData);
        if (parsed && Array.isArray(parsed.slides_outline)) {
            slides = parsed.slides_outline;
        } else if (parsed && Array.isArray(parsed.slides)) {
            slides = parsed.slides;
        } else if (parsed && typeof parsed === 'object' && (parsed.slide_deck || parsed.deck)) {
            slides = parsed.slide_deck || parsed.deck;
        } else {
            const text = typeof raw === 'string' ? raw : JSON.stringify(raw, null, 2);
            const sections = text.split(/\n(?=##?\s)/g);
            slides = sections.map((sec) => {
                const lines = sec.split('\n');
                const header = lines[0].replace(/^#+\s*/, '') || 'Slide';
                const bullets = lines.slice(1).filter(Boolean);
                return { title: header, bullets };
            }).filter(s => s.title || (s.bullets && s.bullets.length));
            if (!slides.length) {
                slides = text.split(/\n\n+/).map((chunk, i) => ({ title: `Slide ${i + 1}`, bullets: chunk.split('\n') }));
            }
        }

        try {
            const resp = await fetch(`${this.baseUrl}/generate_slides`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ project_id: this._lastProjectId || 'demo', presentation: presentationData })
            });
            const { url } = await resp.json();
            window.open(url, '_blank');
        } catch (e) {
            // fallback to client-side
            const w = window.open('', '_blank');
            if (!w) {
                this.showNotification('Popup blocked. Allow popups to view slides.', 'error');
                return;
            }
            const html = this.buildSlidesHtml(slides);
            w.document.open();
            w.document.write(html);
            w.document.close();
        }
    }

    buildSlidesHtml(slides) {
        const slideItems = slides.map((s) => {
            const title = typeof s === 'string' ? s.split('\n')[0] : (s.title || '');
            const bullets = typeof s === 'string' ? s.split('\n').slice(1) : (s.bullets || s.points || []);
            const bulletsHtml = bullets.map(b => `<li>${this.escapeHtml(String(b))}</li>`).join('');
            return `
                <section class="slide">
                    <h2>${this.escapeHtml(title)}</h2>
                    <ul>${bulletsHtml}</ul>
                </section>
            `;
        }).join('');

        return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Presentation</title>
    <style>
        * { box-sizing: border-box; }
        html, body { margin:0; height:100%; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background:#0b1020; color:#fff; }
        .deck { height:100%; display:flex; overflow-x:auto; scroll-snap-type:x mandatory; }
        .slide { min-width:100%; height:100%; scroll-snap-align:start; padding:60px; display:flex; flex-direction:column; justify-content:center; gap:24px; background:radial-gradient(1200px 400px at 10% 10%, rgba(80,120,255,0.15), rgba(0,0,0,0)); }
        h2 { font-size:56px; margin:0 0 12px 0; line-height:1.1; }
        ul { list-style: disc inside; font-size:24px; line-height:1.6; opacity:0.95; }
        .help { position:fixed; bottom:16px; right:20px; opacity:0.7; font-size:14px; }
    </style>
    <script>
        document.addEventListener('keydown', (e) => {
            const container = document.querySelector('.deck');
            if (!container) return;
            if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') container.scrollBy({ left: window.innerWidth, behavior: 'smooth' });
            if (e.key === 'ArrowLeft' || e.key === 'PageUp') container.scrollBy({ left: -window.innerWidth, behavior: 'smooth' });
            if (e.key === 'f') document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
        });
    </script>
</head>
<body>
    <div class="deck">${slideItems}</div>
    <div class="help">Use ← / → to navigate, Space to advance, F for fullscreen</div>
</body>
</html>`;
    }

    escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    formatContent(content) {
        // Basic formatting for JSON and text content
        try {
            // Try to parse and pretty-print JSON
            const parsed = typeof content === 'string' ? JSON.parse(content) : content;
            return JSON.stringify(parsed, null, 2);
        } catch {
            // If not JSON, just return the content as-is
            return content;
        }
    }

    wireCodeTools(tools, card, agentData) {
        const pre = card.querySelector('pre');
        const codeEl = card.querySelector('code');
        if (!pre || !codeEl) return;

        const getText = () => codeEl.textContent;
        const setText = (t) => { codeEl.textContent = t; };

        const onSearch = () => {
            const pattern = tools.querySelector('[data-role="search"]').value;
            if (!pattern) return;
            try {
                const regex = new RegExp(pattern, 'gi');
                const raw = getText();
                const highlighted = raw.replace(regex, (m) => `<<<H>>>${m}<<<H>>>`);
                codeEl.innerHTML = this.escapeHtml(highlighted)
                    .replaceAll('&lt;&lt;&lt;H&gt;&gt;&gt;', '<span class="highlight">')
                    .replaceAll('&lt;&lt;&lt;/H&gt;&gt;&gt;', '</span>');
            } catch (e) {
                this.showNotification('Invalid regex pattern', 'error');
            }
        };

        const onReplace = () => {
            const pattern = tools.querySelector('[data-role="search"]').value;
            const replacement = tools.querySelector('[data-role="replace"]').value;
            if (!pattern) return;
            try {
                const regex = new RegExp(pattern, 'g');
                const updated = getText().replace(regex, replacement);
                setText(updated);
                this.showNotification('Replaced all occurrences', 'success');
            } catch (e) {
                this.showNotification('Invalid regex pattern', 'error');
            }
        };

        const onApplyPrompt = () => {
            const prompt = tools.querySelector('[data-role="prompt"]').value.trim();
            if (!prompt) return;
            const text = getText();
            let updated = text;
            const renameMatch = prompt.match(/rename\s+variable\s+(\w+)\s+to\s+(\w+)/i);
            if (renameMatch) {
                const from = renameMatch[1];
                const to = renameMatch[2];
                updated = updated.replace(new RegExp(`\\b${from}\\b`, 'g'), to);
            }
            const replaceMatch = prompt.match(/replace\s+text\s+"([\s\S]+?)"\s+with\s+"([\s\S]+?)"/i);
            if (replaceMatch) {
                const from = replaceMatch[1];
                const to = replaceMatch[2];
                updated = updated.split(from).join(to);
            }
            if (updated !== text) {
                setText(updated);
                this.showNotification('Applied prompted edit', 'success');
            } else {
                this.showNotification('No change from prompt', 'info');
            }
        };

        tools.querySelector('[data-action="search"]').addEventListener('click', onSearch);
        tools.querySelector('[data-action="replace"]').addEventListener('click', onReplace);
        tools.querySelector('[data-action="apply-prompt"]').addEventListener('click', onApplyPrompt);

        const onSave = async () => {
            const filename = 'coding-agent.txt';
            const content = codeEl.textContent;
            try {
                const resp = await fetch(`${this.baseUrl}/save_code`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ project_id: this._lastProjectId || 'demo', filename, content })
                });
                const { url } = await resp.json();
                this.showNotification('Saved artifact. Opening...', 'success');
                window.open(url, '_blank');
            } catch (e) {
                this.showNotification('Failed to save artifact', 'error');
            }
        };
        tools.querySelector('[data-action="save-artifact"]').addEventListener('click', onSave);
    }

    renderSlidesDownload(slidesLink) {
        // Remove existing if any
        let existing = document.getElementById('slidesDownloadContainer');
        if (existing) existing.remove();

        const resultsSection = document.getElementById('resultsSection');
        if (!resultsSection) return;

        const container = document.createElement('div');
        container.id = 'slidesDownloadContainer';
        container.style.margin = '1rem 0 2rem 0';

        if (slidesLink) {
            container.innerHTML = `
                <a href="${slidesLink}" target="_blank" rel="noopener" class="demo-btn">
                    <i class="fas fa-file-powerpoint"></i> Download Slides
                </a>
            `;
        } else {
            container.innerHTML = `
                <div style="color:#718096; font-size:0.95rem;">
                    <i class="fas fa-info-circle"></i> Slides link will appear here if the model provides one.
                </div>
            `;
        }

        const header = resultsSection.querySelector('.results-header');
        if (header) {
            resultsSection.insertBefore(container, header.nextSibling);
        } else {
            resultsSection.prepend(container);
        }
    }

    setLoadingState(button, isLoading) {
        const btnText = button.querySelector('.btn-text');
        const spinner = button.querySelector('.loading-spinner');

        if (isLoading) {
            btnText.style.display = 'none';
            spinner.style.display = 'flex';
            button.disabled = true;
        } else {
            btnText.style.display = 'block';
            spinner.style.display = 'none';
            button.disabled = false;
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;

        // Add styles
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: type === 'success' ? '#4ade80' : type === 'error' ? '#f87171' : '#60a5fa',
            color: 'white',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.2)',
            zIndex: '1000',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontWeight: '500',
            maxWidth: '300px',
            animation: 'slideInRight 0.3s ease'
        });

        // Add keyframe for animation
        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        // Auto remove after 4 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
}

// Utility functions
function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'none';
    
    // Reset form
    document.getElementById('projectForm').reset();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.hackAIApp = new HackAIApp();
    
    // Add some nice animations on load
    setTimeout(() => {
        document.querySelector('.input-card').classList.add('success-shake');
    }, 1000);
});

// Add some interactive effects
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to cards
    document.addEventListener('mouseover', (e) => {
        if (e.target.closest('.agent-card')) {
            e.target.closest('.agent-card').style.transform = 'translateY(-4px) scale(1.02)';
        }
    });

    document.addEventListener('mouseout', (e) => {
        if (e.target.closest('.agent-card')) {
            e.target.closest('.agent-card').style.transform = 'translateY(0) scale(1)';
        }
    });
});


