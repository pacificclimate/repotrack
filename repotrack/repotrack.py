from checks import checklist
from github import Github
import json
import click


def writer(results):
    with open("repotrack/data.json", "w") as f:
        json.dump(results, f)


def content_search(hub, filter):
    results = {}
    for repo in hub.get_user().get_repos():
        if repo.organization and repo.organization.login == "pacificclimate":
            results[repo.name] = []
            for name, method in checklist.items():
                if method(repo):
                    results[repo.name] += [name]

    def filtering(to_filter):
        filtered = {}
        for key, value in to_filter.items():
            if value:
                filtered[key] = value
        
        return filtered
    
    if filter:
        writer(filtering(results))
    else:
        writer(results)


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

def table_builder():
    with open("repotrack/data.json", "r") as f:
        data = json.loads(f.read())
    
    cols = unique_cols(data)
    header = build_header(cols)
    
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


@click.command()
@click.option("--pat", "-p", help="Github access token")
@click.option("--filter", "-f", is_flag=True, default=True, help="Filter out repos that have no checkboxes")
def main(pat, filter):
    content_search(Github(pat), filter)
    
    table = table_builder() 
    
    with open("README.md", "w") as f:
        f.write(table)


if __name__ == "__main__":
    main()
    