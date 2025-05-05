import sys
import os
import json
import humanize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QTreeView, QAbstractItemView, QInputDialog, QMessageBox,
    QTextEdit, QSplitter, QLabel, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp

LOGO_PATH = "Alliance_Logo.jpeg"

class FileFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FileFilterProxyModel, self).__init__(parent)
        self.exclude_extensions = []
        self.exclude_hidden = False
        self.setRecursiveFilteringEnabled(True)
    
    def setExcludeExtensions(self, extensions_str):
        if extensions_str.strip():
            self.exclude_extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        else:
            self.exclude_extensions = []
        self.invalidateFilter()
    
    def setExcludeHidden(self, exclude):
        self.exclude_hidden = exclude
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        if not index.isValid():
            return False
        
        item = self.sourceModel().itemFromIndex(index)
        file_path = item.data(Qt.UserRole)
        if not file_path:
            return False
        
        base_name = os.path.basename(file_path)
        if self.exclude_hidden and base_name.startswith('.'):
            return False
        
        if self.exclude_extensions and os.path.isfile(file_path):
            for ext in self.exclude_extensions:
                if file_path.lower().endswith(ext.lower()):
                    return False
        
        # Apply the inherited QSortFilterProxyModel's filter (for the Search bar).
        if not super(FileFilterProxyModel, self).filterAcceptsRow(source_row, source_parent):
            return False
        
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TreeGen: File tree generator for research data")
        self.resize(1100, 700)
        self.current_directory = None
        self.descriptions = {}
        self.folder_count = 0
        self.file_count = 0
        self.total_size = 0
        self.logo_pixmap = None
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(5)

        # ------------ title-------------- -------------
        title_label = QLabel("TreeGen: File tree generator for research data")
        title_font = QFont()
        title_font.setPointSize(16)     # Increase font size as desired
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # ---------- Usage instructions with Logo ----------
        usage_layout = QHBoxLayout()
        usage_layout.setSpacing(10)
        usage_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(100, 100)  
        self.logo_label.setScaledContents(True)
        self.logo_label.setStyleSheet("border: none;")

        if os.path.exists(LOGO_PATH):
            self.logo_pixmap = QPixmap(LOGO_PATH)
            self.logo_label.setPixmap(self.logo_pixmap)
        usage_layout.addWidget(self.logo_label)
        
        usage_instructions = (
            "<div style='font-size:16px; line-height:1.3; margin:0; padding:0;'>"
            "<ul style='margin-left:18px; padding-left:0;'>"
            "<li><b>Select directory</b>: Choose a folder whose tree you want to generate.</li>"
            "<li><b>Include a description</b>: Browse the folder structure and double-click in the description column to add/edit its description.</li>"
            "<li><b>Export buttons</b>: Export the tree as Markdown (.md) or plain text (.txt).</li>"
            "<li>For further <b>help</b>, copy and open this "
            "<a href='https://alliance-rdm-gdr.github.io/RDM_OnePager/RDM_TreeGen_en.html'>link</a>."
            "</div>"
        )
        instructions_label = QLabel(usage_instructions)
        instructions_label.setWordWrap(True)
        instructions_label.setTextFormat(Qt.RichText)
        usage_layout.addWidget(instructions_label)

        main_layout.addLayout(usage_layout)
        # ----------------------------------------------------------

        # ---------- Top Control Buttons -----------
        top_buttons_layout = QHBoxLayout()
        self.select_dir_button = QPushButton("Select Directory")
        self.select_dir_button.clicked.connect(self.select_directory)

        self.export_md_button = QPushButton("Export to Markdown (.md)")
        self.export_md_button.setEnabled(False)
        self.export_md_button.clicked.connect(self.export_to_markdown)

        self.export_txt_button = QPushButton("Export to Plain Text (.txt)")
        self.export_txt_button.setEnabled(False)
        self.export_txt_button.clicked.connect(self.export_to_plain_text)

        self.about_button = QPushButton("About / Info")
        self.about_button.clicked.connect(self.show_about_info)

        top_buttons_layout.addWidget(self.select_dir_button)
        top_buttons_layout.addWidget(self.export_md_button)
        top_buttons_layout.addWidget(self.export_txt_button)
        top_buttons_layout.addWidget(self.about_button)
        main_layout.addLayout(top_buttons_layout)

        # ---------- Search/Filter Bar and Exclusion Options ---------
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.on_search_text_changed)
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_bar)

        self.exclude_ext_input = QLineEdit()
        self.exclude_ext_input.setPlaceholderText("e.g., .txt, .py")
        self.exclude_ext_input.textChanged.connect(self.on_exclude_ext_changed)
        filter_layout.addWidget(QLabel("Exclude Extensions:"))
        filter_layout.addWidget(self.exclude_ext_input)

        self.exclude_hidden_checkbox = QCheckBox("Exclude Hidden")
        self.exclude_hidden_checkbox.stateChanged.connect(self.on_exclude_hidden_changed)
        filter_layout.addWidget(self.exclude_hidden_checkbox)

        main_layout.addLayout(filter_layout)

        # ---------- Splitter (Tree on left, Preview on right) ---------
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left Pane: File Tree
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)
        left_widget.setLayout(left_layout)

        self.tree_view = QTreeView()
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.doubleClicked.connect(self.add_description)
        left_layout.addWidget(self.tree_view)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Size", "Description"])

        self.proxy_model = FileFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(0)
        self.tree_view.setModel(self.proxy_model)

        # Adjust the header sections
        self.tree_view.header().setDefaultSectionSize(200)
        self.tree_view.header().setSectionResizeMode(0, self.tree_view.header().Stretch)
        self.tree_view.header().setSectionResizeMode(1, self.tree_view.header().ResizeToContents)
        self.tree_view.header().setSectionResizeMode(2, self.tree_view.header().Stretch)

        splitter.addWidget(left_widget)

        # Right Pane: Markdown Preview
        self.preview_text_edit = QTextEdit()
        self.preview_text_edit.setReadOnly(True)
        splitter.addWidget(self.preview_text_edit)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

    # ------------------- Filter callbacks --------------------
    def on_search_text_changed(self, text):
        reg_exp = QRegExp(text, Qt.CaseInsensitive, QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)

    def on_exclude_ext_changed(self, text):
        self.proxy_model.setExcludeExtensions(text)

    def on_exclude_hidden_changed(self, state):
        self.proxy_model.setExcludeHidden(state == Qt.Checked)

    # ------------------- Directory selection & Tree building --------------------
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.current_directory = directory
            self.load_descriptions()
            self.populate_tree()
            self.export_md_button.setEnabled(True)
            self.export_txt_button.setEnabled(True)
            self.update_markdown_preview()

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

                item = QStandardItem(item_name)
                size_item = QStandardItem(size_human_readable)
                desc_item = QStandardItem(description)

                item.setData(item_path, Qt.UserRole)
                item.setIcon(icon)
                size_item.setData(size, Qt.UserRole)
                desc_item.setData(description, Qt.UserRole)

                parent_item.appendRow([item, size_item, desc_item])

                # Recursively process subdirectories
                if os.path.isdir(item_path):
                    self.add_items(item, item_path)

        except PermissionError:
            pass

    def get_folder_size(self, path):
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except (OSError, PermissionError):
                        pass
        return total_size

    def add_description(self, index):
        source_index = self.proxy_model.mapToSource(index)
        item = self.model.itemFromIndex(source_index.sibling(source_index.row(), 0))
        desc_item = self.model.itemFromIndex(source_index.sibling(source_index.row(), 2))
        item_path = item.data(Qt.UserRole)
        current_desc = desc_item.text()

        text, ok = QInputDialog.getMultiLineText(
            self, "Add Description", f"Enter description for:\n{item_path}", current_desc)
        if ok:
            desc_item.setText(text)
            self.descriptions[item_path] = text
            self.save_descriptions()
            self.update_markdown_preview()

    # ------------------- Markdown generation & preview --------------------
    def generate_markdown_content(self):
        self.folder_count = 0
        self.file_count = 0
        self.total_size = 0
        markdown_lines = []

        root_name = os.path.basename(self.current_directory) or self.current_directory
        markdown_lines.append(f"{root_name}")

        self.build_tree(self.current_directory, markdown_lines, prefix='', is_last=True)

        # Summary
        markdown_lines.append('')
        markdown_lines.append('---')
        markdown_lines.append('**Summary:**')
        markdown_lines.append(f'- Total folders: {self.folder_count}')
        markdown_lines.append(f'- Total files: {self.file_count}')
        total_size_hr = humanize.naturalsize(self.total_size)
        markdown_lines.append(f'- Total size: {total_size_hr}')

        return '\n'.join(markdown_lines)

    def update_markdown_preview(self):
        if self.current_directory:
            md_content = self.generate_markdown_content()
            self.preview_text_edit.setPlainText(md_content)

    # ------------------- Build tree text recursively --------------------
    def build_tree(self, path, lines, prefix='', is_last=True):
        try:
            items = os.listdir(path)
            items.sort()
        except PermissionError:
            lines.append(prefix + '└── [Permission Denied]')
            return

        self.folder_count += 1
        pointers = ['├── '] * (len(items) - 1) + ['└── '] if items else []

        for index, item_name in enumerate(items):
            item_path = os.path.join(path, item_name)
            is_dir = os.path.isdir(item_path)
            size = self.get_folder_size(item_path) if is_dir else os.path.getsize(item_path)
            size_hr = humanize.naturalsize(size)

            if is_dir:
                line = f"{prefix}{pointers[index]}**{item_name}**"
            else:
                line = f"{prefix}{pointers[index]}{item_name}"
                self.file_count += 1
                self.total_size += size

            line += f" [ {size_hr} ]"
            lines.append(line)

            description = self.descriptions.get(item_path, "")
            if description:
                comment_prefix = prefix + ('    ' if pointers[index] == '└── ' else '│   ')
                lines.append(f"{comment_prefix}<!-- {description} -->")

            if is_dir:
                new_prefix = prefix + ('    ' if pointers[index] == '└── ' else '│   ')
                self.build_tree(item_path, lines, prefix=new_prefix, is_last=(pointers[index] == '└── '))

        if not items:
            lines.append(prefix + '└── [Empty Folder]')

    # ------------------- Exporters --------------------
    def export_to_markdown(self):
        if not self.current_directory:
            QMessageBox.warning(self, "No Directory Selected", "Please select a directory first.")
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            os.path.join(self.current_directory, "file_tree.md"),
            "Markdown Files (*.md);;All Files (*)",
            options=options
        )
        if file_path:
            md_content = self.generate_markdown_content()
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                QMessageBox.information(self, "Export Successful", f"File tree exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred:\n{str(e)}")

    def export_to_plain_text(self):
        if not self.current_directory:
            QMessageBox.warning(self, "No Directory Selected", "Please select a directory first.")
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Plain Text File",
            os.path.join(self.current_directory, "file_tree.txt"),
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        if file_path:
            txt_content = self.generate_markdown_content()
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
                QMessageBox.information(self, "Export Successful", f"File tree exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred:\n{str(e)}")

    # ------------------- About / Info --------------------
    def show_about_info(self):
        about_text = (
            "TreeGen: File tree generator for research data\n"
            "---------------------\n"
            "This application is developed and manteined by the curation team of the Federated Research Data Repository (https://www.frdr-dfdr.ca/repo/) \n\n"
            "For more information, please visit our website or contact us at rdm-gdr\@alliancecan.ca.\n\n"            
        )
        QMessageBox.information(self, "About / Info", about_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
