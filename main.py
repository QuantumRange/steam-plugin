import json

import quart
import quart_cors
from quart import jsonify
# from quart import request
import requests
import json

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
# _TODOS = {}
#
# @app.post("/todos/<string:username>")
# async def add_todo(username):
#     request = await quart.request.get_json(force=True)
#     if username not in _TODOS:
#         _TODOS[username] = []
#     _TODOS[username].append(request["todo"])
#     return quart.Response(response='OK', status=200)
#
# @app.get("/todos/<string:username>")
# async def get_todos(username):
#     return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)
#
# @app.delete("/todos/<string:username>")
# async def delete_todo(username):
#     request = await quart.request.get_json(force=True)
#     todo_idx = request["todo_idx"]
#     # fail silently, it's a simple plugin
#     if 0 <= todo_idx < len(_TODOS[username]):
#         _TODOS[username].pop(todo_idx)
#     return quart.Response(response='OK', status=200)
#
# @app.get("/logo.png")
# async def plugin_logo():
#     filename = 'logo.png'
#     return await quart.send_file(filename, mimetype='image/png')
#
# @app.get("/.well-known/ai-plugin.json")
# async def plugin_manifest():
#     host = request.headers['Host']
#     with open("./.well-known/ai-plugin.json") as f:
#         text = f.read()
#         return quart.Response(text, mimetype="text/json")
#
# @app.get("/openapi.yaml")
# async def openapi_spec():
#     host = request.headers['Host']
#     with open("openapi.yaml") as f:
#         text = f.read()
#         return quart.Response(text, mimetype="text/yaml")


def get_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return {"error": "Could not retrieve game details"}

@app.get("/game/<int:id>")
async def get_game(id):
    game_data = get_game_details(id)

    print(game_data)

    if 'error' not in game_data:
        app_details = game_data[str(id)]['data']
        mapped_data = {
            "steam_appid": app_details['steam_appid'],
            "name": app_details['name'],
            "categories": app_details['categories'],
            "developers": app_details['developers'],
            "publishers": app_details['publishers'],
            "platforms": app_details['platforms'],
            "price_overview": app_details['price_overview'],
            "demos": app_details['demos'],
            "genres": app_details['genres'],
            "recommendations": app_details['recommendations'],
            "achievements": app_details['achievements'],
        }
        return jsonify(mapped_data)
    else:
        return jsonify(game_data)

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)
# https://store.steampowered.com/api/appdetails?appids=57690
if __name__ == "__main__":
    main()
