# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt

import os
import urllib.request
from invoke import task, Collection, Context

# Define the license information
LICENSE_TYPE = "Apache-2.0"
COPYRIGHT_HOLDER = "CHARUDATTA KORDE LLC"
COPYRIGHT_YEAR = "2076"
LICENSE_URL = f"https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/{LICENSE_TYPE.lower()}.txt"
CODE_DIR = "."

# Define file types and comment symbols
file_types = {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*", ".sh": "#"}


@task
def fetch_license_text(ctx):
    try:
        with urllib.request.urlopen(LICENSE_URL) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
            else:
                print(
                    "Failed to fetch the license text. HTTP Status Code:",
                    response.status,
                )
                return None
    except urllib.error.URLError as e:
        print(f"Failed to fetch the license text. Error: {e}")
        return None


@task
def create_license_file(ctx, license_text, license_path="LICENSE"):
    """Create a LICENSE file with the specified license text.
    Args:
        license_text (str): The license text to write to the LICENSE file.
        license_path (str): The path to the LICENSE file. Default is "LICENSE".
    Returns:
        None
    Example:
        $ invoke create_license_file --license_text=... --license_path=LICENSE
    """
    with open(license_path, "w") as license_file:
        license_file.write(license_text)
    print("LICENSE file created.")


@task(pre=[fetch_license_text])
def add_license_header_to_file(ctx, file_path, header_text, comment_symbol):
    with open(file_path, "r+") as file:
        content = file.read()
        if header_text in content:
            print(f"License header already exists in {file_path}.")
            return
        file.seek(0, 0)
        file.write(
            f"{comment_symbol} {header_text} \n{comment_symbol}\n{comment_symbol} {LICENSE_URL}\n\n{content}"
        )

    print(f"Added license header to {file_path}")


@task(pre=[fetch_license_text])
def remove_license_header_from_file(ctx, file_path, header_text, comment_symbol):
    with open(file_path, "r+") as file:
        content = file.read()
        header = f"{comment_symbol} {header_text} \n{comment_symbol}\n{comment_symbol} {LICENSE_URL}\n\n"
        if header in content:
            content = content.replace(header, "")
            file.seek(0)
            file.truncate()
            file.write(content)
            print(f"Removed license header from {file_path}.")
        else:
            print(f"No license header found in {file_path}.")


@task(pre=[fetch_license_text])
def add_license_headers(ctx):
    """Add license headers to all specified file types in the directory.
    Args:
        ctx (Context): The context instance (passed automatically).
    Returns:
        None
    Example:
        $ invoke add_license_headers
    """
    # Fetch the license text
    result = fetch_license_text(ctx)
    if not result:
        return

    # Add the copyright notice to the license text
    header_text = (
        f"Copyright {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER} - {LICENSE_TYPE} License"
    )
    license_text = f"{result} \n\n{header_text}  \n"

    # Create the LICENSE file
    create_license_file(ctx, license_text)

    # Add the license header to all specified file types in the directory
    for root, _, files in os.walk(CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in file_types:
                comment_symbol = file_types[file_ext]
                file_path = os.path.join(root, file)
                add_license_header_to_file(ctx, file_path, header_text, comment_symbol)


@task(pre=[fetch_license_text])
def remove_license_headers(ctx):
    """Remove license headers from all specified file types in the directory.
    Args:
        ctx (Context): The context instance (passed automatically).
    Returns:
        None
    Example:
        $ invoke remove_license_headers
    """
    # Fetch the license text
    result = fetch_license_text(ctx)
    if not result:
        return

    # Define the license header text
    header_text = (
        f"Copyright {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER} - {LICENSE_TYPE} License"
    )

    # Remove the license header from all specified file types in the directory
    for root, _, files in os.walk(CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in file_types:
                comment_symbol = file_types[file_ext]
                file_path = os.path.join(root, file)
                remove_license_header_from_file(
                    ctx, file_path, header_text, comment_symbol
                )


ns = Collection(
    create_license_file,
    add_license_headers,
    remove_license_headers,
    default=add_license_headers,
)
ns.name = "license"
if __name__ == "__main__":
    default(Context())
