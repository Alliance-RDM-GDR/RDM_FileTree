import sys
import os
import json
import ctypes
import humanize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QTreeView, QAbstractItemView, QInputDialog, QMessageBox,
    QTextEdit, QSplitter, QLabel, QLineEdit, QCheckBox, QSizePolicy
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp

LOGO_PATH = "Alliance_Logo.jpeg"

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4


def is_hidden_path(path):
    """
    Determine whether a path should be treated as hidden.
    On Windows this checks the hidden/system file attributes; elsewhere it falls back to dot-prefix.
    """
    path_str = os.fspath(path)
    if sys.platform.startswith("win"):
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(path_str)
        except (AttributeError, ValueError):
            attrs = 0xFFFFFFFF
        if attrs == 0xFFFFFFFF:
            return os.path.basename(path_str).startswith(".")
        return bool(attrs & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM))
    return os.path.basename(path_str).startswith(".")


def should_exclude_entry(path, is_dir, exclude_hidden=False, exclude_extensions=None):
    exclude_extensions = exclude_extensions or []
    if exclude_hidden and is_hidden_path(path):
        return True
    if not is_dir and exclude_extensions:
        lower_path = os.fspath(path).lower()
        for ext in exclude_extensions:
            if lower_path.endswith(ext):
                return True
    return False


def iter_visible_children(path, exclude_hidden=False, exclude_extensions=None):
    exclude_extensions = exclude_extensions or []
    entries = []
    with os.scandir(path) as iterator:
        for entry in iterator:
            child_path = entry.path
            is_dir = entry.is_dir(follow_symlinks=False)
            if should_exclude_entry(child_path, is_dir, exclude_hidden, exclude_extensions):
                continue
            entries.append((entry.name, child_path, is_dir))
    entries.sort(key=lambda item: item[0].lower())
    return entries


def calculate_folder_size(path, exclude_hidden=False, exclude_extensions=None):
    exclude_extensions = exclude_extensions or []
    total_size = 0
    try:
        with os.scandir(path) as iterator:
            for entry in iterator:
                entry_path = entry.path
                is_dir = entry.is_dir(follow_symlinks=False)
                if should_exclude_entry(entry_path, is_dir, exclude_hidden, exclude_extensions):
                    continue
                if is_dir:
                    total_size += calculate_folder_size(entry_path, exclude_hidden, exclude_extensions)
                else:
                    try:
                        total_size += entry.stat(follow_symlinks=False).st_size
                    except (OSError, PermissionError):
                        pass
    except (PermissionError, FileNotFoundError):
        pass
    return total_size

class FileFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FileFilterProxyModel, self).__init__(parent)
        self.exclude_extensions = []
        self.exclude_hidden = False
        self.setRecursiveFilteringEnabled(True)
    
    def setExcludeExtensions(self, extensions_str):
        if extensions_str.strip():
            self.exclude_extensions = [
                ext.strip().lower() for ext in extensions_str.split(",") if ext.strip()
            ]
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
        
        if self.exclude_hidden and is_hidden_path(file_path):
            return False
        
        if self.exclude_extensions and os.path.isfile(file_path):
            lower_path = file_path.lower()
            for ext in self.exclude_extensions:
                if lower_path.endswith(ext):
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

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.setChildrenCollapsible(False)
        main_layout.addWidget(vertical_splitter)

        # ---------- Header / Controls Panel ----------
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        header_widget.setLayout(header_layout)

        title_label = QLabel("TreeGen: File tree generator for research data")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

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
            "<div style='font-size:15px; line-height:1.5; margin:0; padding:0;'>"
            "<ol style='margin-left:20px; padding-left:0;'>"
            "<li><b>Select Directory</b>: Choose the folder you want to describe.</li>"
            "<li><b>Describe</b>: Browse the file tree, double-click the description column, and use the filters as needed.</li>"
            "<li><b>Export</b>: Review the preview, then export to Markdown or plain text.</li>"
            "</ol>"
            "<p style='margin-top:10px; margin-left:40px'>For additional guidance, visit the "
            "<a href='https://alliance-rdm-gdr.github.io/CUR_Res_OnePagers/RDM_TreeGen_en.html'>TreeGen one-pager</a> "
            "or the "
            "<a href='https://github.com/Alliance-RDM-GDR/RDM_FileTree'>GitHub repository</a>.</p>"
            "</div>"
        )
        instructions_label = QLabel(usage_instructions)
        instructions_label.setWordWrap(True)
        instructions_label.setTextFormat(Qt.RichText)
        instructions_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        instructions_label.setOpenExternalLinks(True)
        usage_layout.addWidget(instructions_label)
        header_layout.addLayout(usage_layout)

        top_buttons_layout = QHBoxLayout()
        self.select_dir_button = QPushButton("Select Directory")
        self.select_dir_button.clicked.connect(self.select_directory)

        self.about_button = QPushButton("About / Info")
        self.about_button.clicked.connect(self.show_about_info)

        top_buttons_layout.addWidget(self.select_dir_button)
        top_buttons_layout.addStretch(1)
        top_buttons_layout.addWidget(self.about_button)
        header_layout.addLayout(top_buttons_layout)

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

        header_layout.addLayout(filter_layout)
        header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # ---------- Tree / Preview Panel ----------
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)
        content_widget.setLayout(content_layout)

        splitter = QSplitter(Qt.Horizontal)
        content_layout.addWidget(splitter)

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

        export_layout = QHBoxLayout()
        export_layout.setContentsMargins(0, 5, 0, 0)

        self.export_md_button = QPushButton("Export Markdown (.md)")
        self.export_md_button.setEnabled(False)
        self.export_md_button.clicked.connect(self.export_to_markdown)

        self.export_txt_button = QPushButton("Export Plain Text (.txt)")
        self.export_txt_button.setEnabled(False)
        self.export_txt_button.clicked.connect(self.export_to_plain_text)

        export_layout.addStretch(1)
        export_layout.addWidget(self.export_md_button)
        export_layout.addWidget(self.export_txt_button)
        content_layout.addLayout(export_layout)

        vertical_splitter.addWidget(header_widget)
        vertical_splitter.addWidget(content_widget)
        vertical_splitter.setStretchFactor(0, 0)
        vertical_splitter.setStretchFactor(1, 1)
        header_widget.setMaximumHeight(header_widget.sizeHint().height())

    # ------------------- Filter callbacks --------------------
    def on_search_text_changed(self, text):
        reg_exp = QRegExp(text, Qt.CaseInsensitive, QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)

    def on_exclude_ext_changed(self, text):
        self.proxy_model.setExcludeExtensions(text)
        if self.current_directory:
            self.update_markdown_preview()

    def on_exclude_hidden_changed(self, state):
        self.proxy_model.setExcludeHidden(state == Qt.Checked)
        if self.current_directory:
            self.update_markdown_preview()

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

    def get_folder_size(self, path, respect_filters=False):
        exclude_hidden = self.proxy_model.exclude_hidden if respect_filters else False
        exclude_extensions = self.proxy_model.exclude_extensions if respect_filters else []
        return calculate_folder_size(path, exclude_hidden, exclude_extensions)

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
        exclude_hidden = self.proxy_model.exclude_hidden
        exclude_extensions = self.proxy_model.exclude_extensions

        try:
            items = iter_visible_children(path, exclude_hidden, exclude_extensions)
        except PermissionError:
            connector = '\\-- ' if is_last else '|-- '
            lines.append(f"{prefix}{connector}[Permission Denied]")
            return
        except FileNotFoundError:
            connector = '\\-- ' if is_last else '|-- '
            lines.append(f"{prefix}{connector}[Not Found]")
            return

        self.folder_count += 1

        if not items:
            connector = '\\-- ' if is_last else '|-- '
            lines.append(f"{prefix}{connector}[Empty Folder]")
            return

        connectors = ['|-- '] * (len(items) - 1) + ['\\-- ']

        for index, (item_name, item_path, is_dir) in enumerate(items):
            connector = connectors[index]
            size = self.get_folder_size(item_path, respect_filters=True) if is_dir else 0

            if not is_dir:
                try:
                    size = os.path.getsize(item_path)
                except (OSError, PermissionError):
                    size = 0

            size_hr = humanize.naturalsize(size)

            if is_dir:
                line = f"{prefix}{connector}**{item_name}**"
            else:
                line = f"{prefix}{connector}{item_name}"
                self.file_count += 1
                self.total_size += size

            line += f" [ {size_hr} ]"
            lines.append(line)

            description = self.descriptions.get(item_path, "")
            if description:
                comment_prefix = prefix + ('    ' if connector == '\\-- ' else '|   ')
                lines.append(f"{comment_prefix}<!-- {description} -->")

            if is_dir:
                new_prefix = prefix + ('    ' if connector == '\\-- ' else '|   ')
                self.build_tree(item_path, lines, prefix=new_prefix, is_last=(connector == '\\-- '))

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
            "This application is developed and maintained by the Curation Services team of the Digital Research Alliance of Canada (https://alliancecan.ca).\n\n"
            "Including a clear file tree helps repositories evaluate submissions faster. Consider FRDR (https://www.frdr-dfdr.ca/repo/) "
            "and Borealis (https://borealisdata.ca) when sharing Canadian research data.\n\n"
            "For more information or support, contact us at rdm-gdr@alliancecan.ca.\n"
        )
        QMessageBox.information(self, "About / Info", about_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



