# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt
####################################################
# make simplified version for private directories with notes, tasks, title, description
#####################################################

from invoke import task, Collection
from pathlib import Path


class ConfigGen:

    def __init__(self):
        self.data = {}

    def _getlist(self, input_prompt):
        lines = ""
        while True:
            line = input(f"{input_prompt}")
            if line:
                lines += f"- {line} \n"
            else:
                break
        return lines

    def _labelGen(self, input_prompt):
        list_labels = ""
        while True:
            line = input(f"{input_prompt}")
            if line:
                list_labels += f"`{line}` "
            else:
                break
        return list_labels

    def get_data(self):
        self.data["title"] = input("Enter title of project -> ")
        self.data["description"] = input("Enter project description -> ")
        self.data["features"] = self._getlist("Enter project features -> ")
        self.data["list_badges"] = self._labelGen(
            "Enter softwares used in the project -> "
        )


class ReadmeGen:

    def __init__(self):
        self.template_path = Path(__file__).parent / "template.md"
        self.file_name = "README.md"
        self.data = {}

    def add_template(self):
        with open(self.template_path, mode="r", encoding="utf-8") as template_file:
            self.template_content = template_file.read()

    def add_config(self):
        config = ConfigGen()
        config.get_data()
        self.data = config.data

    def gen_str(self):
        self.doc = self.template_content.format(
            title=self.data.get("title"),
            description=self.data.get("description"),
            features=self.data.get("features"),
            list_badges=self.data.get("list_badges"),
        )

    def gen_file(self):
        with open(self.file_name, "w+", encoding="utf-8") as f:
            f.write(self.doc)

    def main(self, ppt_gen=False):
        self.add_template()
        self.add_config()
        self.gen_str()
        self.gen_file()
        if ppt_gen:
            self.ppt_gen()

    def ppt_gen(self):
        file_content = f"""---
marp: true
headingDivider: 6
theme: gaia
---\n{self.doc}"""

        with open("readmex.md", "w+", encoding="utf-8") as f:
            f.write(file_content)


@task
def generate_readme(ctx, ppt_gen=False):
    readme = ReadmeGen()
    readme.main(ppt_gen=ppt_gen)


ns = Collection(generate_readme)
ns.name = "readme"

if __name__ == "__main__":
    default(context())
