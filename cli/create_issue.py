# create issue.py

import click
import requests
from decouple import config

"""
https://github.com/en/rest/reference/issues#create-an-issue

python cli/create_issue.py \
--title='' \
--body='' \
--labels='feature'
"""

# O repositorio para adicionar issue
REPO_OWNER = config("REPO_OWNER")
REPO_NAME = config("REPO_NAME")
TOKEN = config("TOKEN")


def write_file(filename, number, title, description, labels):
    labels = " ,".join(labels).strip()
    with open(filename, "a") as f:
        f.write(f"\n---\n\n")
        f.write(f"[ ] {number} - {title}\n")
        f.write(f"    {labels}\n\n")

        if description:
            f.write(f"    {description}\n\n")

        f.write(
            f"    make lint; git add .; git commit -m '{title} close #{number}'; git push"
        )  # noqa E501


@click.command()
@click.option("--title", prompt="Title", help="Digite o Título.")
@click.option("--body", prompt="Description", help="Digite a Descrição.")
# @click.option('--assignee', prompt='assignee', help='Digite o nome da pessoa a ser associada.')
@click.option("--labels", prompt="Labels", help="Digite as Labels.")
def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    """
    Cria issue no github
    """

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {TOKEN}"}

    labels = labels.split(",")

    # cria issue

    issue = {"title": title, "body": body, "labels": labels}
    if assignee:
        issue["assignees"] = [assignee]

    # adiciona a issue no repositório
    req = requests.post(url, headers=headers, json=issue)

    if req.status_code == 201:
        print(f'Successfully created Issue "{title}".')
        number = req.json()["number"]
        description = body

        filename = "/home/luiz.cruz/tarefas.txt"
        write_file(filename, number, title, description, labels)

    else:
        print(f'Could not create Issue "{title}"')


if __name__ == "__main__":
    make_github_issue()
