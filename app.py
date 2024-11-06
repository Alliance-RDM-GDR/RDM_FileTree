import sys
import os
import json
import humanize  
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTreeView, QAbstractItemView, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Tree Explorer")
        self.resize(800, 600)
        self.current_directory = None
        self.descriptions = {}
        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Button to select directory
        self.select_dir_button = QPushButton("Select Directory")
        self.select_dir_button.clicked.connect(self.select_directory)
        layout.addWidget(self.select_dir_button)

        # Button to export to Markdown
        self.export_button = QPushButton("Export to Markdown")
        self.export_button.clicked.connect(self.export_to_markdown)
        self.export_button.setEnabled(False)  # Disable until a directory is selected
        layout.addWidget(self.export_button)

        # Tree view to display file structure
        self.tree_view = QTreeView()
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.doubleClicked.connect(self.add_description)
        layout.addWidget(self.tree_view)

        # Model to hold data for the tree view
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Size", "Description"])
        self.tree_view.setModel(self.model)
        self.tree_view.header().setDefaultSectionSize(200)
        self.tree_view.header().setSectionResizeMode(0, self.tree_view.header().Stretch)
        self.tree_view.header().setSectionResizeMode(1, self.tree_view.header().ResizeToContents)
        self.tree_view.header().setSectionResizeMode(2, self.tree_view.header().Stretch)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.current_directory = directory
            self.load_descriptions()
            self.populate_tree()
            self.export_button.setEnabled(True)  # Enable the export button

    def load_descriptions(self):
        desc_file = os.path.join(self.current_directory, ".descriptions.json")
        if os.path.exists(desc_file):
            with open(desc_file, 'r', encoding='utf-8') as f:
                self.descriptions = json.load(f)
        else:
            self.descriptions = {}

    def save_descriptions(self):
        desc_file = os.path.join(self.current_directory, ".descriptions.json")
        with open(desc_file, 'w', encoding='utf-8') as f:
            json.dump(self.descriptions, f, indent=4)

    def populate_tree(self):
        self.model.removeRows(0, self.model.rowCount())
        root_item = self.model.invisibleRootItem()
        self.add_items(root_item, self.current_directory)
        self.tree_view.expandAll()

    def add_items(self, parent_item, path):
        try:
            items = os.listdir(path)
            items.sort()
            for item_name in items:
                item_path = os.path.join(path, item_name)
                if os.path.isdir(item_path):
                    size = self.get_folder_size(item_path)
                    icon = QIcon.fromTheme("folder")
                else:
                    size = os.path.getsize(item_path)
                    icon = QIcon.fromTheme("text-x-generic")
                size_human_readable = humanize.naturalsize(size)
                description = self.descriptions.get(item_path, "")

                # Create items for each column
                item = QStandardItem(item_name)
                size_item = QStandardItem(size_human_readable)
                desc_item = QStandardItem(description)

                # Set data and icons
                item.setData(item_path, Qt.UserRole)
                item.setIcon(icon)
                size_item.setData(size, Qt.UserRole)
                desc_item.setData(description, Qt.UserRole)

                # Append row to parent
                parent_item.appendRow([item, size_item, desc_item])

                # Recursively add child items if directory
                if os.path.isdir(item_path):
                    self.add_items(item, item_path)
        except PermissionError:
            pass  # Skip directories that cannot be accessed

    def get_folder_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except (OSError, PermissionError):
                        pass  # Skip files that cannot be accessed
        return total_size

    def add_description(self, index):
        item = self.model.itemFromIndex(index.siblingAtColumn(0))
        desc_item = self.model.itemFromIndex(index.siblingAtColumn(2))

        item_path = item.data(Qt.UserRole)
        current_desc = desc_item.text()

        text, ok = QInputDialog.getMultiLineText(
            self, "Add Description", f"Enter description for:\n{item_path}", current_desc)
        if ok:
            desc_item.setText(text)
            self.descriptions[item_path] = text
            self.save_descriptions()

    def export_to_markdown(self):
        if not self.current_directory:
            QMessageBox.warning(self, "No Directory Selected", "Please select a directory first.")
            return

        # Prompt the user to select a location to save the Markdown file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            os.path.join(self.current_directory, "file_tree.md"),
            "Markdown Files (*.md);;All Files (*)",
            options=options
        )
        if file_path:
            # Initialize counters
            self.folder_count = 0
            self.file_count = 0
            self.total_size = 0

            # Generate the markdown content
            markdown_lines = []
            # Add the path of the root directory
            root_name = os.path.basename(self.current_directory) or self.current_directory
            markdown_lines.append(f"{root_name}")
            self.build_tree(self.current_directory, markdown_lines, prefix='', is_last=True)
            # Add summary at the end
            markdown_lines.append('')
            markdown_lines.append('---')
            markdown_lines.append('**Summary:**')
            markdown_lines.append(f'- Total folders: {self.folder_count}')
            markdown_lines.append(f'- Total files: {self.file_count}')
            total_size_hr = humanize.naturalsize(self.total_size)
            markdown_lines.append(f'- Total size: {total_size_hr}')

            markdown_content = '\n'.join(markdown_lines)
            # Write to file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                QMessageBox.information(self, "Export Successful", f"File tree exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred:\n{str(e)}")


    def build_tree(self, path, lines, prefix='', is_last=True):
        # Get list of items
        try:
            items = os.listdir(path)
            items.sort()
        except PermissionError:
            lines.append(prefix + '└── [Permission Denied]')
            return

        # Update folder count and total size
        self.folder_count += 1
        folder_size = 0

        # Prepare the prefixes
        pointers = ['├── '] * (len(items) - 1) + ['└── '] if items else []
        for index, item_name in enumerate(items):
            item_path = os.path.join(path, item_name)
            is_dir = os.path.isdir(item_path)
            size = self.get_folder_size(item_path) if is_dir else os.path.getsize(item_path)
            size_hr = humanize.naturalsize(size)

            if is_dir:
                # Folder names in bold
                line = f"{prefix}{pointers[index]}**{item_name}**"
            else:
                # File names not in bold
                line = f"{prefix}{pointers[index]}{item_name}"
                # Update file count and total size
                self.file_count += 1
                self.total_size += size
                folder_size += size

            line += f" [ {size_hr} ]"

            lines.append(line)

            # Add description as a comment
            description = self.descriptions.get(item_path, "")
            if description:
                comment_prefix = prefix + ('    ' if pointers[index] == '└── ' else '│   ')
                lines.append(f"{comment_prefix}<!-- {description} -->")

            if is_dir:
                if pointers[index] == '└── ':
                    extension = '    '
                else:
                    extension = '│   '
                self.build_tree(item_path, lines, prefix=prefix + extension, is_last=(pointers[index] == '└── '))
                # Update folder size after processing subdirectories
                self.total_size += size
                folder_size += size

        # If the directory is empty
        if not items:
            lines.append(prefix + '└── [Empty Folder]')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
