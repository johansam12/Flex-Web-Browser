import os
from google import genai
from google.genai import types

# This looks for a key named 'GEMINI_API_KEY' on the user's system
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # This helps the recruiter understand why it isn't working
    print("Error: GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

def get_ai_research(query):
    try:
        # We enable 'google_search' so the AI can improvise with real-time data
        search_tool = types.Tool(google_search=types.GoogleSearch())
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are an AI Browser Research Assistant. Analyze this search query and provide a cited summary: {query}",
            config=types.GenerateContentConfig(tools=[search_tool])
        )
        return response.text
    except Exception as e:

        return f"AI Research Error: {str(e)}"
