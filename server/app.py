import json

import falcon


class StarNeighbours:
    def on_get(self, req: falcon.Request, res: falcon.Response):
        """Handles GET requests"""
        res.status = falcon.HTTP_200
        d = [{
            "repo": '<repoA>',
            "stargazers": '[<stargazers in common>, ...]',
        }, {
            "repo": '<repo>',
            "stargazers": '[<stargazers in common>, ...]',
        }]
        res.text = json.dumps(d)



def build_app():
    app = falcon.App()
    things = StarNeighbours()
    app.add_route('/things', things)
    return app
    
