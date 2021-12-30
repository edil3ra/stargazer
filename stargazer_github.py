from typing import List, Dict
import itertools
from collections import Counter
from dataclasses import dataclass
import typing

from github import Github
from github.Repository import Repository
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList


from serde import serialize, deserialize
from serde.json import from_json, to_json


@deserialize
@serialize
@dataclass
class Stargazer:
    name: str
    count: int


@deserialize
@serialize
@dataclass
class RepoStargazer:
    repo: str
    stargazers: List[Stargazer]


@dataclass
class StargazerGithub:
    _repos: List[Repository] 
    _repo_to_stargazers: Dict[str, List[str]]
    _common_stargazers: set
    _common_stargazers_counted: Dict[str, int]
    _repos_stargazers_by_user: Dict[str, List[RepoStargazer]] # very simple caching system, in a real project I would used something more powerfull and decoupled it from the class
    
    def __init__(self, github: Github):
        self.client: Github = github
        self._repos_stargazers_by_user = {}

    def get_repos_with_common_stargazers(self, user: str):
        if not user in self._repos_stargazers_by_user:
            self._build(user)
        return self._repos_stargazers_by_user[user]
        
    def _get_startgazers_from_repo(self, repo: Repository) -> List[str]:
        return list([user.login for user in repo.get_stargazers()])

    def _build(self, user: str):
        self._build_repos_from_user(user)\
            ._build_repos_user_dicts()\
            ._build_duplicated_users()\
            ._build_repos_stargazers(user)
    
    def _build_repos_from_user(self, user: str):
        self._repos = list(self.client.get_user(user).get_repos())
        return self
    
    def _build_repos_user_dicts(self):
        self._repo_to_stargazers = {repo.name: self._get_startgazers_from_repo(repo) for repo in self._repos}
        return self

    def _build_duplicated_users(self):
        raw_counted_users = Counter([value for values in self._repo_to_stargazers.values() for value in values])
        self._common_stargazers_counted = {key: value for key, value in raw_counted_users.items() if value > 1}
        self._common_stargazers = set(self._common_stargazers_counted.keys())
        return self

    def _build_repos_stargazers(self, user: str):
        self._repos_stargazers_by_user[user] = []
        for repo in self._repos:
            stargazers = self._repo_to_stargazers[repo.name]
            common_stargazers: List[Stargazer] = []
            for stargazer in stargazers:
                if stargazer in self._common_stargazers:
                    count = self._common_stargazers_counted[stargazer] - 1
                    common_stargazer = Stargazer(stargazer, count)
                    common_stargazers.append(common_stargazer)
            repo_stargazer = RepoStargazer(repo.name, common_stargazers)
            self._repos_stargazers_by_user[user].append(repo_stargazer)
