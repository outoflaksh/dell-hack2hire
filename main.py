import re
import json
from pprint import pprint
import os, pathlib
from collections import Counter


def find_url(strings: list):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = []

    for line, string in enumerate(strings):
        url = re.findall(regex, string)
        if url:
            line_url = [line + 1, [x[0] for x in url]]
            urls.append(line_url)

    return urls


def find_apikeys(strings: list):
    regex1 = [
        r"AIza[0-9A-Za-z-_]{35}",
        r"key-[0-9a-zA-Z]{32}",
        r"[h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
        r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
        r"https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
        r"[0-9a-f]{32}-us[0-9]{1,2}",
        r"EAACEdEose0cBA[0-9A-Za-z]+]",
        r"(?i)(facebook|fb)(.{0,20})?(?-i)['\\\"][0-9a-f]{32}['\\\"]",
        r"(?i)(facebook|fb)(.{0,20})?['\\\"][0-9]{13,17}['\\\"]",
        r"(?i)twitter(.{0,20})?['\\\"][0-9a-z]{35,44}['\\\"]",
        r"(?i)twitter(.{0,20})?['\\\"][0-9a-z]{18,25}['\\\"]",
        r"ghp_[0-9a-zA-Z]{36}",
        r"gho_[0-9a-zA-Z]{36}",
        r"(ghu|ghs)_[0-9a-zA-Z]{36}",
        r"ghr_[0-9a-zA-Z]{76}",
        r"(?i)linkedin(.{0,20})?(?-i)[0-9a-z]{12}",
        r"(?i)linkedin(.{0,20})?[0-9a-z]{16}",
        r"[a-zA-Z0-9_-]*:[a-zA-Z0-9_-]+@github\\.com*",
        r"rk_live_[0-9a-zA-Z]{24}",
        r"sk_live_[0-9a-zA-Z]{24}",
        r"sqOatp-[0-9A-Za-z\\-_]{22}",
        r"ya29\\.[0-9A-Za-z\\-_]+",
        r"[0-9(+-[0-9A-Za-z_]{32}.apps.googleusercontent.com",
        r"(A3T[A-Z0-9]|AKIA|AGPA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        r"(?i)aws(.{0,20})?(?-i)['\\\"][0-9a-zA-Z\/+]{40}['\\\"]",
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
    ]

    apikeys = []

    for line, string in enumerate(strings):
        for regex in regex1:
            apikey = re.findall(regex, string)
            if apikey:
                line_apikey = [line + 1, [x for x in apikey]]
                apikeys.append(line_apikey)

    return apikeys


def get_http_urls_from_file(file_name: str):
    with open(file_name, "r+") as f:
        code_base: str = f.read()

    return find_url(list(code_base.split("\n")))


def get_api_keys_from_file(file_name):
    with open(file_name, "r+") as f:
        code_base: str = f.read()

    return find_apikeys(list(code_base.split("\n")))


def get_external_libraries_from_file(config_file_name: str):
    with open(config_file_name, "rb+") as f:
        config_file = json.load(f)

    return config_file["dependencies"]


def get_endpoints_from_file(file_name: str):
    with open(file_name, "r+") as f:
        code_base: str = f.read()

    internal_endpoints = {}
    internal_endpoints["get"] = list(re.findall(r"app.get\(\"(.*?)\"", code_base))
    internal_endpoints["post"] = list(re.findall(r"app.post\(\"(.*?)\"", code_base))
    internal_endpoints["delete"] = list(re.findall(r"app.delete\(\"(.*?)\"", code_base))
    internal_endpoints["put"] = list(re.findall(r"app.put\(\"(.*?)\"", code_base))

    return internal_endpoints


# Temporary way for finding outdated packages
def get_outdated_packages(parent_dir):
    raw_result = os.popen(f"cd {parent_dir} && npm outdated").read().split()[7:]
    result = []

    for i in range(0, len(raw_result), 6):
        result.append(
            {
                "pkg_name": raw_result[i],
                "curr_version": raw_result[i + 1],
                "latest_version": raw_result[i + 3],
            }
        )

    return result


def get_database_info(config_file_name):
    dependencies = set(
        get_external_libraries_from_file(config_file_name=config_file_name).keys()
    )
    result = {"mongo": False, "sql": False}

    mongo_clients: set = {"mongoose", "mongodb"}
    if mongo_clients.intersection(dependencies):
        result["mongo"] = True

    sql_clients: set = {"sequelize", "typeorm", "prisma"}
    if sql_clients.intersection(dependencies):
        result["sql"] = True

    return result


def generate_doc_for_file(file_name):
    return {
        "http_urls": get_http_urls_from_file(file_name),
        "internal_endpoints": get_endpoints_from_file(file_name),
        # "api_keys": get_api_keys_from_file(file_name),
    }


def count_files_type(codebase_path):
    counts = Counter()
    for c_dir, dirs, files in os.walk(codebase_path):
        for file in files:
            before, ext = os.path.splitext(file)
            counts[ext] += 1
    return {"total_files": sum(counts.values()), "files_type": counts}


def generate_doc_for_codebase(codebase_path, config_file_name):
    config_file_path = f"{codebase_path}/{config_file_name}"

    blacklisted_folders = [
        "node_modules",
        "venv",
        ".git",
        ".vscode",
        "__pycache__",
        "vendor",
    ]
    blacklisted_files = [
        "package-lock.json",
        "requirements.txt",
        ".gitignore",
    ]

    file_list = []

    for dirPath, dirNames, fileNames in os.walk(codebase_path):
        if any(folder in dirPath for folder in blacklisted_folders):
            continue
        else:
            for fileName in fileNames:
                if any(file in fileName for file in blacklisted_files):
                    continue
                else:
                    file_list.append(os.path.join(dirPath, fileName))

    doc = {
        "files": {},
        "outdated_packages": get_outdated_packages(codebase_path),
        "database": get_database_info(config_file_path),
        "external_libraries": get_external_libraries_from_file(config_file_path),
        "files_present": count_files_type(codebase_path=codebase_path),
    }

    for file in file_list:
        doc["files"][file] = generate_doc_for_file(file)

    doc["total_files_scanned"] = len(file_list)

    with open("integration_doc.json", "w+") as f:
        f.write(json.dumps(doc, indent=4))

    return doc
