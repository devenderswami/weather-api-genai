import os
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from utils.config import SYSTEM_PROMPT
from utils.parser import WeatherParser
import google.generativeai as genai

#  Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


class WeatherAPIClient:
    """Client for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Initialize API key from parameter or env var WEATHER_API_KEY
        self.api_key = api_key or WEATHER_API_KEY
        # Raise ValueError if no key
        if not self.api_key:
            raise ValueError("No API key provided")
        # Set base URL for weather API
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather data for a given city."""
        #  Make HTTP GET request to weather API
        response = requests.get(self.base_url, params={
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        })
        # Handle HTTP errors (401, 404, 429, etc.)
        if response.status_code == 401:
            raise ValueError("Invalid API key")
        elif response.status_code == 404:
            raise ValueError("City not found")
        elif response.status_code == 429:
            raise ValueError("Rate limit exceeded")
        # Handle network errors and timeouts
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError("Error fetching weather data") from e


class LLMClient:
    """Client for calling Gemini API to generate weather insights."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Initialize API key from parameter or env var GEMINI_API_KEY
        self.api_key = api_key or GEMINI_API_KEY
        # Raise ValueError if no key
        if not self.api_key:
            raise ValueError("No API key provided")
        # Configure Gemini API
        genai.configure(api_key=self.api_key)

    def generate_insights(self, weather_data: Dict[str, Any]) -> str:
        """Generate weather insights and recommendations using LLM."""
        try:
            # Format weather data for LLM prompt
            weather_info = json.dumps(weather_data, indent=2)
            prompt = SYSTEM_PROMPT.replace("{weather_data}", weather_info)
            
            # Initialize the model (use correct model name)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Generate content
            response = model.generate_content(prompt)
            
            # Clean the response - remove markdown code blocks if present
            cleaned_response = response.text.strip()
            
            # Remove ```json at the start
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:].strip()
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:].strip()
                
            # Remove ``` at the end
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3].strip()
          
            
            # Return cleaned insights
            return cleaned_response
        except Exception as e:
            raise ValueError(f"Error generating insights: {str(e)}") from e


class WeatherAssistant:
    """Main assistant that coordinates weather data fetching and insights generation."""
    
    def __init__(self):
        # Initialize weather API client
        self.weather_client = WeatherAPIClient()
        # Initialize LLM client
        self.llm_client = LLMClient()
        #Initialize weather parser
        self.parser = WeatherParser()
   
    
    def get_weather_insights(self, city: str) -> Dict[str, Any]:
        """Get weather data and generate insights for a given city."""
        # Fetch weather data from API
        weather_data = self.weather_client.get_weather(city)
        # Parse and validate weather data
        parsed_data = self.parser.parse(weather_data)
        # Generate insights using LLM
        insights = self.llm_client.generate_insights(parsed_data)
        # Handle all possible errors gracefully
        # Parse insights into structured format (e.g., JSON)
        # For simplicity, assume insights is already structured
        try:
            structured_insights = json.loads(insights)
            return structured_insights
        except json.JSONDecodeError:
            raise ValueError("Error parsing insights - AI response is not valid JSON")             
        


def main():
    """Main function to demonstrate the weather assistant functionality."""
    test_cities = [
        "London",
        "New York", 
        "Tokyo",
        "Paris",
        "Sydney"
    ]
    
    print("Weather Data Parser & API Assistant")
    print("=" * 50)
    
    assistant = WeatherAssistant()
    
    for city in test_cities:
        print(f"\nGetting weather insights for {city}...")
        try:
            result = assistant.get_weather_insights(city)
            print(f"Temperature: {result.get('temperature', 'N/A')}°C")
            print(f"Description: {result.get('description', 'N/A')}")
            print(f"Recommendation: {result.get('recommendation', 'N/A')}")
            print(f"Insights: {result.get('insights', 'N/A')}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)


if __name__ == "__main__":
    main()
