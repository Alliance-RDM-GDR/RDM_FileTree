# TreeGen: File Tree Generator for Research Data

## English

**TreeGen** is a cross-platform desktop application developed by the Digital Research Alliance of Canada. It helps researchers, data curators, and technical teams document and share folder hierarchies in a clear, consistent, and citable format. Users can visualize a directory, add contextual descriptions, and export the structure as Markdown or plain text, with full support for English and French.

---

### Overview

TreeGen streamlines file tree documentation by:

- Automatically listing folder and file names with human-readable sizes
- Allowing inline editing of descriptions that persist between sessions
- Rendering a live Markdown preview that mirrors filters and annotations
- Providing one-click exports to `.md` and `.txt`
- Remembering the preferred language across sessions

This workflow is ideal for research data management, dataset publication, software documentation, and reproducible workflows.

---

### Features

- **Interactive Tree:** Browse and annotate an expandable hierarchy.
- **Bilingual Interface:** Switch between English and French without restarting the app.
- **Live Preview:** Inspect the Markdown output before exporting.
- **Search & Filters:** Locate entries, hide hidden or system files, and skip selected extensions.
- **Localized Exports:** Markdown and text exports include localized summaries and messages.
- **Offline Friendly:** All processing happens locally; no internet connection is required.

---

- **Use on Unmanaged Devices:** Be cautious when scanning sensitive data on personal or shared devices, as standard security controls may vary.

---

### Installation

**Option A - Download the Executable**  
Grab the installer or standalone executable for your platform from the [Releases](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases) page.

> [!NOTE] > **Official Source**: GitHub Releases is the **only** official source for TreeGen executables.
> **Security Warning**: Binaries are currently **unsigned**. You may need to bypass OS security warnings (e.g., "Unidentified Developer" on macOS or SmartScreen on Windows) to run them.

**Option B - Run from Source**

Requirements: Python 3.10+, see `environment.yml` or `requirements.txt` for dependencies.

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
conda env create -f environment.yml
conda activate treegen-env
python TreeGen.py
```

**Build from Source (Reproducible Build)**  
For instructions on building the executable yourself relative to the source code, see [Building TreeGen](docs/BUILD.md).

---

### Security & Data Privacy

- **Metadata Exposure**: TreeGen lists file names and folder paths. While it does _not_ access file contents, be aware that directory structures themselves can reveal sensitive information (e.g., project code names, participant IDs).
- **Persistent Annotations**: Descriptions are stored in a hidden file named `.descriptions.json` inside the scanned directory. This file **remains unless manually deleted**.
- **Version Control**: If you are using Git, add `.descriptions.json` to your `.gitignore` file to prevent accidentally committing internal notes or descriptions to public repositories.

---

### Updates

TreeGen does not have an automatic update mechanism. Please check the [Releases](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases) page periodically for new versions and security fixes. All updates will be documented in [UPDATES.md](UPDATES.md).

---

### Usage Guide

1. Launch TreeGen and click **Select Directory** to load a folder. Existing annotations in `.descriptions.json` are restored automatically.
2. Explore the tree, double-click entries to edit descriptions, and adjust filters as needed.
3. Use the **Language** dropdown at the top-right to switch between English and French. Your choice persists between sessions.
4. Export to Markdown or plain text when ready. The output reflects the active filters, descriptions, and language.

For more detail, see the [Quick Start Tutorial](docs/QuickStart.md).

---

### Documentation

- [Architecture Overview](docs/architecture.md)
- [Quick Start Tutorial](docs/QuickStart.md)
- [Software Management Plan](docs/SoftwareManagementPlan.pdf)
- [Update Log](UPDATES.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

---

### License

TreeGen is released under the [MIT License](LICENSE).

---

### Citation

If TreeGen supports your work, please cite it using the metadata in [`CITATION.cff`](CITATION.cff) or reference the Zenodo archive (10.5281/zenodo.17289197).

---

### Contact

Questions or feedback? Email [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca).

Digital Research Alliance of Canada

---

## Français

**TreeGen** est une application de bureau multiplateforme développée par l'Alliance de recherche numérique du Canada. Elle aide les chercheuses, chercheurs, conservateurs et équipes techniques à documenter et partager la structure de leurs dossiers de façon claire, uniforme et citable. L'utilisateur peut visualiser un répertoire, ajouter des descriptions contextuelles et exporter l'arborescence en Markdown ou en texte brut, avec prise en charge complète du français et de l'anglais.

---

### Aperçu

TreeGen simplifie la documentation d'arborescences en :

- Listant automatiquement les dossiers et fichiers avec des tailles lisibles
- Permettant la modification directe des descriptions, conservées d'une session à l'autre
- Offrant un aperçu Markdown en temps réel reflétant filtres et annotations
- Proposant une exportation simple vers `.md` et `.txt`
- Mémorisant la langue préférée d'une session à l'autre

Cette approche est idéale pour la gestion des données de recherche, la publication de jeux de données, la documentation logicielle et les flux de travail reproductibles.

---

### Fonctionnalités

- **Arborescence interactive :** Parcourez et annotez une hiérarchie extensible.
- **Interface bilingue :** Passez du français à l'anglais sans redémarrer l'application.
- **Aperçu en direct :** Vérifiez le rendu Markdown avant l'exportation.
- **Recherche et filtres :** Trouvez des éléments, masquez les fichiers cachés ou système et excluez certaines extensions.
- **Exportations localisées :** Les exports Markdown et texte incluent des résumés et messages traduits.
- **Utilisation hors ligne :** Toutes les opérations sont effectuées localement, sans connexion Internet.

---

### Installation

**Option A - Télécharger l'exécutable**  
Téléchargez l'installateur ou l'exécutable autonome correspondant à votre plateforme depuis la page des [versions](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases).

> [!NOTE] > **Source officielle** : Les versions GitHub sont la **seule** source officielle pour les exécutables TreeGen.
> **Avertissement de sécurité** : Les binaires ne sont actuellement **pas signés**. Vous devrez peut-être contourner les avertissements de sécurité du système d'exploitation (par ex. « Développeur non identifié » sur macOS ou SmartScreen sur Windows) pour les exécuter.

**Option B - Lancer depuis le code source**

Exigences : Python 3.10+, voir `environment.yml` ou `requirements.txt` pour les dépendances.

```bash
git clone https://github.com/Alliance-RDM-GDR/RDM_FileTree.git
cd RDM_FileTree
conda env create -f environment.yml
conda activate treegen-env
python TreeGen.py
```

**Construire depuis la source (Build reproductible)**
Pour savoir comment construire vous-même l'exécutable à partir du code source, consultez [Construire TreeGen](docs/BUILD.md).

---

### Sécurité et confidentialité des données

- **Exposition des métadonnées** : TreeGen liste les noms de fichiers et les chemins des dossiers. Bien qu'il n'accède _pas_ au contenu des fichiers, soyez conscient que la structure des répertoires elle-même peut révéler des informations sensibles (par ex. noms de code de projets, identifiants de participants).
- **Annotations persistantes** : Les descriptions sont stockées dans un fichier caché nommé `.descriptions.json` à l'intérieur du répertoire analysé. Ce fichier **reste présent à moins d'être supprimé manuellement**.
- **Contrôle de version** : Si vous utilisez Git, ajoutez `.descriptions.json` à votre fichier `.gitignore` pour éviter de commettre accidentellement des notes internes ou des descriptions dans des dépôts publics.

---

### Mises à jour

TreeGen ne dispose pas de mécanisme de mise à jour automatique. Veuillez consulter périodiquement la page des [versions](https://github.com/Alliance-RDM-GDR/RDM_FileTree/releases) pour les nouvelles versions et les correctifs de sécurité. Toutes les mises à jour seront documentées dans [UPDATES.md](UPDATES.md).

---

### Guide d'utilisation

1. Lancez TreeGen et cliquez sur **Sélectionner un dossier** pour charger un répertoire. Les annotations existantes dans `.descriptions.json` sont restaurées automatiquement.
2. Parcourez l'arborescence, double-cliquez pour modifier les descriptions et ajustez les filtres au besoin.
3. Utilisez le menu **Langue** en haut à droite pour basculer entre français et anglais. Votre choix est conservé d'une session à l'autre.
4. Exportez en Markdown ou en texte brut lorsque vous êtes prêt. Le résultat reflète les filtres, descriptions et la langue active.

Pour plus de détails, consultez le [Tutoriel de démarrage rapide](docs/QuickStart.md).

---

### Documentation

- [Aperçu de l'architecture](docs/architecture.md)
- [Guide de démarrage rapide](docs/QuickStart.md)
- [Plan de gestion logicielle](docs/SoftwareManagementPlan.pdf)
- [Journal des mises à jour](UPDATES.md)
- [Guide de contribution](docs/CONTRIBUTING.md)
- [Instructions de construction](docs/BUILD.md)

---

### Licence

TreeGen est distribué sous la [licence MIT](LICENSE).

---

### Citation

Si TreeGen vous est utile, veuillez le citer à l'aide des informations contenues dans [`CITATION.cff`](CITATION.cff) ou du DOI Zenodo (10.5281/zenodo.17289197).

---

### Contact

Pour toute question ou rétroaction, écrivez à [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca).

Alliance de recherche numérique du Canada

---

_Last updated / Dernière mise à jour : 2026-01-07_
