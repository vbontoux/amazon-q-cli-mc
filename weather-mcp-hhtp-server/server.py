from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get API key from environment variable
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

@app.get("/health/")
async def tools(request: Request):
    """Return the list of available tools."""
    return "Hello"


@app.post("/mcp/v1/tools")
async def tools(request: Request):
    """Return the list of available tools."""
    return {
        "tools": [
            {
                "name": "get_weather",
                "description": "Get the current weather and forecast for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name or location to get weather for"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days for the forecast (1-3)",
                            "default": 1
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
    }

@app.post("/mcp/v1/execute")
async def execute(request: Request):
    """Execute a tool."""
    data = await request.json()
    
    if data.get("name") != "get_weather":
        raise HTTPException(status_code=400, detail="Unknown tool")
    
    params = data.get("parameters", {})
    location = params.get("location")
    days = params.get("days", 1)
    
    if not location:
        return JSONResponse(
            status_code=400,
            content={"error": "Location parameter is required"}
        )
    
    if not WEATHER_API_KEY:
        return JSONResponse(
            status_code=500,
            content={"error": "Weather API key not configured"}
        )
    
    try:
        # Call the WeatherAPI.com service
        response = requests.get(
            f"https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": WEATHER_API_KEY,
                "q": location,
                "days": min(days, 3),
                "aqi": "no"
            }
        )
        
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": f"Weather API error: {response.text}"}
            )
        
        weather_data = response.json()
        
        # Format the response
        result = {
            "location": f"{weather_data['location']['name']}, {weather_data['location']['country']}",
            "current": {
                "temperature_c": weather_data['current']['temp_c'],
                "temperature_f": weather_data['current']['temp_f'],
                "condition": weather_data['current']['condition']['text'],
                "humidity": weather_data['current']['humidity'],
                "wind_kph": weather_data['current']['wind_kph']
            },
            "forecast": []
        }
        
        # Add forecast data
        for day in weather_data['forecast']['forecastday']:
            result['forecast'].append({
                "date": day['date'],
                "max_temp_c": day['day']['maxtemp_c'],
                "min_temp_c": day['day']['mintemp_c'],
                "condition": day['day']['condition']['text'],
                "chance_of_rain": f"{day['day']['daily_chance_of_rain']}%"
            })
        
        return {"result": result}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error fetching weather data: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
