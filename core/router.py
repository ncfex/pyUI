class Route:
    def __init__(self, path, element, children=None, loader=None, action=None):
        self.path = path
        self.element = element
        self.children = children or []
        self.loader = loader
        self.action = action

class Router:
    def __init__(self, connection, routes):
        self.connection = connection
        self.routes = {route.path: route for route in routes}

    def add_route(self, route: str, view_class):
        self.routes[route] = Route(route, view_class)
        print(f"{self.routes}")

    def get_view(self, path, sid, subpath=None):
        route = self.routes.get(path)
        if route:
            if subpath and route.children:
                subroute = next((child for child in route.children if child.path == subpath), None)
                if subroute:
                    return subroute.element(sid=sid, connection=self.connection)
            return route.element(sid=sid, connection=self.connection)
        return None

    def navigate_to(self, route: str, subroute: str=None, sid=None, elem_id=None):
        print(f"Checking {route} in {self.routes}")
        if sid is not None:
          if route in self.routes:
              view = self.get_view(route, subroute)
              print(f"find {route} in {self.routes} {view}")
              if self.connection:
                  self.connection.emit("from-server", {"event_name": "change-location", "id": f"{elem_id}", "value": f"{route}" }, sid)
        else:
            print(f"No ELEM ID PROVIDED")
            return -1