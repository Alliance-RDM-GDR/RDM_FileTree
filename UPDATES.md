# Update Log

## 2025-11-04

- **Hidden file parity**: Updated filtering logic to respect Windows hidden/system attributes across the UI and exports and added shared helpers for exclusion rules.
- **Export fidelity**: Refactored the markdown/plain-text generation pipeline so preview and exports mirror the filtered tree, ensuring hidden or excluded items stay omitted.
- **Windows regression coverage**: Added automated tests that exercise hidden/system attribute handling, extension exclusions, and filtered size calculations on Windows.
- **Resizable layout**: Introduced a vertical splitter that keeps the header fixed while allowing the tree and preview panes to expand vertically, improving usability for large directories.
- **Guided workflow**: Revised the header instructions to a numbered 1-2-3 flow, repositioned export buttons beneath the tree/preview area, and clarified usage links.
- **About/Info refresh**: Updated the dialog with Digital Research Alliance messaging, repository guidance (FRDR/Borealis), and cleaned contact details.
- **External link handling**: Enabled rich-text labels to open hyperlinks in the user’s default browser.
