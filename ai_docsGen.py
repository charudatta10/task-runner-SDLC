import json
from pathlib import Path
from .src.config import Config
from .src.utility import load_json_file, download_file
from invoke import task, Collection
import urllib.request

class DocumentationGenerator:
    def __init__(self, repo_path: str, template_file: str, output_dir: str = "docs"):
        self.repo_path = Path(repo_path).expanduser().absolute()
        self.output_dir = Path(output_dir).absolute()
        self.output_dir.mkdir(exist_ok=True)
        self.template_file = Path(template_file)
        download_file(
            f"{Config.REPO_DOCS}/{self.template_file}",
            "prompt_docgen.json"
        )
        self.doc_templates = load_json_file(self.template_file)


    def generate_with_ollama(
        self, prompt: str, context: str = "", model: str = "granite3.2:8b"
    ) -> str:
        full_prompt = f"Generate detailed documentation:\n{prompt}\nContext:\n{context}"
        api_url = "http://localhost:11434/api/generate"
        request_data = json.dumps(
            {"model": model, "prompt": full_prompt, "stream": False}
        ).encode("utf-8")
        req = urllib.request.Request(
            api_url, data=request_data, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.load(response)
        return result.get("response", "")

    def generate_all_docs(self):
        for filename, prompt in self.doc_templates.items():
            print(f"[DEBUG] Generating documentation for: {filename} with prompt: {prompt}")
            content = self.generate_with_ollama(prompt)
            output_path = self.output_dir / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved: {output_path}")


@task
def ai_doc_gen(
    ctx, repo_path=".", template_file="prompt_docgen.json", output_dir="docs"
):
    """Invoke Task to Generate Documentation"""
    generator = DocumentationGenerator(
        repo_path=repo_path, template_file=template_file, output_dir=output_dir
    )
    generator.generate_all_docs()


ns = Collection(ai_doc_gen)
