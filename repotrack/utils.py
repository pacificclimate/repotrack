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
    for datum in data:
        for tool in datum["tools"]:
            cols.add(tool)

    return sorted(cols)


def build_header(cols):
    """Build README table header"""
    header = "| Repo | Last Updated |"
    for col in cols:
        header += f" {col} |"

    header += "\n|:-:|:-:|" + ":-:|" * len(cols)
    return header + "\n"


def recent_commit_date(repo):
    """Return the date of the most recent commit or None"""
    try:
        latest, *_ = repo.get_commits()

    except:
        return None

    return latest.commit.committer.date


def sort_by_date(devops_data):
    """Sort list by datetime object"""
    return sorted(devops_data, key=lambda key: key["date"], reverse=True)


def table_builder(devops_data, organization, no_empties, ordered):
    """Build a markdown table out of the collected data"""
    cols = unique_cols(devops_data)
    header = build_header(cols)

    def filtering(to_filter):
        filtered = []
        for to_f in to_filter:
            if to_f["tools"]:
                filtered.append(to_f)

        return filtered

    if no_empties:
        devops_data = filtering(devops_data)

    if ordered:
        devops_data = sort_by_date(devops_data)

    rows = ""
    for devops_datum in devops_data:
        row = f'| [{devops_datum["name"]}](https://github.com/{organization}/{devops_datum["name"]}) |'
        row += f' {devops_datum["date"]} |'

        for col in cols:
            if col in devops_datum["tools"]:
                row += f" :heavy_check_mark: |"
            else:
                row += f" |"
        row += "\n"
        rows += row

    return header + rows


def eprint(string):
    """Write to stderr"""
    sys.stderr.write(f"{string}\n")
