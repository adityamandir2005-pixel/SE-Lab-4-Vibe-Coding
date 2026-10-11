import random

import pygame


class Fruit:
    """A falling fruit or catchable hazard."""

    FRUIT_COLORS = {
        "apple": (225, 55, 60),
        "orange": (245, 145, 35),
        "grapes": (155, 80, 205),
    }

    def __init__(self, screen_width, base_speed=4.0):
        self.screen_width = screen_width
        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2
        self.kind = random.choices(
            ["apple", "orange", "grapes", "rotten", "bomb"],
            weights=[28, 28, 28, 8, 8],
            k=1,
        )[0]
        self.speed = random.uniform(base_speed, base_speed + 2.5)
        self.color = self._color_for_kind()

    def _color_for_kind(self):
        if self.kind in self.FRUIT_COLORS:
            return self.FRUIT_COLORS[self.kind]
        if self.kind == "rotten":
            return (105, 125, 55)
        return (45, 48, 55)

    def update(self):
        self.y += self.speed

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(surface, self.color, center, self.radius)

        if self.kind == "bomb":
            pygame.draw.circle(surface, (20, 22, 27), center, self.radius - 3)
            pygame.draw.line(surface, (225, 175, 70), (center[0] + 6, center[1] - 9),
                             (center[0] + 11, center[1] - 15), 3)
            pygame.draw.circle(surface, (255, 100, 35), (center[0] + 12, center[1] - 16), 3)
            pygame.draw.circle(surface, (255, 210, 90), (center[0] - 5, center[1] - 4), 2)
        elif self.kind == "rotten":
            pygame.draw.circle(surface, (65, 75, 38), (center[0] - 4, center[1] + 3), 3)
            pygame.draw.circle(surface, (65, 75, 38), (center[0] + 5, center[1] - 3), 2)
            pygame.draw.line(surface, (75, 55, 35), (center[0], center[1] - 12),
                             (center[0] + 2, center[1] - 17), 3)
        else:
            pygame.draw.circle(surface, (255, 255, 255),
                               (int(self.x - 4), int(self.y - 4)), 3)
            pygame.draw.line(surface, (75, 125, 55), (center[0], center[1] - 12),
                             (center[0] + 2, center[1] - 17), 3)

