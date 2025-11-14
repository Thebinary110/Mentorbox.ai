import os

PROJECT_ROOT = "rag_video_chat"

STRUCTURE = {
    "app": {
        "__init__.py": "",
        "core": {
            "__init__.py": "",
            "config.py": "",
            "logger.py": "",
        },
        "models": {
            "__init__.py": "",
            "transcript_segment.py": "",
            "query_request.py": "",
            "response_schema.py": "",
        },
        "services": {
            "__init__.py": "",
            "asr_service.py": "",
            "vad_service.py": "",
            "embedding_service.py": "",
            "vectorstore_service.py": "",
            "rerank_service.py": "",
            "llm_service.py": "",
            "compression_service.py": "",
        },
        "pipelines": {
            "__init__.py": "",
            "rag_pipeline.py": "",
        },
        "orchestration": {
            "__init__.py": "",
            "graph_builder.py": "",
        },
        "api": {
            "__init__.py": "",
            "routes.py": "",
        },
        "utils": {
            "__init__.py": "",
            "chunker.py": "",
            "text_cleaner.py": "",
            "timer.py": "",
        },
    },
    "backend": {
        "__init__.py": "",
        "main.py": "",
    },
    "frontend": {
        "streamlit_app.py": ""
    },
    "data": {},
    "embeddings": {},
    "infra": {
        "docker-compose.yml": "",
        "Dockerfile": "",
    },
    "scripts": {
        "download_and_extract.py": "",
        "run_asr.py": "",
        "run_indexing.py": "",
        "test_pipeline.py": "",
    },
    "tests": {
        "__init__.py": "",
        "test_asr.py": "",
        "test_retrieval.py": "",
        "test_rag.py": "",
    },
    "README.md": "",
    "requirements.txt": "",
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    print(f"Creating project structure for: {PROJECT_ROOT}")
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    create_structure(PROJECT_ROOT, STRUCTURE)
    print("Project structure created successfully!")
