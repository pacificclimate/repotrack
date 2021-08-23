from os import write
from checks import checklist
from github import Github
import json
import click


def content_search(hub):
    results = {}
    for repo in hub.get_user().get_repos():
        if repo.organization and repo.organization.login == "pacificclimate":
            results[repo.name] = []
            for name, method in checklist.items():
                if method(repo):
                    results[repo.name] += [name]

    with open("repotrack/data.json", "w") as f:
        json.dump(results, f)


def unique_cols(data):
    cols = set()
    for _, items in data.items():
        for tool in items:
            cols.add(tool)
    
    return sorted(cols)


def build_header(cols):
    header = "| Repo |"
    for col in cols:
        header += f" {col} |"
    
    header += "\n|:-:|" + ":-:|" * len(cols)
    return header + "\n"


def table_builder(filter):
    with open("repotrack/data.json", "r") as f:
        data = json.loads(f.read())
    
    cols = unique_cols(data)
    header = build_header(cols)

        
    def filtering(to_filter):
        filtered = {}
        for key, value in to_filter.items():
            if value:
                filtered[key] = value
        
        return filtered
    
    if filter:
        data = filtering(data)
    
    rows = ""
    for repo_name, tools in data.items():
        row = f"| [{repo_name}](https://github.com/pacificclimate/{repo_name}) |"
        for col in cols:
            if col in tools:
                row += f" **X** |"
            else:
                row += f" |"
        row += "\n"
        rows += row
    
    return header + rows


def write_readme(table):
    # Clear old data before rewriting
    open("README.md", "w").close()

    with open("README.md", "w") as f:
        f.write(table)


@click.command()
@click.option("--pat", "-p", help="Github access token")
@click.option("--filter", "-f", is_flag=True, default=False, help="Filter out repos that have no checkboxes")
@click.option("--write-from-data", "-d", is_flag=True, default=False, help="Write README.md table from stored data")
def main(pat, filter, write_from_data):
    if not write_from_data:
        content_search(Github(pat))

    table = table_builder(filter) 
    write_readme(table)


if __name__ == "__main__":
    main()
    