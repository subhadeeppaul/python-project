# API Documentation: https://www.mediawiki.org/wiki/API:Search

from argparse import ArgumentParser
import requests
import json
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/w/api.php"
session = requests.session()

def fetch_data(keyword, num_urls):
  print("Fetching data for keyword: {}".format(keyword))
  search_params = {
    "action": "query",  # Search
    "format": "json", # Response format
    "prop": "info",   # Get page info
    "generator": "search",  # Search for pages
    "inprop": "url",  # Get URL
    "gsrsearch": keyword, # Search term
    "gsrlimit": num_urls  # Number of results to return
  }
  
  paragraphs = []
  response = session.get(url=URL, params=search_params) # Get search results
  try:
    data = response.json()["query"]["pages"]
    for page_id in data:
      paragraph = get_paragraph(page_id)
      paragraphs.append({"url": data[page_id]["fullurl"], "paragraph": paragraph})
    return paragraphs
  except KeyError:
    print("No results found for keyword: {}".format(keyword))
    exit(1)

def get_paragraph(page_id):
  print("Fetching paragraph for page_id: {}".format(page_id))
  page_params = {
    "action": "parse",  # Parse page
    "format": "json",
    "pageid": page_id,  # Unique page ID
    "prop": "text",     # Get page text
    "utf8": "1"
  }
  response = session.get(URL, params=page_params)
  data = response.json()["parse"]["text"]["*"]

  soup = BeautifulSoup(data, "html.parser")   # Parse HTML
  for para in soup.find_all("p"):
    if para.text.strip():   # Skip empty paragraphs
      [sup.decompose() for sup in para.find_all("sup")]   # Remove all <sup> tags (references)
      return para.text.strip()    # Return first non-empty paragraph
  return ""

def store_data(data, output_file):
  # Store data in JSON format
  json.dump(data, open(output_file, 'w'))
  print("Data stored in file: {}".format(output_file))

if __name__ == '__main__':
  parser = ArgumentParser(description='Extract info from Wikipedia and save to json')
  parser.add_argument('--keyword', type=str, help='Keyword to search for')
  parser.add_argument('--num_urls', type=int, help='Number of urls to extract')
  parser.add_argument('--output', type=str, help='Output filename')

  args = parser.parse_args()

  if not args.keyword or not args.num_urls:
    print('Please provide a keyword, number of urls and output filename')
    exit(1)
  
  data = fetch_data(args.keyword, args.num_urls)
  store_data(data, args.output or 'output.json')
