Wikipedia Extractor
---
A simple program which grabs a data about any keyword, and dumps it into desire json file.

## Requirements
Install `bs4` and `requests` package with `pip`
```shell
pip install bs4 requests
```

## Usage

```bash
python3 wiki_extractor.py --keyword="My Keyword" --num_urls=10 --output=out.json
```
