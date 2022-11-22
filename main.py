import re
import json
from pprint import pprint
import os, pathlib
from collections import Counter
from dotenv import load_dotenv

load_dotenv()


def find_url(strings: list):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = []

    for line, string in enumerate(strings):
        url = re.findall(regex, string)
        if url:
            line_url = [line + 1, [x[0] for x in url]]
            urls.append(line_url)

    return urls


def get_http_urls_from_file(file_name: str):
    with open(file_name, "r+") as f:
        code_base: str = f.read()

    return find_url(list(code_base.split("\n")))


def get_api_keys_from_files(file_list):
    to_scan = []
    for file_name in file_list:
        with open(file_name, "r+") as f:
            code_base: str = f.read()
        to_scan.append({"filename": file_name, "document": code_base})

    GG_API_KEY = os.getenv("GITGUARDIAN_API_KEY")
    from pygitguardian import GGClient

    client = GGClient(api_key=GG_API_KEY)
    scan_result = client.multi_content_scan(to_scan)

    return scan_result.to_dict()


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

def get_protocols_from_file(file_name: str):
    with open(file_name, "r+") as f:
        code_base: str = f.read()

    protocols = {}
    protocols["http"] = list(re.findall(r"http://(.*?)\"", code_base))
    protocols["https"] = list(re.findall(r"https://(.*?)\"", code_base))
    protocols["ftp"] = list(re.findall(r"ftp://(.*?)\"", code_base))
    protocols["sftp"] = list(re.findall(r"sftp://(.*?)\"", code_base))
    protocols["ssh"] = list(re.findall(r"ssh://(.*?)\"", code_base))
    protocols["smtp"] = list(re.findall(r"smtp://(.*?)\"", code_base))
    protocols["pop3"] = list(re.findall(r"pop3://(.*?)\"", code_base))
    protocols["imap"] = list(re.findall(r"imap://(.*?)\"", code_base))
    

    return protocols

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
        "protocols": get_protocols_from_file(file_name),
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
        "secret_scan": get_api_keys_from_files(file_list),
    }

    for file in file_list:
        doc["files"][file] = generate_doc_for_file(file)

    doc["total_files_scanned"] = len(file_list)

    with open("integration_doc.json", "w+") as f:
        f.write(json.dumps(doc, indent=4))

    return doc
