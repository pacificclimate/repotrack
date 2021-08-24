from utils import get_contents, check_topics


def actions(repo):
    """Check for actions"""
    if not get_contents(repo, ".github/workflows"):
        return False

    else:
        return True


def anchore(repo):
    """Check for anchore"""
    path = ".github/workflows"
    contents = get_contents(repo, path)

    if not contents:
        return False

    for workflow in [f"{path}/anchore-analysis.yml", f"{path}/image-scan.yml"]:
        if workflow in contents:
            return True

    return False


def daccs(repo):
    """Check for daccs"""
    return check_topics(repo, "daccs")


def docker(repo):
    """Check for docker"""
    root_contents = get_contents(repo)

    if "Dockerfile" in root_contents:
        return True

    docker_contents = get_contents(repo, "docker")

    if docker_contents:
        return True

    return False


def jenkins(repo):
    """Check for jenkins"""
    root_contents = get_contents(repo)

    if "Jenkinsfile" in root_contents:
        return True

    jenkins_contents = get_contents(repo, "jenkins")

    if jenkins_contents:
        return True

    return False


def make(repo):
    """Check for make"""
    if "Makefile" in get_contents(repo):
        return True

    else:
        return False


def pip(repo):
    """Check for pip"""
    root_contents = get_contents(repo)

    for req_file in [
        "requirements.txt",
        "test_requirements.txt",
        "dev_requirements.txt",
        "deploy_requirements.txt",
    ]:
        if req_file in root_contents:
            return True

    return False


def pipenv(repo):
    """Check for pipenv"""
    root_contents = get_contents(repo)

    for req_file in ["Pipfile", "Pipfile.lock"]:
        if req_file in root_contents:
            return True

    return False


def snyk(repo):
    """Check for snyk"""
    return check_topics(repo, "snyk")


checklist = {
    "actions": actions,
    "anchore": anchore,
    "daccs": daccs,
    "docker": docker,
    "jenkins": jenkins,
    "make": make,
    "pip": pip,
    "pipenv": pipenv,
    "snyk": snyk,
}
