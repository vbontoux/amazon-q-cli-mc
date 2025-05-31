# Weather MCP Server

A simple MCP server that provides weather forecast information using the WeatherAPI.com service.

## Setup

1. Sign up for a free API key at [WeatherAPI.com](https://www.weatherapi.com/)
2. Copy `.env.example` to `.env` and add your API key:
   ```
   cp .env.example .env
   ```
3. Edit `.env` and add your WeatherAPI.com API key
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Start the server:
   ```
   python server.py
   ```

The server will run on http://localhost:8000

## Using with Amazon Q CLI

To use this MCP server with Amazon Q CLI, add it to your configuration:

```bash
q config add-mcp-server weather http://localhost:8000
```

Then you can use it in your conversations with Amazon Q:

```bash
q chat
```

Example query: "What's the weather forecast for Seattle?"
