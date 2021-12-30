from serde.json import to_json

import falcon

import models

class StarNeighbours:
    def on_get(self, req: falcon.Request, res: falcon.Response, user):
        """Handles GET requests"""
        res.status = falcon.HTTP_200
        u1 = models.Stargazer('vince', 1)
        u2 = models.Stargazer('pierre', 2)
        u3 = models.Stargazer('john', 1)
        r = models.RepoStargazer('my-repo', [u1, u2, u3])

        print('user: {}'.format(user))
        res.text = to_json(r)


class AuthMiddleware:
    def process_request(self, req, resp):
        token = req.get_header('Authorization')

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized(title='Auth token required', description=description)

        if not self._token_is_valid(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized(title='Authentication required', description=description)

    def _token_is_valid(self, token):
        return token == 'token'


def build_app():
    # app = falcon.App(middleware=[AuthMiddleware()])
    app = falcon.App()
    stars = StarNeighbours()
    app.add_route('/repos/{user}/starneighbours', stars)
    return app
    
