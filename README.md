# TreeGen: File Tree Generator for Research Data

**TreeGen** is a cross-platform desktop application developed by the Digital Research Alliance of Canada. It helps researchers, data curators, and technical teams document and share the structure of digital folders in a clear, consistent, and citable format. With TreeGen, users can visualize and annotate the file hierarchy of any directory and export it as structured Markdown or plain text.

---

## Overview

TreeGen simplifies the process of generating file tree documentation by:

* Automatically reading folder and file names and sizes
* Allowing inline editing of descriptions
* Generating a live preview
* Supporting clean export to `.md` and `.txt`

This tool is especially useful for research data management, dataset publication, software documentation, and reproducible workflows.

---

## Features

* **Interactive File Tree:** Browse and annotate an expandable folder structure.
* **Live Markdown Preview:** Real-time rendering of the exported structure.
* **Search & Filter:** Find specific files, exclude hidden files, or ignore selected extensions.
* **Export Options:** Save your file tree as Markdown or plain text with an optional summary.
* **Usage Instructions:** Clear in-app guidance with clickable help links.
* **Local and Secure:** No internet access required; all operations are local.

---

## Installation

### Option A: Download the Executable

Download pre-built executables for your system from the [Releases](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases) page.

### Option B: Run from Source

#### Requirements

* Python 3.10+
* See `environment.yml` or `requirements.txt` for dependencies.

#### Setup Instructions

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
conda env create -f environment.yml
conda activate treegen-env
python TreeGen.py
```

---

## Usage Guide

* Launch TreeGen and click **Select Directory**.
* Navigate through the tree and double-click any file or folder to add a description.
* Use the search bar or exclusion options to filter what is shown.
* Click **Export to Markdown** or **Export to Plain Text** to save your documentation.

For step-by-step guidance, refer to the [Quick Start Tutorial](docs/TreeGen%20Tutorial.md).

---

## Documentation

* [Architecture Overview](docs/architecture.md)
* [Quick Start Tutorial](docs/QuickStart.md)
* [Software Management Plan](docs/SoftwareManagementPlan.pdf)
* [Contributing Guidelines](docs/contributing.md)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Citation

If you use TreeGen in your work, please cite it using the information provided in the [`CITATION.cff`](CITATION.cff) file.

TreeGen is also archived and citable via Zenodo: \[DOI placeholder]

---

## Contact

For support or questions, please contact: [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca)

Digital Research Alliance of Canada

---

*Last updated: 2025-07-28*
