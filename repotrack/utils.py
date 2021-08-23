def get_contents(repo, path=""):
    try:
        contents = [content.path for content in repo.get_contents(path)]
    except Exception as e:
        # In case it doesn't exist, might add logging here later
        contents = []

    return contents


def check_topics(repo, target):
    topics = repo.get_topics()

    if target in topics:
        return True

    else:
        return False
