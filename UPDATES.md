# Update Log

## 2026-01-07

- **Security Audit Response:** Implemented recommendations from the cybersecurity audit, including a new "Security & Data Privacy" section in the README and Quick Start guide (bilingual).
- **Dependency Management:** Tightened version constraints in `requirements.txt` and `environment.yml` to minimize supply chain risks (`~=` pinning).
- **Build Documentation:** Added `docs/BUILD.md` detailing the manual build process for reproducibility in both English and French.
- **Update Awareness:** Clarified that GitHub Releases is the official source for updates and documented the "unsigned" nature of current executables.
- **UI Update:** Added a prominent "Security & Privacy" warning link in the application header pointing to the new README safety guidelines.
- **New Feature:** Added CSV Export capability (`.csv`) including file type, size, and descriptions.
- **DevOps:** Implemented automated GitHub Actions workflow for cross-platform builds (Windows, macOS, Ubuntu).
- **Accessibility:** Added `F2`/`Enter` keyboard shortcuts for editing descriptions and improved screen reader labels for buttons.

## 2025-11-05

- **Bilingual interface & exports:** Added a `Localization` service, language selector, and persistent language preference so the UI and generated Markdown/Text files can be shown in English or French.
- **Content refresh:** Converted the README and Quick Start guide into bilingual documents and updated architecture notes to describe the localization workflow.
- **Dependency refresh:** Bumped PyQt5, humanize, markdown, and pyinstaller versions in `environment.yml` and `requirements.txt` to reflect the localization-ready release.
- **Documentation alignment:** Documented localization flows and session persistence in the architecture overview and update log.

## 2025-11-04

- **Hidden file parity**: Updated filtering logic to respect Windows hidden/system attributes across the UI and exports and added shared helpers for exclusion rules.
- **Export fidelity**: Refactored the markdown/plain-text generation pipeline so preview and exports mirror the filtered tree, ensuring hidden or excluded items stay omitted.
- **Windows regression coverage**: Added automated tests that exercise hidden/system attribute handling, extension exclusions, and filtered size calculations on Windows.
- **Resizable layout**: Introduced a vertical splitter that keeps the header fixed while allowing the tree and preview panes to expand vertically, improving usability for large directories.
- **Guided workflow**: Revised the header instructions to a numbered 1-2-3 flow, repositioned export buttons beneath the tree/preview area, and clarified usage links.
- **About/Info refresh**: Updated the dialog with Digital Research Alliance messaging, repository guidance (FRDR/Borealis), and cleaned contact details.
- **External link handling**: Enabled rich-text labels to open hyperlinks in the user’s default browser.
