import re
import json
from pprint import pprint


def find_url(strings: list):
	regex = r"(?i)\b((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	urls = []
	
	for line, string in enumerate(strings):
		url = re.findall(regex,string)
		if url:
			line_url = [line+1, [x[0] for x in url]]
			urls.append(line_url)

	return urls


def get_http_urls_from_file(file_name: str): 
	with open(file_name, "r+") as f:
		code_base: str = f.read()

	return find_url(list(code_base.split('\n')))


def get_external_libraries_from_file(config_file_name: str):
	with open(config_file_name, "rb+") as f:
		config_file = json.load(f)

	return config_file["dependencies"]


def get_endpoints_from_file(file_name: str):
	with open(file_name, "r+") as f:
		code_base: str = f.read()

	return list(re.findall(r".get\(\"(.*?)\"", code_base))


js_file = "./index.js"
config_file = "./package.json"


result = {"http_urls": get_http_urls_from_file(js_file), 
	"external_libraries": get_external_libraries_from_file(config_file), 
	"internal_endpoints": get_endpoints_from_file(js_file)}

pprint(result)
