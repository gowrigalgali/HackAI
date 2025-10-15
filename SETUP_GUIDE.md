# HackAI Setup Guide

## Issue Fixed: HTTP 400 Bad Request Errors

The HTTP 400 Bad Request errors you were experiencing were caused by several issues in the Gemini API integration:

### Problems Identified and Fixed:

1. **Incorrect API Key Authentication**: The original code used `X-goog-api-key` header, but Gemini API expects the key as a query parameter
2. **Malformed Request Payload**: The payload structure didn't match Gemini API requirements
3. **Incorrect Response Parsing**: The code wasn't properly extracting the generated text from the API response
4. **Missing Environment Variable**: No `.env` file was set up for API key configuration

### Changes Made:

1. **Fixed API Request Structure**:
   ```python
   # Before (incorrect)
   headers = {"X-goog-api-key": self.api_key}
   
   # After (correct)
   params = {"key": self.api_key}
   headers = {"Content-Type": "application/json"}
   ```

2. **Updated Payload Format**:
   ```python
   payload = {
       "contents": [{"parts": [{"text": prompt}]}],
       "generationConfig": {
           "maxOutputTokens": max_tokens,
           "temperature": 0.7,
           "topP": 0.8,
           "topK": 10
       }
   }
   ```

3. **Fixed Response Parsing**:
   - Properly navigates the nested response structure
   - Extracts text from `candidates[0].content.parts[0].text`
   - Added fallback error handling

4. **Added Configuration Validation**:
   - Checks for required `GEMINI_API_KEY` on startup
   - Validates Redis connection
   - Better error messages for debugging

## Setup Instructions:

### 1. Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Install required packages (if not already installed)
pip install fastapi uvicorn httpx redis python-dotenv google-generativeai
```

### 2. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
nano .env
```

Add your Gemini API key to the `.env` file:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
REDIS_URL=redis://localhost:6379/0
```

### 3. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

### 4. Install Redis (Optional - for caching)
Since Redis is used for caching responses, you can either:
- Install Redis locally: `brew install redis` (macOS) or `sudo apt install redis` (Ubuntu)
- Or comment out redis-related code if you don't need caching

### 5. Run the Application
```bash
# Start the FastAPI server
uvicorn orchestrator:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API
```bash
curl -X POST "http://localhost:800<｜tool▁call▁begin｜>
create_project" \
-H "Content-Type: application/json" \
-d '{
  "title": "Test Project",
  "brief": "Create a simple web app"
}'
```

## API Endpoints:

- **POST** `/create_project` - Generate AI-powered project suggestions
- **GET** `/docs` - Interactive API documentation (FastAPI auto-generated)

## Next Steps:

1. Get your Gemini API key from Google AI Studio
2. Add it to your `.env` file
3. Test the API endpoint
4. All agents (ideation, research, planning, coding, presentation) should now work without 400 errors!

The system will now properly communicate with Google's Gemini 2.0 Flash API and return structured project recommendations.



