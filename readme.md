# Merger for Obsidian Markdown Editor

The following program merges Markdown files in Obsidian in order to allow for easier exports.  This optimises your workflow for both exporting to a PDF and exporting for use in LLMs.

## Templates

Found in `/templates`, the program works with the folder structure:
```bash
└── vault
     └── Root Folder
          ├── Topics
          └── Concepts
```

`/templates/CSC Concept.md` is a basic template for a concept (sub-topic) and only contains a title and a tag for any topics it's referenced in.

`/templates/CSC Topic Overview.md` is the temaplte for a topic, including headers for an overview, list of concepts, exam questions etc.

To use these templates in your own vault, copy the files into `vault/templates/`, and follow the instructions found [in the Obsidian Documentation](https://obsidian.md/help/plugins/templates)

## Outputs

By running this script from the Root Folder, a Topic file for $N$ topics will be created in the root folder, 
which includes the topic overview, as well as every concept in the order they appear in the overview file.  This 
allows for a single PDF to be created using Obsidian's PDF export.  
Additionally, an overview file will be created, containing all topics and concepts in one file.  The purpose
of this file is to allow for LLM injestion to create a source of truth for conversations.

## Usage 

### Directory and File Naming

Each topic file should follow the naming convention: `Topic X - Topic Name.md`

Each tag should follow the naming convention: `Root Folder_Topic Number`

i.e. If the root folder is `ABC1010` and the topic is `Topic 1 - Introduction.md`, each concept used in the topic should be tagged with `#ABC1010_1`.
Please note, if the root directory begins with `CSC`, this is dropped from each tag, i.e. `#CSC1010_1` becomes `#1010_1`.

### Running the Script

#### Prerequisites
- Python 3 installed (`python3 --version`)
- Your vault follows the required structure:
  - `Topics/`
  - `Concepts/`

---

#### Option 1 — Run from the Root Folder (recommended)

Navigate to your module root directory (e.g. `ABC1010`):

```bash
cd "/path/to/your/vault/ABC1010"
```

Run the script:

```bash
python3 /path/to/obsidianMerger/script.py .
```

---

#### Option 2 — Run from anywhere

You can also pass the path explicitly:

```bash
python3 /path/to/obsidianMerger/script.py "/path/to/your/vault/ABC1010"
```

---

#### Optional — Create a shell shortcut (zsh)

To avoid typing the full path every time, add this function to your `~/.zshrc`:

```bash
obsidian-merge() {
  python3 /path/to/obsidianMerger/script.py "$(pwd)"
}
```

Then reload your shell:

```bash
source ~/.zshrc
```

Now you can simply run:

```bash
obsidian-merge
```

from inside any valid root folder.

---

#### Output

Running the script will generate:

- `Topic Overview 1.md`, `Topic Overview 2.md`, ..., `Topic Overview N.md`
- `<module>_module_summary.md` (e.g. `1010_module_summary.md`)

All files are created in the root folder.

---

#### Notes

- The script must be run from (or pointed to) the root folder containing `Topics/` and `Concepts/`
- Concept links must match filenames exactly: `[[Concept Name]]`
- If a concept file is missing, it will be skipped, with a list of skipped files printed to the console
- Only concept files within the `## Concepts` section of the overview file will be included
- Only concept files within the `/Vault/Root Folder/Concepts/` folder will be included
