# TreeGen: file tree generator for scientific files

## Overview

**TreeGen** is a desktop application built with PyQt5. It allows users to generate, view, and export the file structure of a selected directory with features such as:

---

## Features

- **Interactive file tree:** Browse an expandable file tree with detailed size information.
- **Live markdown preview:** See a real-time Markdown representation of your file tree.
- **Editable descriptions:** Add or edit descriptions for any file or folder to document your dataset content.
- **Search & filter:** Quickly search for items and exclude specific file types and hidden files/folders.
- **Export options:** Save the file tree output as either Markdown (`.md`) or Plain Text (`.txt`).

This tool is especially useful for researchers, librarians and data managers who needs to document file structures in an organized manner.

---

## Use (executable)

**Windows users:** Download and run the .exe file located in the dist/ folder.
**Mac (M1) users:** Download the .app app file located in the dist/ folder.

## Use (script)

### Prerequisites

- Python 3.x
- [PyQt5](https://pypi.org/project/PyQt5/)
- [humanize](https://pypi.org/project/humanize/)

_Optional (for converting Markdown to HTML in the preview, if needed):_

- [Markdown](https://pypi.org/project/Markdown/)

Install the dependencies using pip:

```bash
pip install PyQt5 humanize
# Optional:
pip install markdown
```

Clone the Repository

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree
cd file-tree-generator
```

---

## Usage
Run the application in terminal with:

```bash
python TreeGen.py
```

Or run the script with code interpreters like [Visual Studio Code](https://code.visualstudio.com/).

## How to use

- **Select Directory:** Choose a folder whose tree you want to generate..

- **View File Tree:** The left pane displays the file tree while the right pane shows a live Markdown preview.

- **Edit Descriptions:** Browse the folder structure and double-click in the description column to add/edit its description.

- **Filter Files/Folders:** Use the search bar to find specific items and use the exclusion options to omit unwanted file types or hidden files.

- **Export the File Tree:** Export the tree as Markdown (.md) or plain text (.txt).

---

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit)

---
## Contact

For questions or further support, please contact rdm-gdr\@alliancecan.ca.

