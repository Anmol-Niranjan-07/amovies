from flask import Flask, render_template, request, redirect, url_for
import requests
from lxml import html
import logging

app = Flask(__name__)

IMDB_SEARCH_URL = "https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

logging.basicConfig(level=logging.DEBUG)

def get_imdb_results(query):
    logging.debug(f"Searching for IMDb results for query: {query}")
    response = requests.get(IMDB_SEARCH_URL.format(query=query), headers=HEADERS)
    tree = html.fromstring(response.content)
    results = tree.xpath('//*[@id="__next"]/main/div[2]/div[4]/section/div/div[1]/section[2]/div[2]/ul/li')
    
    logging.debug(f"Number of results found: {len(results)}")
    movies = []
    for result in results:
        title_element = result.xpath('.//div[2]/div/a')
        
        if title_element:
            title = title_element[0].text_content().strip()
            imdb_url = title_element[0].get('href')
            imdb_id = imdb_url.split('/')[2]
            movies.append({'title': title, 'imdb_id': imdb_id})
    
    return movies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    movies = get_imdb_results(query)
    if movies:
        return render_template('search.html', movies=movies)
    return render_template('search.html', error="No movies found. Please try again.")

@app.route('/watch/<imdb_id>')
def watch(imdb_id):
    return render_template('watch.html', imdb_id=imdb_id)

if __name__ == '__main__':
    app.run(debug=True)
