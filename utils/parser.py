"""
Weather data parser module.
Handles parsing and validation of weather API responses.
"""

from typing import Dict, Any


class WeatherParser:
    """Parser for weather API responses."""
    
    def parse_weather_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw weather API response into structured format."""
        # Extract city name from raw_data.get('name')
        city = raw_data.get('name')
        # Extract country from raw_data.get('sys', {}).get('country')
        country = raw_data.get('sys', {}).get('country')
        # Extract temperature from raw_data.get('main', {}).get('temp')
        temperature = raw_data.get('main', {}).get('temp')
        # Extract feels_like from raw_data.get('main', {}).get('feels_like')
        feels_like = raw_data.get('main', {}).get('feels_like')
        # Extract humidity from raw_data.get('main', {}).get('humidity')
        humidity = raw_data.get('main', {}).get('humidity')
        # Extract description from raw_data.get('weather', [])[0].get('description')
        description = raw_data.get('weather', [])[0].get('description')
        # Extract wind_speed from raw_data.get('wind', {}).get('speed')
        wind_speed = raw_data.get('wind', {}).get('speed')
        # Return dictionary with all extracted data
        return {
            "city": city,
            "country": country,
            "temperature": temperature,
            "feels_like": feels_like,
            "humidity": humidity,
            "description": description,
            "wind_speed": wind_speed
        }

    def validate_weather_data(self, weather_data: Dict[str, Any]) -> bool:
        """Validate that weather data has required fields."""
        # Check if required fields exist and are not None
        required_fields = ['city', 'temperature', 'description', 'humidity', 'wind_speed']
        for field in required_fields:
            if field not in weather_data or weather_data[field] is None:
                return False
        # Return True if all fields are present, False otherwise
        return True

    def format_weather_for_llm(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data for LLM prompt."""
        # Create formatted string with weather information
        formatted = (
            f"City: {weather_data.get('city', 'N/A')}\n"
            f"Country: {weather_data.get('country', 'N/A')}\n"
            f"Temperature: {weather_data.get('temperature', 'N/A')}°C\n"
            f"Feels Like: {weather_data.get('feels_like', 'N/A')}°C\n"
            f"Description: {weather_data.get('description', 'N/A')}\n"
            f"Humidity: {weather_data.get('humidity', 'N/A')}%\n"
            f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s\n"
        )
        return formatted
        # Return formatted string
    def parse(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate raw weather data."""
        parsed_data = self.parse_weather_data(raw_data)
        if not self.validate_weather_data(parsed_data):
            raise ValueError("Invalid weather data - missing required fields")
        return parsed_data
