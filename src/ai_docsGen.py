import json
from pathlib import Path
import ollama
from .config import Config
from .utility import load_json_file, download_file
from invoke import task, Collection

class DocumentationGenerator:
    def __init__(self, repo_path: str, template_file: str, output_dir: str = "docs"):
        """Initialize the documentation generator."""
        self.repo_path = Path(repo_path).expanduser().absolute()
        self.output_dir = Path(output_dir).absolute()
        self.output_dir.mkdir(exist_ok=True)
        self.template_file = Path(template_file)
        self.doc_templates = load_json_file(self.template_file)


    def generate_with_ollama(self, prompt: str, context: str = "", model: str = "llama3:8b") -> str:
        """Generate documentation using Ollama with a specified model."""
        full_prompt = f"Generate detailed documentation:\n{prompt}\nContext:\n{context}"
        result = ollama.generate(model=model, prompt=full_prompt, stream=False)
        return result.get("response", "")

    def generate_all_docs(self):
        """Generate all documentation files using extracted templates."""
        for filename, prompt in self.doc_templates.items():
            content = self.generate_with_ollama(prompt)
            output_path = self.output_dir / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved: {output_path}")


@task
def ai_doc_gen(ctx, repo_path, template_file="templates.json", output_dir="docs"):
    """Invoke Task to Generate Documentation"""
    download_file(Config.REPO_DOCS + "/prompt_docgen.json", ".")
    generator = DocumentationGenerator(repo_path = ".", template_file="prompt_docgen.json", output_dir=".")
    generator.generate_all_docs()

ns = Collection(ai_doc_gen)



    