# TreeGen software architecture 

## Overview

TreeGen is a cross-platform desktop application developed in Python using PyQt5. It is designed to help users interactively explore a directory structure, annotate files and folders with descriptions, and export the annotated tree in Markdown or plain-text format. The application combines filesystem traversal, metadata aggregation, GUI rendering, and export logic into a modular architecture inspired by Model-View-Controller (MVC) principles.

---

## High-Level Architecture

The application consists of the following core components:

### 1. **Model (Data Management Layer)**

This layer is responsible for interacting with the local filesystem, collecting metadata (paths, file/folder sizes, descriptions), and handling annotation persistence. It includes:
- Use of Python's `os` module to traverse directories and access file properties.
- The `humanize` library to convert file sizes into human-readable strings.
- A local `.descriptions.json` file stored at the root of the selected directory to save and reload user-added descriptions.

### 2. **View (Graphical User Interface)**

TreeGen uses PyQt5 widgets to build a modern split-pane user interface:
- `QTreeView` displays the interactive file/folder hierarchy on the left.
- `QTextBrowser` or `QTextEdit` shows a live Markdown preview on the right.
- `QSplitter` manages layout flexibility between the two panes.
- UI elements such as search bars, buttons, and checkboxes allow users to interact with the application dynamically.

### 3. **Controller (Interaction and Logic Layer)**

The logic layer ties the model and view together. It:
- Reacts to user actions (directory selection, description editing, search/filter changes).
- Updates the file tree model and preview pane accordingly.
- Handles export actions and writes Markdown or text files to disk.
- Manages input validation, filtering (e.g., hidden files, excluded extensions), and sorting.

---

## Filtering and Search

A custom `FileFilterProxyModel` subclass (built on PyQt5's `QSortFilterProxyModel`) adds advanced functionality for:
- Real-time search using wildcard patterns.
- Filtering out hidden files and folders.
- Excluding specific file types based on user-defined extensions.

This model separates the filtering logic from the data model and view, promoting maintainability.

---

## Export Engine

The Markdown and plain-text export feature is powered by a recursive tree traversal function that:
- Adds indentation and tree symbols (`├──`, `└──`, `│`) to emulate UNIX-style tree views.
- Includes file sizes and optional user-provided descriptions.
- Outputs the tree structure in two formats:
  - Markdown with bolded folder names and HTML comment-style annotations.
  - Plain text for simple embedding in reports or email.

---

## Design Principles

TreeGen is guided by the following design values:

- **Modularity:** Each responsibility (UI, filtering, metadata gathering, exporting) is encapsulated in its own component.
- **Reusability:** Filtering and export logic are written as standalone functions or classes, easy to test and extend.
- **Clarity and Maintainability:** Clean code organization, rich comments, and consistent styling help future contributors understand the system quickly.
- **Responsiveness:** The GUI updates in real time and remains performant even when loading large directory trees.
- **Cross-platform compatibility:** All components are tested on Windows, macOS, and Linux with a consistent experience.

---

## Planned Enhancements

- Asynchronous file system scanning for improved performance on large datasets.
- Multilingual support

---

-_Last updated: [2025-07-25]_
