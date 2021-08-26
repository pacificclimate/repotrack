import click
from github import Github
import json

from checks import checklist
from utils import table_builder, recent_commit_date, eprint


def search_for_devops(gat, organization):
    """Create json file with DevOps tool usage details"""
    hub = Github(gat)

    def devops_checklist(repo):
        """Helper method to build list of devops tools used with help from `checklist`"""
        return [name for name, method in checklist.items() if method(repo)]

    return [
        {"name": repo.name, "date": recent_commit_date(repo), "tools": devops_checklist(repo)}
        for repo in hub.get_user().get_repos()
        if repo.organization and repo.organization.login == organization
    ]


@click.command()
@click.option("--gat", "-g", help="Github access token")
@click.option(
    "--organization", "-o", default="pacificclimate", help="Target organization"
)
@click.option(
    "--no-empties",
    "-n",
    is_flag=True,
    default=False,
    help="Filter out repos that have no DevOps tools",
)
@click.option(
    "--ordered",
    "-r",
    is_flag=True,
    default=False,
    help="Order output by most recently updated",
)
def main(gat, organization, no_empties, ordered):
    """Run through process of collecting repo data and reporting it to stdout

    The result of this script is written to stdout and can be piped into a file using `tee`. 
    The "logging" messages are written to stderr and will not be recorded in the file.
    
    Example:
        pipenv run python repotrack/repotrack.py --gat $GITHUB_GAT --no-empties | tee README.md
    """
    eprint("Starting...")
    devops_data = search_for_devops(gat, organization)

    eprint("Building table")
    table = table_builder(devops_data, organization, no_empties, ordered)

    eprint("Finished...")
    print(table)


if __name__ == "__main__":
    main()
    
