# TreeGen: Quick Start Tutorial

## English

Welcome to **TreeGen**, the desktop application that helps you describe and share your folder structures in a clean, repeatable way. This guide covers installation, the main interface, and the export workflow, followed by tips to make the most of the new bilingual release.

---
### 1. Installation

**Option A - Download the Executable**  
Grab the installer or standalone executable that matches your operating system from the [Releases](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases) page and launch TreeGen directly.

**Option B - Run from Source**

Requirements:

- Python 3.10 or later
- Conda or another virtual environment tool (recommended)

Steps:

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
conda env create -f environment.yml
conda activate treegen-env
python TreeGen.py
```

Optional build step (creates a single-file executable):

```bash
pyinstaller --onefile --windowed TreeGen.py
```

---
### 2. User Interface Overview

TreeGen presents a split layout:

- **Header:** App title, the Alliance logo, usage instructions, and top-row controls (Select Directory, Language dropdown, About / Info).
- **Left Pane:** A `QTreeView` with expandable folders and editable descriptions.
- **Right Pane:** A read-only Markdown preview that refreshes automatically.
- **Filter Bar:** Search, exclude-extension entry, and an "Exclude Hidden" toggle.

You can switch between English and French at any time using the `Language` dropdown. TreeGen remembers your choice for the next session.

---
### 3. Creating a File Tree

1. **Select a directory.** Click **Select Directory** and choose the root folder you want to document. TreeGen loads any existing `.descriptions.json` file in that directory.
2. **Explore and annotate.** Expand folders, then double-click the Description column to add context or notes. Filters and search update instantly.
3. **Review the preview.** The Markdown pane mirrors your filters and annotations so you can confirm exactly what will be exported.

---
### 4. Exporting

- **Export Markdown (.md):** Generates a Markdown file with bold folder names, file sizes, annotations (as HTML comments), and a localized summary of totals.
- **Export Plain Text (.txt):** Produces a plain-text equivalent using the same content.

Both export options respect the current language, filters, and descriptions. TreeGen shows a localized success or error dialog after every export attempt.

---
### 5. Tips and Best Practices

- TreeGen stores descriptions in `.descriptions.json`. Commit or back up that file to retain annotations.
- Use the language selector before exporting to ensure the report is generated in the desired language.
- The About / Info dialog contains quick links to Alliance resources, FRDR, and Borealis repositories.
- Hidden files and excluded extensions remain hidden in both the preview and export, preserving a clean hierarchy.

---
### 6. Support and Citation

Need help? Check the [README](../README.md) or email [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca).  
Please cite TreeGen using the information in `CITATION.cff` or the Zenodo DOI (10.5281/zenodo.17289197).

---

## Français

Bienvenue dans **TreeGen**, l'application de bureau qui vous aide à décrire et à partager la structure de vos dossiers de manière claire et reproductible. Ce guide présente l'installation, l'interface principale et le processus d'exportation, suivis de conseils pour profiter de la nouvelle version bilingue.

---
### 1. Installation

**Option A - Télécharger l'exécutable**  
Récupérez l'installateur ou l'exécutable autonome correspondant à votre système d'exploitation sur la page des [versions](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases), puis lancez TreeGen directement.

**Option B - Lancer depuis le code source**

Exigences :

- Python 3.10 ou version ultérieure
- Conda ou un autre gestionnaire d'environnements virtuels (recommandé)

Étapes :

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
conda env create -f environment.yml
conda activate treegen-env
python TreeGen.py
```

Étape facultative (crée un exécutable autonome) :

```bash
pyinstaller --onefile --windowed TreeGen.py
```

---
### 2. Aperçu de l'interface

TreeGen propose une interface en panneaux :

- **En-tête :** Titre de l'application, logo de l'Alliance, instructions et commandes principales (Sélectionner un dossier, menu Langue, À propos / Info).
- **Volet gauche :** Un `QTreeView` avec dossiers extensibles et descriptions éditables.
- **Volet droit :** Un aperçu Markdown en lecture seule qui se met à jour automatiquement.
- **Barre de filtres :** Recherche, champ d'exclusion d'extensions et case « Exclure les éléments cachés ».

Vous pouvez passer de l'anglais au français (et inversement) à tout moment grâce au menu `Langue`. TreeGen mémorise votre choix pour la session suivante.

---
### 3. Création d'une arborescence

1. **Sélectionnez un dossier.** Cliquez sur **Sélectionner un dossier** et choisissez le répertoire racine à documenter. TreeGen charge tout fichier `.descriptions.json` existant dans ce dossier.
2. **Explorez et annotez.** Déployez les dossiers, puis double-cliquez la colonne Description pour ajouter des notes. Les filtres et la recherche s'appliquent immédiatement.
3. **Vérifiez l'aperçu.** Le volet Markdown reflète vos filtres et annotations afin de valider le contenu avant exportation.

---
### 4. Exportation

- **Exporter en Markdown (.md) :** Génère un fichier Markdown avec noms de dossiers en gras, tailles des fichiers, annotations (commentaires HTML) et un résumé localisé.
- **Exporter en texte brut (.txt) :** Produit un équivalent texte utilisant les mêmes informations.

Les deux formats respectent la langue active, les filtres et les descriptions. TreeGen affiche un message localisé de réussite ou d'erreur après chaque export.

---
### 5. Conseils pratiques

- TreeGen enregistre les descriptions dans `.descriptions.json`. Conservez ce fichier pour garder vos annotations.
- Sélectionnez la langue voulue avant d'exporter afin que le rapport soit généré dans la bonne langue.
- La boîte de dialogue À propos / Info contient des liens vers les ressources de l'Alliance, ainsi que vers les dépôts FRDR et Borealis.
- Les fichiers cachés et extensions exclues sont également ignorés lors de l'export, pour une arborescence claire.

---
### 6. Soutien et citation

Besoin d'aide ? Consultez le [README](../README.md) ou écrivez à [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca).  
Pour citer TreeGen, utilisez les renseignements fournis dans `CITATION.cff` ou le DOI Zenodo (10.5281/zenodo.17289197).

---

*Alliance de recherche numérique du Canada*
