class CollisionSystem():
    def circle_hit(self, a, b):
        return a.pos.distance_to(b.pos) <= a.radius + b.radius
    