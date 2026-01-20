# TreeGen Software Architecture

## Overview

TreeGen is a cross-platform desktop application built with Python and PyQt5. It allows users to explore a directory structure, annotate files and folders, and export the annotated hierarchy as Markdown or plain text. The codebase follows a pragmatic Model-View-Controller style that separates data access, presentation, and orchestration logic. The 2025 bilingual release added a dedicated localization layer and persisted language preferences, enhancing usability without changing the overall architecture.

---

## High-Level Components

### 1. Model - Filesystem & Metadata

The model layer gathers and persists the data needed to render the tree and exports.

- Uses Python's `os` and `pathlib` modules to iterate through directories safely.
- Applies `humanize.naturalsize` to present byte sizes in readable units.
- Stores user annotations in a `.descriptions.json` file at the root of the selected directory.
- Reuses helper functions (`iter_visible_children`, `calculate_folder_size`, etc.) for both the UI model and the export pipeline.

### 2. View - PyQt5 Widgets

TreeGen's user interface is composed of standard Qt widgets arranged with splitters and layouts.

- `QTreeView` paired with a `QStandardItemModel` renders the file hierarchy.
- `QTextEdit` displays a live Markdown preview of the generated export.
- Toolbars, filters, and status widgets (buttons, line edits, combo boxes, checkboxes) provide interaction points.
- `QSplitter` keeps the tree and preview panes resizable while the header remains fixed.

### 3. Controller - Application Logic

The `MainWindow` class coordinates user interactions.

- Responds to directory selection, double-click editing, export requests, and filter changes.
- Syncs the tree model, preview panel, and persistence layer.
- Handles error scenarios (missing directories, permission errors, failed exports) via Qt dialogs.
- Regenerates derived data (counts, totals) whenever filters or descriptions change.

### 4. Localization - Language Services

The bilingual release introduces `localization.py`, a lightweight service that centralizes all user-facing strings.

- `Localization` stores translations in a dictionary keyed by language code and exposes a `tr` helper for runtime lookup.
- `MainWindow` maintains a `Localization` instance, sets the active language on startup using `QSettings`, and rerenders the UI through `retranslate_ui()`.
- A `QComboBox` in the toolbar lets users switch between English and French; selections persist across sessions.
- Generated output (Markdown summaries, status messages, export dialogs) uses the same translation keys to ensure consistency across the UI and exported files.

---

## Data Flow

1. **Directory Selection**  
   The user picks a root folder. The controller loads `.descriptions.json` if present and calls `populate_tree()`.

2. **Model Population**  
   `populate_tree()` builds `QStandardItem` rows recursively. Each row stores the absolute path in `Qt.UserRole` for later reference.

3. **Filtering & Search**  
   The `FileFilterProxyModel` wraps the tree model, applying hidden-file and extension filters plus wildcard text search. The proxy feeds both the on-screen tree and the export routines.

4. **Preview Generation**  
   `generate_markdown_content()` walks the filtered filesystem, building Markdown lines, counting folders/files, and appending a localized summary.

5. **Localization Updates**  
   Whenever the language changes, `retranslate_ui()` updates widget text, placeholder hints, and export strings, then regenerates the preview so that summaries use the new language.

6. **Export**  
   The user chooses Markdown or plain text. The controller writes the generated content to disk and displays localized success or error dialogs.

---

## Key Supporting Modules

- **Filtering:** `FileFilterProxyModel` subclasses `QSortFilterProxyModel` to provide recursive filtering while respecting user preferences for hidden files and excluded extensions.
- **Persistence:** `QSettings` stores the preferred language; `.descriptions.json` stores per-path annotations; exported files are written with UTF-8 encoding.
- **Localization:** `localization.py` contains translation dictionaries, language display names, and helper methods to avoid scattering hard-coded strings.

---

## Design Guidelines

- **Maintainability:** Shared helpers (e.g., for tree traversal and size calculation) minimize duplication between preview and export code paths.
- **Responsiveness:** Filtering leverages Qt's proxy model to keep UI updates efficient even for large directory trees.
- **Accessibility:** Bilingual UI text, localized exports, and persistent preferences ensure users can work in their preferred language every session.
- **Extensibility:** The localization service is dictionary-driven, making it straightforward to add new languages or integrate with external translation workflows in the future.

---

## Planned Enhancements

- Async directory scanning to keep the UI responsive with very large datasets.
- Optional import/export of translation catalogs (e.g., `.ts`/`.qm`) for professional localization teams.
- Extended test coverage for language switching and export edge cases.

---

_Last updated: 2025-11-05_
