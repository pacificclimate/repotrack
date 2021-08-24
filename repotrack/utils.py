from os import write
import json
import sys


def get_contents(repo, path=""):
    """Return path contents as list"""
    try:
        contents = [content.path for content in repo.get_contents(path)]
    except Exception as e:
        # In case it doesn't exist, might add logging here later
        contents = []

    return contents


def check_topics(repo, target):
    """Generaric check for repo topics"""
    topics = repo.get_topics()

    if target in topics:
        return True

    else:
        return False


def unique_cols(data):
    """Create sorted list of unique DevOps tools used"""
    cols = set()
    for _, tools in data.items():
        for tool in tools:
            cols.add(tool)

    return sorted(cols)


def build_header(cols):
    """Build README table header"""
    header = "| Repo |"
    for col in cols:
        header += f" {col} |"

    header += "\n|:-:|" + ":-:|" * len(cols)
    return header + "\n"


def table_builder(devops_data, organization, no_empties):
    """Build a markdown table out of the collected data"""
    cols = unique_cols(devops_data)
    header = build_header(cols)

    def filtering(to_filter):
        filtered = {}
        for key, value in to_filter.items():
            if value:
                filtered[key] = value

        return filtered

    if no_empties:
        devops_data = filtering(devops_data)

    rows = ""
    for repo_name, tools in devops_data.items():
        row = f"| [{repo_name}](https://github.com/{organization}/{repo_name}) |"
        for col in cols:
            if col in tools:
                row += f" :heavy_check_mark: |"
            else:
                row += f" |"
        row += "\n"
        rows += row

    return header + rows


def eprint(string):
    """Write to stderr"""
    sys.stderr.write(f"{string}\n")