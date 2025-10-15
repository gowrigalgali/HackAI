# file: hackai/orchestrator.py

import asyncio
import hashlib
import json
import os
from typing import Any

import httpx
import redis.asyncio as aioredis
from fastapi import FastAPI, Body
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Config
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Validate configuration
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required. Please set it in your .env file or environment.")

# FastAPI app and Redis client
app = FastAPI(title="HackAI Orchestrator", description="AI-powered project generation system")

# Mount static files
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# in orchestrator.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:8000"] for more restrictive
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend page"""
    return FileResponse('static/index.html')

@app.get("/demo")
async def demo_endpoint():
    """Return sample demo data for testing frontend"""
    return {
        "project_id": "demo123",
        "title": "AI-Powered Recipe Assistant",
        "brief": "Create an AI assistant that helps users find recipes based on available ingredients and dietary preferences",
        "agents": {
            "ideation": {
                "raw": """
[
  {
    "title": "SmartFridge: Intelligent Food Management System",
    "pitch": "SmartFridge uses computer vision to track refrigerator contents and AI to suggest recipes, prevent food waste, and create smart shopping lists. Scan grocery items as you put them away, and the app learns your preferences while helping you use everything before it expires.",
    "tech": "Computer Vision APIs (Google Vision, AWS Rekognition), React Native, Firebase, Machine Learning (TensorFlow), Optical Character Recognition",
    "novelty": "Combines real-world inventory tracking with intelligent meal planning and waste reduction algorithms."
  },
  {
    "title": "FlavorMatch: AI Recipe Recommendation Engine",
    "pitch": "FlavorMatch analyzes user dietary restrictions, taste preferences, and current pantry contents to recommend personalized recipes. The app learns from user ratings and can suggest ingredient substitutions based on nutritional goals and flavor profiles.",
    "tech": "Python/FastAPI, PostgreSQL, Redis (caching), Scikit-learn (recommendation algorithms), Spoonacular API, Nutritional database APIs",
    "novelty": "Advanced recommendation system that considers multiple user factors including nutrition, taste, and ingredient availability."
  },
  {
    "title": "FreshAI: Real-time Cooking Assistant",
    "pitch": "FreshAI provides voice-guided cooking instructions with ingredient substitution suggestions and real-time nutritional feedback. Use voice commands to navigate recipes while cooking, get portion adjustments, and allergy-safe alternatives.",
    "tech": "Speech recognition (Web Speech API), Natural Language Processing (OpenAI API), Android/iOS, Real-time audio processing, Nutritional data APIs",
    "novelty": "Hands-free cooking experience with intelligent ingredient flexibility and dietary accommodation."
  }
]
"""
            },
            "research": {
                "raw": """
{
  "research_papers": [
    {
      "title": "Deep Learning for Recipe Recommendation",
      "url": "https://arxiv.org/abs/1906.01472",
      "summary": "Paper exploring neural collaborative filtering for food recommendation systems, analyzing user preferences and ingredient compatibility."
    },
    {
      "title": "Computer Vision for Food Recognition",
      "url": "https://ieeexplore.ieee.org/document/9123456",
      "summary": "Technical implementation of food item classification using convolutional neural networks with high accuracy rates."
    }
  ],
  "apis_and_services": [
    {"name": "Spoonacular API", "description": "Recipe search, nutrition data, ingredient analysis"},
    {"name": "Edamam Recipe API", "description": "Recipe database with nutritional information"},
    {"name": "FoodData Central API", "description": "USDA nutritional database for ingredients"}
  ],
  "recommended_libraries": [
    {"name": "scikit-learn", "description": "Machine learning algorithms for recommendation systems"},
    {"name": "Pandas", "description": "Data manipulation for recipe and nutrition data"},
    {"name": "TensorFlow Lite", "description": "Mobile-optimized ML inference"}
  ]
}
"""
            },
            "planning": {
                "raw": """
{
  "project_timeline": "24 hours",
  "development_phases": [
    {
      "phase": "Setup & Requirements (4 hours)",
      "tasks": [
        "Environment setup and project scaffolding",
        "API research and integration planning", 
        "Database design and schema creation",
        "Basic UI wireframing"
      ]
    },
    {
      "phase": "Core Development (12 hours)",
      "tasks": [
        "Build recipe search and filtering system",
        "Implement user preference tracking",
        "Create recommendation algorithm",
        "Develop ingredient substitution logic",
        "Build responsive web interface"
      ]
    },
    {
      "phase": "Integration & Testing (6 hours)",
      "tasks": [
        "API integration testing",
        "User interface testing and refinement",
        "Performance optimization",
        "Documentation and deployment prep"
      ]
    }
  ],
  "tech_stack": ["Python/FastAPI", "React.js", "PostgreSQL", "Redis", "Docker"],
  "team_roles": ["Full-stack Developer", "UI/UX Designer (optional)"],
  "success_metrics": ["Recipe recommendation accuracy", "User engagement time", "Successful ingredient matches"]
}
"""
            },
            "coding": {
                "raw": """
# Project: AI Recipe Assistant

## Repository Structure
```
ai-recipe-assistant/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── routes/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
├── README.md
└── docker-compose.yml
```

## Backend Implementation (FastAPI + Python)

### app/models/recipe.py
```python
from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    nutrition = Column(JSON)
    cuisine_type = Column(String)
    diet_labels = Column(JSON)
```

### app/services/recommendation.py
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecipeRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def get_recommendations(self, user_ingredients, preferences):
        # Implementation of recommendation algorithm
        pass
```

## Frontend Implementation (React)

### src/components/RecipeSearch.js
```jsx
import React, { useState } from 'react';

const RecipeSearch = () => {
    const [ingredients, setIngredients] = useState([]);
    const [preferences, setPreferences] = useState({});
    
    return (
        <div className="recipe-search">
            <input 
                placeholder="Enter ingredients..."
                onChange={(e) => setIngredients(e.target.value.split(','))}
            />
            <button onClick={handleSearch}>Find Recipes</button>
        </div>
    );
};

export default RecipeSearch;
```

## Deployment with Docker

### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/recipes
  
 the frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=recipes
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```
"""
            },
            "presentation": {
                "raw": """
# AI Recipe Assistant Demo Presentation

## Slide 1: The Problem
**"60% of food is wasted due to poor meal planning"**
- Users struggle to find recipes matching their available ingredients
- Difficulty accommodating dietary restrictions
- Lack of personalized recommendations leads to meal monotony

## Slide 2: Our Solution
**"Smart Recipe Matching with AI Intelligence"**
- Input your available ingredients
- Receive personalized recipe suggestions
- Get dietary-compliant alternatives
- Track nutritional information in real-time

## Slide 3: Key Features
- 🔍 **Smart Ingredient Matching**: Find recipes using what you have
- 🎯 **Personalized Recommendations**: AI learns your taste preferences  
- 🚫 **Dietary Filtering**: Allergen and dietary restriction support
- 📱 **Mobile-Optimized**: Voice commands for hands-free cooking
- 📊 **Nutrition Tracking**: Real-time nutritional analysis

## Slide 4: Live Demo Demo Script

**"Let me show you how it works..."**

1. **Enter Ingredients**: "I have chicken, broccoli, tomatoes, and rice"
2. **Show Results**: AI suggests "Teriyaki Chicken Bowl" with substitution options
3. **Apply Filters**: Filter for "low-carb" dietary preference
4. **Voice Feature**: Demonstrate hands-free ingredient addition
5. **Nutrition Panel**: Show real-time nutritional breakdown

## Slide 5: Technical Implementation
- **Backend**: FastAPI + PostgreSQL + Redis caching
- **ML Engine**: Collaborative filtering + content-based recommendations
- **APIs**: Spoonacular food database + USDA nutritional data
- **Frontend**: React.js with responsive design
- **Deployment**: Docker containers on cloud infrastructure

## Slide 6: Impact & Future
- **Target Users**: 25-45 demographic seeking meal variety
- **Market Opportunity**: $3B+ food tech industry growth
- **Next Steps**: Mobile app development, smart kitchen integration
- **Vision**: Become the go-to platform for intelligent meal planning

## Demo Tips:
- Keep demo under 3 minutes
- Use real ingredients for authenticity  
- Prepare backup demo data
- Highlight unique AI features
"""
            }
        }
    }

# Initialize Redis client
redis = aioredis.from_url(REDIS_URL)

@app.on_event("startup")
async def startup_event():
    """Test Redis connection on startup"""
    try:
        await redis.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("⚠️  Running without Redis caching...")


# Gemini client
class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    async def generate(self, prompt: str, max_tokens: int = 1024):
        """Generate content using Gemini API"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        params = {"key": self.api_key}
        headers = {"Content-Type": "application/json"}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                r = await client.post(self.url, json=payload, headers=headers, params=params)
                r.raise_for_status()
                data = r.json()
                    
                candidates = data.get("candidates", [])
                if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                    
                return "No response generated"
                
            except httpx.HTTPStatusError as e:
                raise Exception(f"API request failed: HTTP {e.response.status_code}")
            except Exception as e:
                raise Exception(f"Generation failed: {str(e)}")


llm = GeminiClient(GEMINI_API_KEY)


# Redis helpers
async def cache_get(key: str):
    val = await redis.get(key)
    if val:
        return json.loads(val)
    return None


async def cache_set(key: str, value: Any, ttl: int = 3600):
    await redis.set(key, json.dumps(value), ex=ttl)


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()


def try_parse_json(text: str):
    """Best-effort JSON extraction from LLM text. Returns parsed object or None."""
    if not text or not isinstance(text, str):
        return None
    # Quick direct parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Extract from code fences
    fences = ["```json", "```", "\n```"]
    start_idx = -1
    for fence in fences:
        i = text.find(fence)
        if i != -1:
            start_idx = i + len(fence)
            break
    if start_idx != -1:
        end = text.find("```", start_idx)
        if end != -1:
            candidate = text[start_idx:end].strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass
    # Heuristic: take first JSON-looking substring
    first_brace = text.find("{")
    first_bracket = text.find("[")
    starts = [x for x in [first_brace, first_bracket] if x != -1]
    if not starts:
        return None
    start = min(starts)
    # Try progressively trimming from end
    for end in range(len(text), start + 1, -1):
        candidate = text[start:end].strip()
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except Exception:
            continue
    return None


# Request model
class ProjectRequest(BaseModel):
    title: str
    brief: str
    time_hours: int = 24


async def planner_agent(project_id: str, brief: str, time_hours: int):
    prompt = (
        f"Plan tasks for the project based on the brief: {brief}. "
        f"Return a JSON with keys: nodes (list of tasks with id, title, description, estimate_hours), "
        f"and edges (list of {{from,to}}). Budget {time_hours} hours."
    )
    key = f"hackmate:{project_id}:planner:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


async def evaluator_agent(project_id: str, title: str, brief: str):
    prompt = (
        f"Evaluate the project idea '{title}'. Brief: {brief}. Return JSON with keys: risks (list), feasibility (low/medium/high), impact (1-10), recommendations (list)."
    )
    key = f"hackmate:{project_id}:evaluator:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out
async def ideation_agent(project_id: str, brief: str):
    prompt = (
        f"You are an ideation assistant. Given the brief:\n{brief}\n"
        f"Produce 6 distinct hackathon project ideas as JSON list of "
        f"{{title, pitch, tech, novelty}}."
    )
    key = f"hackmate:{project_id}:ideation:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


async def research_agent(project_id: str, idea: str):
    prompt = (
        f"Research for idea: {idea}. Provide 5 papers or URLs, 3 APIs, "
        f"3 libraries, short summaries in JSON."
    )
    key = f"hackmate:{project_id}:research:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


async def planning_agent(project_id: str, idea: str, time_hours: int):
    prompt = (
        f"Plan a roadmap for idea {idea} in {time_hours} hours: milestones, "
        f"tasks, owners, estimates in JSON."
    )
    key = f"hackmate:{project_id}:planning:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


async def coding_agent(project_id: str, idea: str):
    prompt = f"Generate a starter repo for idea {idea}: README, requirements, app.py skeleton and one example file."
    key = f"hackmate:{project_id}:coding:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


async def presentation_agent(project_id: str, idea: str):
    prompt = (
        f"Create 6 slide outlines and a 200-word pitch for {idea}. Include demo script and resources. "
        f"Return a JSON object with keys: slides_outline, pitch, demo_script, resources. "
        f"If possible, also create shareable slides and include a publicly accessible PPTX download URL as 'slides_link'. "
        f"If not possible, set 'slides_link' to null."
    )
    key = f"hackmate:{project_id}:presentation:{prompt_hash(prompt)}"
    cached = await cache_get(key)
    if cached:
        return cached
    try:
        text = await llm.generate(prompt)
        parsed = try_parse_json(text)
        out = {"raw": text}
        if parsed is not None:
            out["parsed"] = parsed
            # Bubble up a potential slides link if present
            slides_link = parsed.get("slides_link") if isinstance(parsed, dict) else None
            if slides_link:
                out["slides_link"] = slides_link
    except Exception as e:
        out = {"error": str(e)}
    await cache_set(key, out)
    return out


# Main endpoint
@app.post("/create_project")
async def create_project(req: ProjectRequest):
    project_id = hashlib.sha1((req.title + req.brief).encode()).hexdigest()[:8]

    tasks = [
        asyncio.create_task(planner_agent(project_id, req.brief, req.time_hours)),
        asyncio.create_task(ideation_agent(project_id, req.brief)),
        asyncio.create_task(research_agent(project_id, req.brief)),
        asyncio.create_task(planning_agent(project_id, req.brief, req.time_hours)),
        asyncio.create_task(coding_agent(project_id, req.brief)),
        asyncio.create_task(presentation_agent(project_id, req.brief)),
        asyncio.create_task(evaluator_agent(project_id, req.title, req.brief)),
    ]
    results = await asyncio.gather(*tasks)

    agg = {
        "project_id": project_id,
        "title": req.title,
        "brief": req.brief,
        "time_hours": req.time_hours,
        "agents": {
            "planner": results[0],
            "ideation": results[1],
            "research": results[2],
            "planning": results[3],
            "coding": results[4],
            "presentation": results[5],
            "evaluator": results[6],
        },
    }

    await cache_set(f"hackmate:{project_id}:aggregate", agg, ttl=24 * 3600)
    return agg


# Artifacts helpers and endpoints
def ensure_artifacts_dir(project_id: str) -> str:
    base = os.path.join("static", "artifacts", project_id)
    os.makedirs(base, exist_ok=True)
    return base


class SlidesRequest(BaseModel):
    project_id: str
    presentation: Any


@app.post("/generate_slides")
async def generate_slides(req: SlidesRequest):
    project_dir = ensure_artifacts_dir(req.project_id)
    slides_html_path = os.path.join(project_dir, "slides.html")

    # Build simple HTML from parsed structure or raw text
    pres = req.presentation or {}
    parsed = pres.get("parsed") if isinstance(pres, dict) else None
    raw = pres.get("raw") if isinstance(pres, dict) else pres
    slides = []
    if parsed and isinstance(parsed, dict):
        if isinstance(parsed.get("slides_outline"), list):
            slides = parsed["slides_outline"]
        elif isinstance(parsed.get("slides"), list):
            slides = parsed["slides"]
        elif isinstance(parsed.get("slide_deck"), list):
            slides = parsed["slide_deck"]
    if not slides:
        text = raw if isinstance(raw, str) else json.dumps(raw, indent=2)
        sections = [s for s in (text or "").split("\n## ") if s]
        for idx, sec in enumerate(sections or [text]):
            lines = sec.split("\n")
            title = lines[0].strip() if lines and idx < len(sections) else f"Slide {idx+1}"
            bullets = [l.strip() for l in lines[1:] if l.strip()]
            slides.append({"title": title, "bullets": bullets})

    def escape(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    items = []
    for s in slides:
        title = escape(str(s if isinstance(s, str) else s.get("title", "")))
        bullets = s if isinstance(s, str) else s.get("bullets", [])
        lis = "".join(f"<li>{escape(str(b))}</li>" for b in bullets)
        items.append(f"<section class=\"slide\"><h2>{title}</h2><ul>{lis}</ul></section>")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Presentation</title>
<style>
*{{{{box-sizing:border-box}}}}
html,body{{{{margin:0;height:100%;font-family:Inter,-apple-system,Segoe UI,Roboto,sans-serif;background:#0b1020;color:#fff}}}}
.deck{{{{height:100%;display:flex;overflow-x:auto;scroll-snap-type:x mandatory}}}}
.slide{{{{min-width:100%;height:100%;scroll-snap-align:start;padding:60px;display:flex;flex-direction:column;justify-content:center;gap:24px;background:radial-gradient(1200px 400px at 10% 10%, rgba(80,120,255,.15), rgba(0,0,0,0))}}}}
h2{{{{font-size:56px;margin:0 0 12px 0;line-height:1.1}}}}
ul{{{{list-style:disc inside;font-size:24px;line-height:1.6;opacity:.95}}}}
.help{{{{position:fixed;bottom:16px;right:20px;opacity:.7;font-size:14px}}}}
</style>

<script>
document.addEventListener('keydown', e => {{
    const c = document.querySelector('.deck');
    if (!c) return;
    if (['ArrowRight','PageDown',' '].includes(e.key))
        c.scrollBy({{ left: window.innerWidth, behavior: 'smooth' }});
    if (['ArrowLeft','PageUp'].includes(e.key))
        c.scrollBy({{ left: -window.innerWidth, behavior: 'smooth' }});
    if (e.key === 'f' && document.documentElement.requestFullscreen)
        document.documentElement.requestFullscreen();
}});
</script>
</head>
<body>
<div class='deck'>{"".join(items)}</div>
<div class='help'>Use ←/→ or Space. F for fullscreen.</div>
</body>
</html>"""


    with open(slides_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    url = f"/static/artifacts/{req.project_id}/slides.html"
    return {"url": url}


class SaveCodeRequest(BaseModel):
    project_id: str
    filename: str | None = None
    content: str


@app.post("/save_code")
async def save_code(req: SaveCodeRequest):
    project_dir = ensure_artifacts_dir(req.project_id)
    name = req.filename or "code.txt"
    safe_name = "".join(c for c in name if c.isalnum() or c in ("-", "_", ".")) or "code.txt"
    path = os.path.join(project_dir, safe_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(req.content)
    url = f"/static/artifacts/{req.project_id}/{safe_name}"
    return {"url": url}
