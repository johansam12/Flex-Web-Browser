from google import genai
from google.genai import types

# REPLACE WITH YOUR ACTUAL KEY
client = genai.Client(api_key="AIzaSyCa7ZqR4DSvanjOBrrrlvZCrMccbUw6Bdc") 

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