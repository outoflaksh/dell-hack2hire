from fastapi import FastAPI, Form
from main import generate_doc_for_codebase

app = FastAPI()


@app.get("/")
def read_index():
    return "<h1> Home page </h1>"


@app.post("/generate-document")
def generate_document(codebase_path: str = Form(), config_file_name: str = Form()):

    return generate_doc_for_codebase(
        codebase_path=codebase_path, config_file_name=config_file_name
    )
