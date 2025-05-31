---
marp: true
theme: gaia
paginate: true
backgroundColor: #fff
---

## Amazon Q CLI with MCP Demo
### Demo project to showcase Amazon Q CLI with Model Context Protocol (MCP) integration.

* Explores various configurations of mcp servers
* Includes a [simple weather forecast HTTP MCP server](./weather-mcp-hhtp-server/README.md)

---

## What is MCP ?

---

## Initial Amazon Q CLI prompt
```
> I would like to install an mcp server localy in this project that gets weather forcast. 
It can be a docker MCP server or just a local definition of a public MCP servier but make 
sure this is the most simple approach with the least dependencies 
```
```
$ I'll help you set up a simple MCP server for weather forecasts with minimal dependencies. 
Let's create a basic implementation using a public weather API.
```
---

## MCP Server Creation
### Prompt
```
$ Let's create a simple MCP server using Python and FastAPI, which is 
one of the easiest approaches with minimal dependencies. 
This server will connect to a public weather API.
```

---

## MCP Server Creation
### Result
```
$ I've set up a simple weather MCP server

1. Weather MCP Server Structure:
weather-mcp-server/
├── server.py           # Main MCP server implementation (FastAPI)
├── requirements.txt    # Python dependencies
├── README.md           # Setup and usage instructions
└── .env.example        # Template for API key configuration
```

---

## MCP Server Creation
### Run it
1. Get a free API key from WeatherAPI.com
2. Set up the environment variables
`code .env.example`
3. Install the dependencies `pip install -r requirements.txt`
4. Run the server `python server.py`
5. Configure Amazon Q CLI to use this MCP server `export AMAZON_Q_MCP_SERVERS=weather=http://localhost:8000`

---

## MCP Server Creation
##### Testing tools request
```
curl -s -X POST http://localhost:8000/mcp/v1/tools
```
```json
{"tools":[{"name":"get_weather","description":"Get the current weather and forecast for a location",
"parameters":{"type":"object","properties":{"location":{"type":"string",
"description":"The city name or location to get weather for"},"days":{"type":"integer",
"description":"Number of days for the forecast (1-3)","default":1}},"required":["location"]}}]}
```
👍 **Server works**

---

## MCP Server Creation
##### Testing execute request
```
curl -s -X POST http://localhost:8000/mcp/v1/execute -H "Content-Type: application/json" -d '
{"name":"get_weather","parameters":{"location":"Paris"}}'
```
```json
{"result":{"location":"Paris, France","current":{"temperature_c":15.3,"temperature_f":59.5,
"condition":"Sunny","humidity":94,"wind_kph":4.7},"forecast":[{"date":"2025-05-30","max_temp_c":28.7,
"min_temp_c":14.3,"condition":"Sunny","chance_of_rain":"0%"}]}}
```

👍 **Server works**

---

## MCP Server Config - Issue 1
##### Bad suggestion to configure the MCP server
`q config add-mcp-server weather http://localhost:8000` + `q config list-mcp-servers`
`export AMAZON_Q_MCP_SERVERS=weather=http://localhost:8000`

👎 **Not working at all `q config` is not a valid command**

---

## MCP Server Config - Issue 2
##### Tested ChatGPT config : MCP HTTP server
```json
{
  "mcpServers": [
    {
      "name": "weather",
      "url": "http://localhost:8000",
      "enabled": true
    }
  ]
}
```
👎 **This is [not supported yet by Amazon Q CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-configuration.html)**

---

## MCP Server Config - Issue 3
##### Proposed a config based on ChatGPT
```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": [ "mcp-remote", "--url", "http://localhost:8000", 
                "--transport", "http", "--allow-http"],
      "timeout": 60000
    }
  }
}
```
👎 **Does not work eather...**

---

## MCP Server Config - Finally ...
##### Tested another one
```json
{
  "mcpServers": {
    "weather": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/adhikasp/mcp-weather.git", "mcp-weather"],
            "env": {
                "ACCUWEATHER_API_KEY": "GzxXDAK6qsjEZBi34NB1O5MeTtA1q8DV"
            }
        }
  }
}
```
👌 **THIS WORKS !!**

---

### References
- [MCP Servers](https://github.com/modelcontextprotocol/servers)
- [AWS MCP servers](https://github.com/awslabs/mcp)
