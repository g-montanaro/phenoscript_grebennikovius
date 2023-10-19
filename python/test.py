import os
import re



def find_phenoscript_extensions():
    vscode_extensions_dir = os.path.expanduser("~/.vscode/extensions")
    phenoscript_folders = []

    # List all folders in the ~/.vscode/extensions directory
    extension_folders = os.listdir(vscode_extensions_dir)

    # Filter folders that contain "tarasov-lab.phenoscript"
    for folder in extension_folders:
        if "tarasov-lab.phenoscript" in folder:
            phenoscript_folders.append(folder)

    # Sort folders by version number (assuming format '0.0.XX')
    phenoscript_folders.sort(reverse=True, key=lambda folder: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', folder)])

    # Create full paths to the folders
    phenoscript_paths = [os.path.join(vscode_extensions_dir, folder) for folder in phenoscript_folders]

    return phenoscript_paths

phenoscript_paths=find_phenoscript_extensions()
latest=phenoscript_paths[0]
others=phenoscript_paths[1:]