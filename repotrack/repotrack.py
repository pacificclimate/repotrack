import click
from github import Github
import json

from checks import checklist
from utils import table_builder, table_to_file, load_from_file


def search_for_devops(gat, organization):
    """Create json file with DevOps tool usage details"""
    hub = Github(gat)

    def devops_checklist(repo):
        """Helper method to build list of devops tools used with help from `checklist`"""
        return [name for name, method in checklist.items() if method(repo)]

    devops_data = {
        repo.name: devops_checklist(repo)
        for repo in hub.get_user().get_repos()
        if repo.organization and repo.organization.login == organization
    }

    return devops_data


@click.command()
@click.option("--gat", "-g", help="Github access token")
@click.option(
    "--organization", "-o", default="pacificclimate", help="Target organization"
)
@click.option(
    "--savepath",
    "-s",
    default="",
    help="Filepath to json file where you wish to save collected data",
)
@click.option(
    "--loadpath",
    "-l",
    default="",
    help="Write DevOps table from stored data",
)
@click.option(
    "--no-empties",
    "-n",
    is_flag=True,
    default=False,
    help="Filter out repos that have no DevOps tools",
)
def main(gat, organization, savepath, loadpath, no_empties):
    """Run through process of collecting repo data and reporting it to a file"""
    print("Starting...")
    if loadpath:
        print("Loading from file")
        devops_data = load_from_file(loadpath)

    else:
        print("Searching with Github API")
        devops_data = search_for_devops(gat, organization)

    if savepath:
        print("Saving for later...")
        with open(savepath, "w") as f:
            json.dump(devops_data, f)

    print("Building table")
    table = table_builder(devops_data, organization, no_empties)

    print("Writing table")
    table_to_file(table)


if __name__ == "__main__":
    main()
