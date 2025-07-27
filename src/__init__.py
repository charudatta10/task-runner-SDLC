# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# © 2025 Charudatta Korde. Some Rights Reserved. Attribution aRequired. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import Collection
from . import git, quality, setup, docs, licenser, manager, tools

# Root namespace
ns = Collection()

# Add sub-collections
ns.add_collection(git.ns, name="git")
ns.add_collection(quality.ns, name="quality")
ns.add_collection(setup.ns, name="setup")
ns.add_collection(docs.ns, name="docs")
ns.add_collection(licenser.ns, name="licenser")
ns.add_collection(manager.ns, name="manager")
ns.add_collection(tools.ns, name="tools")

