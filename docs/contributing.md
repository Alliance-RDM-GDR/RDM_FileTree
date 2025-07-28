# Contributing to TreeGen

We welcome contributions from developers, RDM practitioners and users who want to make this tool better. This document outlines how to propose improvements, report bugs, contribute code, and maintain consistent documentation.

---

## How You Can Help

- 🐛 **Report bugs** via the [Issues](https://github.com/Alliance-RDM-GDR/RDM_FileTree/issues) tab.
- 🛠️ **Submit feature requests** if you have an idea for improvement.
- 📚 **Improve documentation**, including the README, usage instructions, or internal architecture docs.
- 💻 **Contribute code** to fix bugs or implement new features.

---

## Development Guidelines

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use meaningful variable and function names.
- Document functions and classes with clear docstrings.
- UI code should remain modular—keep logic and layout definitions cleanly separated when possible.

### File Structure

- `TreeGen.py` contains the main app logic.
- `docs/` contains all technical documentation (architecture, dependencies, maintenance).
- `tests/` will be added to support test coverage in the future.

---

## Documentation Requirements

All contributions that change the functionality, interface, or user experience must include corresponding updates to the documentation:

- If you add a new feature or GUI element, update the usage instructions in `README.md`.
- If you add or modify internal structures, update `docs/architecture.md`.
- If your change affects how users interact with the software, revise setup or environment notes.
- Link to any relevant external standards or dependencies in Markdown format.

We use [Markdownlint](https://github.com/DavidAnson/markdownlint) to ensure consistency across documentation files. Please run a linter before submitting.

---

## Submitting a Contribution

1. **Fork** the repository to your own GitHub account.
2. **Create a branch** from `main` with a meaningful name
3. **Make your changes** and include tests or updated docs if applicable.
4. **Commit** your changes with a clear message.
5. **Push** to your fork and open a **Pull Request (PR)** against the `main` branch.

The PR should:
- Reference the issue it fixes (if any).
- Include a description of what changed and why.
- Pass all automated tests (if configured).
- Include updated or new documentation if needed.

---

## Review Process

All pull requests are reviewed by a maintainer. They may ask for:
- Clarification or rewording of documentation.
- Code refactoring for clarity or performance.
- Splitting larger PRs into smaller logical pieces.

Once approved, the PR will be merged and added to the next release milestone.

---

## Code of Conduct

All contributors are expected to follow the [Alliance Code of Conduct](https://alliancecan.ca/en/code-of-conduct). Be respectful, constructive, and collaborative.

---

## Questions?

If you’re unsure about where to start, need clarification, or would like to discuss an idea, feel free to open a GitHub Discussion or email us at [rdm-gdr@alliancecan.ca](mailto:rdm-gdr@alliancecan.ca).
