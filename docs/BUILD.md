# Build Process Documentation / Documentation du processus de construction

This document outlines the manual build process for TreeGen to ensuring a consistent and reproducible executable creation.

## English

### Prerequisites

- **Python**: Version 3.10 is required.
- **Environment**: A clean virtual environment (Conda or venv) is recommended to avoid dependency conflicts.

### 1. Setup Environment

Clone the repository and enter the directory:

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
```

Create and activate the environment:

**Using Conda:**

```bash
conda env create -f environment.yml
conda activate treegen-env
```

**Using venv:**

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Verify Dependencies

Ensure all dependencies are installed at the expected versions:

```bash
pip freeze
```

Check that `PyInstaller` is available:

```bash
pyinstaller --version
```

### 3. Build the Executable

Run PyInstaller using the project's specification file. This ensures all settings (windowed mode, one-file, etc.) are applied consistently.

```bash
pyinstaller TreeGen.spec
```

_Note: If specific adjustments are needed (e.g., changing the icon), modify `TreeGen.spec` rather than passing command-line flags._

### 4. Verify the Artifact implementation

The build process will produce two folders:

- `build/`: Temporary build files (can be deleted).
- `dist/`: Contains the final executable.

**Verification Steps:**

1. Navigate to `dist/`.
2. Locate the `TreeGen` (or `TreeGen.exe`) file.
3. Launch the application.
4. Verify the "About" dialog shows the correct version information.
5. Test basic functionality (Select Directory -> Export).

### 5. Cleaning Up

To start a fresh build, remove the generated directories:

```bash
# Windows (PowerShell)
Remove-Item -Recurse -Force build, dist

# macOS/Linux
rm -rf build dist
```

---

## Français

Ce document décrit le processus de construction manuel de TreeGen afin de garantir la création d'un exécutable cohérent et reproductible.

### Prérequis

- **Python** : La version 3.10 est requise.
- **Environnement** : Un environnement virtuel propre (Conda ou venv) est recommandé pour éviter les conflits de dépendances.

### 1. Configuration de l'environnement

Clonez le dépôt et entrez dans le répertoire :

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
```

Créez et activez l'environnement :

**Avec Conda :**

```bash
conda env create -f environment.yml
conda activate treegen-env
```

**Avec venv :**

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Vérification des dépendances

Assurez-vous que toutes les dépendances sont installées dans les versions attendues :

```bash
pip freeze
```

Vérifiez que `PyInstaller` est disponible :

```bash
pyinstaller --version
```

### 3. Construction de l'exécutable

Lancez PyInstaller en utilisant le fichier de spécification du projet. Cela garantit que tous les paramètres (mode fenêtré, fichier unique, etc.) sont appliqués de manière cohérente.

```bash
pyinstaller TreeGen.spec
```

_Remarque : Si des ajustements spécifiques sont nécessaires (par ex. changer l'icône), modifiez `TreeGen.spec` plutôt que de passer des arguments en ligne de commande._

### 4. Vérification de l'artefact

Le processus de construction produira deux dossiers :

- `build/` : Fichiers de construction temporaires (peuvent être supprimés).
- `dist/` : Contient l'exécutable final.

**Étapes de vérification :**

1. Naviguez vers `dist/`.
2. Localisez le fichier `TreeGen` (ou `TreeGen.exe`).
3. Lancez l'application.
4. Vérifiez que la boîte de dialogue "À propos" affiche les bonnes informations de version.
5. Testez les fonctionnalités de base (Sélectionner un dossier -> Exporter).

### 5. Nettoyage

Pour relancer une construction propre, supprimez les répertoires générés :

```bash
# Windows (PowerShell)
Remove-Item -Recurse -Force build, dist

# macOS/Linux
rm -rf build dist
```
