import json
import urllib.request
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from config import Config
    from __init__ import load_json_file, download_file
except ImportError:
    Config = type('Config', (), {})()
    def load_json_file(*args, **kwargs):
        return {}
    def download_file(*args, **kwargs):
        pass


class DocumentationGenerator:
    def __init__(self, repo_path: str, template_file: str, output_dir: str = "docs"):
        self.repo_path = Path(repo_path).expanduser().absolute()
        self.output_dir = Path(output_dir).absolute()
        self.output_dir.mkdir(exist_ok=True)
        self.template_file = Path(template_file)
        download_file(f"{Config.REPO_DOCS}/{self.template_file}", "prompt_docgen.json")
        self.doc_templates = load_json_file(self.template_file)

    def generate_with_local_llm(
        self, prompt: str, context: str = "", model: str = "granite3.2:8b"
    ) -> str:
        full_prompt = f"Generate detailed documentation:\n{prompt}\nContext:\n{context}"
        api_url = "http://localhost:1337/v1/chat/completions"
        request_data = json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": full_prompt}],
                "stream": False,
        }).encode('utf-8')
        
        try:
            req = urllib.request.Request(api_url, data=request_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling local LLM: {e}")
            return ""

    def generate_all_docs(self):
        for filename, prompt in self.doc_templates.items():
            print(
                f"[DEBUG] Generating documentation for: {filename} with prompt: {prompt}"
            )
            content = self.generate_with_local_llm(prompt)
            output_path = self.output_dir / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved: {output_path}")



def ai_doc_gen(
    repo_path=".", template_file="prompt_docgen.json", output_dir="docs"
):
    """Invoke Task to Generate Documentation"""
    generator = DocumentationGenerator(
        repo_path=repo_path, template_file=template_file, output_dir=output_dir
    )
    generator.generate_all_docs()



