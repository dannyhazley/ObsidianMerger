from os import listdir
from os.path import isfile, join
import re
from pathlib import Path

def get_concepts_per_topic(concept_block):
    return re.findall(r"\[\[(.*?)\]\]", concept_block)

def strip_tag(content):
    return re.sub(r"#\w+_\d+\s*$", "", content.strip())

def get_relationships(path):
    topics_path = join(path, "Topics")

    results = {}

    for file in listdir(topics_path):
        file_path = join(topics_path, file)

        if isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r"## Concepts([\s\S]*?)(?=^#)", content, re.M)

            if match:
                concepts = get_concepts_per_topic(match.group(1))
                results[file.strip(".md")] = concepts

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

    content = ""
    with open(concept_path, "r", encoding="utf-8") as f:
        content = f.read()

    return prepend_title(content, concept_name)

def prepend_title(content, title):
    return f"# {title}\n\n{content}"

def get_topic_overview_concepts_as_string(path, topic, topic_rels):
    match = re.search(r"Topic\s*(\d+)\s*-\s*(.*)", topic)
    topic_number = match.group(1) if match else "0"

    all_concepts = []

    topic_content = read_topic(path, topic)
    all_concepts.append(strip_tag(topic_content))

    for concept_title in topic_rels:
        concept_content = read_concept(path, concept_title)
        cleaned = strip_tag(concept_content)
        all_concepts.append(cleaned)

    overview =  "\n\n".join(all_concepts)
    last_dir = Path(PATH).name.strip("CSC")

    tag = f"#{last_dir}_{topic_number}"

    return overview + "\n" + tag

def run(path):
    rels = get_relationships(path)

    all_topic_overviews = []

    for topic, concepts in rels.items():
        all_topic_overviews.append(get_topic_overview_concepts_as_string(path, topic, concepts))

    for n in range(len(all_topic_overviews)):
        fname = f"Topic Overview {n+1}.md"
        full_path = join(path, fname)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(all_topic_overviews[n])

PATH = "/Users/dannyhazley/Library/Mobile Documents/iCloud~md~obsidian/Documents/BSC/CSC2063"

run(PATH)