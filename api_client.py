import requests

url = 'http://127.0.0.1:5000/movies/api/v1.0/get_movie'

r = requests.post(url, json={"show_me_what_you_got": "Avatar"})
print(r.text)