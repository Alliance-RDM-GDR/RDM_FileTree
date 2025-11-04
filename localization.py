"""Localization utilities and translations for TreeGen."""

from __future__ import annotations

from typing import Dict, Iterable

AVAILABLE_LANGUAGES: Iterable[str] = ("en", "fr")
DEFAULT_LANGUAGE = "en"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "TreeGen: File tree generator for research data",
        "usage_instructions": (
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
        ),
        "select_directory_button": "Select Directory",
        "about_button": "About / Info",
        "language_label": "Language:",
        "language_name_en": "English",
        "language_name_fr": "French",
        "search_label": "Search:",
        "search_placeholder": "Search...",
        "exclude_extensions_label": "Exclude Extensions:",
        "exclude_extensions_placeholder": "e.g., .txt, .py",
        "exclude_hidden_checkbox": "Exclude Hidden",
        "tree_column_name": "Name",
        "tree_column_size": "Size",
        "tree_column_description": "Description",
        "export_md_button": "Export Markdown (.md)",
        "export_txt_button": "Export Plain Text (.txt)",
        "select_directory_dialog": "Select Directory",
        "add_description_title": "Add Description",
        "add_description_prompt": "Enter description for:\n{path}",
        "summary_heading": "**Summary:**",
        "summary_total_folders": "- Total folders: {count}",
        "summary_total_files": "- Total files: {count}",
        "summary_total_size": "- Total size: {size}",
        "permission_denied": "[Permission Denied]",
        "not_found": "[Not Found]",
        "empty_folder": "[Empty Folder]",
        "no_directory_title": "No Directory Selected",
        "no_directory_message": "Please select a directory first.",
        "save_markdown_dialog": "Save Markdown File",
        "save_markdown_default_filename": "file_tree.md",
        "markdown_file_filter": "Markdown Files (*.md);;All Files (*)",
        "save_plain_text_dialog": "Save Plain Text File",
        "save_plain_text_default_filename": "file_tree.txt",
        "plain_text_file_filter": "Text Files (*.txt);;All Files (*)",
        "export_success_title": "Export Successful",
        "export_success_message": "File tree exported to {path}",
        "export_failed_title": "Export Failed",
        "export_failed_message": "An error occurred:\n{error}",
        "about_dialog_title": "About / Info",
        "about_dialog_body": (
            "TreeGen: File tree generator for research data\n"
            "---------------------\n"
            "This application is developed and maintained by the Curation Services team of the "
            "Digital Research Alliance of Canada (https://alliancecan.ca).\n\n"
            "Including a clear file tree helps repositories evaluate submissions faster. Consider FRDR "
            "(https://www.frdr-dfdr.ca/repo/) and Borealis (https://borealisdata.ca) when sharing "
            "Canadian research data.\n\n"
            "For more information or support, contact us at rdm-gdr@alliancecan.ca.\n"
        ),
    },
    "fr": {
        "app_title": "TreeGen : Générateur d'arborescence de fichiers pour les données de recherche",
        "usage_instructions": (
            "<div style='font-size:15px; line-height:1.5; margin:0; padding:0;'>"
            "<ol style='margin-left:20px; padding-left:0;'>"
            "<li><b>Sélectionner un dossier</b> : Choisissez le dossier que vous souhaitez décrire.</li>"
            "<li><b>Décrire</b> : Parcourez l'arborescence, double-cliquez la colonne Description et utilisez les filtres au besoin.</li>"
            "<li><b>Exporter</b> : Vérifiez l'aperçu, puis exportez en Markdown ou en texte brut.</li>"
            "</ol>"
            "<p style='margin-top:10px; margin-left:40px'>Pour plus de détails, consultez la "
            "<a href='https://alliance-rdm-gdr.github.io/CUR_Res_OnePagers/RDM_TreeGen_en.html'>fiche TreeGen</a> "
            "ou le "
            "<a href='https://github.com/Alliance-RDM-GDR/RDM_FileTree'>dépôt GitHub</a>.</p>"
            "</div>"
        ),
        "select_directory_button": "Sélectionner un dossier",
        "about_button": "À propos / Info",
        "language_label": "Langue :",
        "language_name_en": "Anglais",
        "language_name_fr": "Français",
        "search_label": "Recherche :",
        "search_placeholder": "Recherche...",
        "exclude_extensions_label": "Exclure les extensions :",
        "exclude_extensions_placeholder": "p. ex., .txt, .py",
        "exclude_hidden_checkbox": "Exclure les éléments cachés",
        "tree_column_name": "Nom",
        "tree_column_size": "Taille",
        "tree_column_description": "Description",
        "export_md_button": "Exporter en Markdown (.md)",
        "export_txt_button": "Exporter en texte brut (.txt)",
        "select_directory_dialog": "Sélectionner un dossier",
        "add_description_title": "Ajouter une description",
        "add_description_prompt": "Saisissez la description pour :\n{path}",
        "summary_heading": "**Résumé :**",
        "summary_total_folders": "- Total de dossiers : {count}",
        "summary_total_files": "- Total de fichiers : {count}",
        "summary_total_size": "- Taille totale : {size}",
        "permission_denied": "[Permission refusée]",
        "not_found": "[Introuvable]",
        "empty_folder": "[Dossier vide]",
        "no_directory_title": "Aucun dossier sélectionné",
        "no_directory_message": "Veuillez d'abord sélectionner un dossier.",
        "save_markdown_dialog": "Enregistrer le fichier Markdown",
        "save_markdown_default_filename": "arborescence.md",
        "markdown_file_filter": "Fichiers Markdown (*.md);;Tous les fichiers (*)",
        "save_plain_text_dialog": "Enregistrer le fichier texte",
        "save_plain_text_default_filename": "arborescence.txt",
        "plain_text_file_filter": "Fichiers texte (*.txt);;Tous les fichiers (*)",
        "export_success_title": "Exportation réussie",
        "export_success_message": "Arborescence exportée vers {path}",
        "export_failed_title": "Échec de l'exportation",
        "export_failed_message": "Une erreur s'est produite :\n{error}",
        "about_dialog_title": "À propos / Info",
        "about_dialog_body": (
            "TreeGen : Générateur d'arborescence de fichiers pour les données de recherche\n"
            "---------------------\n"
            "Cette application est développée et maintenue par l'équipe des services de curation de "
            "l'Alliance de recherche numérique du Canada (https://alliancecan.ca).\n\n"
            "Fournir une arborescence claire aide les dépôts à évaluer les dépôts plus rapidement. Pensez à FRDR "
            "(https://www.frdr-dfdr.ca/repo/) et Borealis (https://borealisdata.ca) pour partager vos données de recherche canadiennes.\n\n"
            "Pour plus d'information ou de soutien, écrivez-nous à rdm-gdr@alliancecan.ca.\n"
        ),
    },
}

LANGUAGE_DISPLAY_NAMES: Dict[str, Dict[str, str]] = {
    "en": {"en": "English", "fr": "French"},
    "fr": {"en": "Anglais", "fr": "Français"},
}


class Localization:
    """Simple dictionary-based localization helper with graceful fallbacks."""

    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        self._language = DEFAULT_LANGUAGE
        self.set_language(language)

    @property
    def language(self) -> str:
        return self._language

    def set_language(self, language: str) -> None:
        """Select the active language, falling back to the default when missing."""
        self._language = language if language in TRANSLATIONS else DEFAULT_LANGUAGE

    def tr(self, key: str, **kwargs) -> str:
        """Translate a key using the current language with formatting support."""
        lang_map = TRANSLATIONS.get(self._language, {})
        text = lang_map.get(key)
        if text is None:
            text = TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                # Leave text unformatted if placeholders do not match.
                pass
        return text

    def available_languages(self) -> Iterable[str]:
        return AVAILABLE_LANGUAGES

    def language_name(self, language: str) -> str:
        names = LANGUAGE_DISPLAY_NAMES.get(self._language)
        if names is None:
            names = LANGUAGE_DISPLAY_NAMES[DEFAULT_LANGUAGE]
        return names.get(language, language)


__all__ = ["Localization", "AVAILABLE_LANGUAGES", "DEFAULT_LANGUAGE"]
