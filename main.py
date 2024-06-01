from flask import Flask, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

OPENSENSEMAP_API_URL = "https://api.opensensemap.org"

def get_version():
    return "0.0.2"

async def fetch_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def get_temperature_data():
    async with aiohttp.ClientSession() as session:
        url = f"{OPENSENSEMAP_API_URL}/boxes?bbox=-10,-10,10,10&grouptags=temperature&format=json&full=true"
        data = await fetch_data(session, url)
        return data

@app.route('/version', methods=['GET'])
def version():
    version = get_version()
    if version:
        return jsonify({"version": version})
    else:
        return jsonify({"error": "Unable to fetch version"}), 500

@app.route('/temperature', methods=['GET'])
async def temperature():
    data = await get_temperature_data()
    if data is not None:
        return jsonify(data)
    else:
        return jsonify({"error": "Unable to fetch temperature data"}), 500

if __name__ == '__main__':
    app.run(debug=True)