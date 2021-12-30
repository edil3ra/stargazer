import json

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
        res.text = json.dumps(r)



def build_app():
    app = falcon.App()
    things = StarNeighbours()
    app.add_route('/repos/{user}/starneighbours', things)
    return app
    
