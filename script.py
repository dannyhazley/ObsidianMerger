#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import re
from pathlib import Path
import sys

def get_concepts_per_topic(concept_block):
    return re.findall(r"\[\[(.*?)\]\]", concept_block)

def strip_tag(content):
    return re.sub(r"#\w+_\d+\s*$", "", content.strip())

def get_relationships(path):
    topics_path = Path(path) / "Topics"

    results = {}

    for file in listdir(topics_path):
        file_path = join(topics_path, file)

        if isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r"## Concepts\s*([\s\S]*?)(?=\n## |\Z)", content)

            if match:
                concepts = get_concepts_per_topic(match.group(1))
                results[Path(file).stem] = concepts

    return  dict(sorted(results.items()))

def read_topic(path, topic_name):
    path = join(path, "Topics")
    topic_path = join(path, topic_name + ".md")

    content = ""
    with open(topic_path, "r", encoding="utf-8") as f:
        content = f.read()

    return prepend_title(content, topic_name)

def read_concept(path, concept_name):
    path = join(path, "Concepts")
    concept_path = join(path, concept_name + ".md")

    if not Path(concept_path).exists():
        return None

    with open(concept_path, "r", encoding="utf-8") as f:
        content = f.read()

    return prepend_title(content, concept_name)

def prepend_title(content, title):
    return f"# {title}\n\n{content}"

def get_topic_overview_concepts_as_string(path, topic, topic_rels):
    match = re.search(r"Topic\s*(\d+)\s*-\s*(.*)", topic)
    topic_number = match.group(1) if match else "0"

    all_concepts = []
    skipped = []

    topic_content = read_topic(path, topic)
    all_concepts.append(strip_tag(topic_content))

    for concept_title in topic_rels:
        concept_content = read_concept(path, concept_title)

        if concept_content is None:
            skipped.append(concept_title)
            continue

        cleaned = strip_tag(concept_content)
        all_concepts.append(cleaned)

    overview = "\n\n".join(all_concepts)

    name = Path(path).name
    last_dir = name[3:] if name.startswith("CSC") else name
    tag = f"#{last_dir}_{topic_number}"

    return overview + "\n" + tag, skipped

def run(path):
    rels = get_relationships(path)

    all_topic_overviews = []
    skipped_map = {}

    for topic, concepts in rels.items():
        overview, skipped = get_topic_overview_concepts_as_string(path, topic, concepts)
        all_topic_overviews.append(overview)

        if skipped:
            skipped_map[topic] = skipped

    for i, content in enumerate(all_topic_overviews, start=1):
        fname = f"Topic Overview {i}.md"
        full_path = join(path, fname)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    full_path = join(path, f"{Path(path).resolve().name}_module_summary.md")

    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_topic_overviews) + "\n")

    if skipped_map:
        skipped_output = ["\n\nSkipped Files:"]

        for topic, concepts in skipped_map.items():
            skipped_output.append(f"\t{topic}:")
            for concept in concepts:
                skipped_output.append(f"\t\tConcept: [[{concept}]]")

        print("\n".join(skipped_output))

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = Path.cwd()

    run(str(base_path))

if __name__ == "__main__":
    main()