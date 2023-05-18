import json

import quart
import quart_cors
from quart import jsonify
# from quart import request
import requests
import json

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

def get_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return {"error": "Could not retrieve game details"}


@app.route('/game/<int:id>', methods=['GET'])
async def get_game(id):
    game_data = get_game_details(id)

    if 'error' not in game_data:
        app_details = game_data[str(id)]['data']

        mapped_data = {}
        keys_to_map = ['steam_appid', 'name', 'developers', 'publishers',
                       'categories', 'pc_requirements', 'mac_requirements',
                       'linux_requirements', 'website', 'required_age',
                       'release_date', 'platforms', 'price_overview',
                       'demos', 'genres', 'recommendations', 'achievements', 'dlc']

        for key in keys_to_map:
            if key in app_details:
                mapped_data[key] = app_details[key]

        if 'achievements' in app_details:
            mapped_achievements = {
                'total': app_details['achievements']['total'],
                'highlighted': [
                    {'name': ach['name']} for ach in app_details['achievements']['highlighted']
                ]
            }
            mapped_data['achievements'] = mapped_achievements

        return jsonify(mapped_data)
    else:
        return jsonify(game_data)


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
