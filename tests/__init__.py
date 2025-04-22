from invoke import Collection
from . import git, quality, setup, docs, license

# Root namespace
ns = Collection()

# Add sub-collections
ns.add_collection(git.ns, name="git")
ns.add_collection(quality.ns, name="quality")
ns.add_collection(setup.ns, name="setup")
ns.add_collection(docs.ns, name="docs")
ns.add_collection(license.ns, name="license")