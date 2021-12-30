from serde.json import to_json

import falcon

import models
from stargazer_github import StargazerGithub

class StarNeighboursResource:
    def __init__(self, stagazer_github: StargazerGithub):
        self.stagazer_github = stagazer_github
        
    def on_get(self, req: falcon.Request, res: falcon.Response):
        stargazers = self.stagazer_github.get_repos_with_common_stargazers()
        res.text = to_json(stargazers)

class AuthMiddleware:
    def __init__(self, stagazer_github: StargazerGithub):
        self.stagazer_github = stagazer_github
        
    def process_request(self, req: falcon.Request, res: falcon.Response):
        token = req.get_header('Authorization')
        if token is None:
            description = ('Please provide your github token '
                           'as part of the request '
                           'ex: Authorization:{your_github_token}')

            raise falcon.HTTPUnauthorized(title='Auth token required', description=description)

        self.stagazer_github.connect(token)
        if not self.stagazer_github.is_authenticated():
            description = ('The provided auth token is not valid. ')
            raise falcon.HTTPUnauthorized(title='Authentication required', description=description)


def build_app():
    stagazer_github = StargazerGithub()
    app = falcon.App(middleware=[AuthMiddleware(stagazer_github)])
    stars = StarNeighboursResource(stagazer_github)
    # I am not fully sure to undestand the endpoint, the {user} was redudant because the token already authenticate the user
    # as only the connected user can see this endpoint I removed the {user}
    # previous:  app.add_route('/repos/{user}/starneighbours', stars)
    app.add_route('/repos/starneighbours', stars)
    return app
    
