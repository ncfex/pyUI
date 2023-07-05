# core/router.py

class Router:
    def __init__(self, connection):
        self.routes = {}
        self.connection = connection

    def add_route(self, route: str, component_class):
        self.routes[route] = component_class

    def get_component(self, route):
        if route in self.routes:
            return self.routes[route](self.connection)
        return None
            
    def navigate_to(self, route: str):
        print(f"Checking {route} in {self.routes}")
        if route in self.routes:
            component = self.routes[route]
            print(f"find {route} in {self.routes} {component}")
            if self.connection:
                self.connection.send(route, route, "navigate_to")