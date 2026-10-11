import math
import random

import pygame

from game.basket import Basket
from game.fruit import Fruit


class SplashParticle:
    """A small colored droplet used for catch and floor splash effects."""

    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.0, 4.0)
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 1.5
        self.color = color
        self.life = random.randint(18, 32)
        self.max_life = self.life
        self.radius = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18
        self.life -= 1

    def render(self, surface):
        if self.life <= 0:
            return
        radius = max(1, round(self.radius * self.life / self.max_life))
        pygame.draw.circle(surface, self.color, (round(self.x), round(self.y)), radius)


class GameEngine:
    STARTING_LIVES = 3
    STARTING_SPAWN_DELAY = 750
    MIN_SPAWN_DELAY = 260
    GROUND_HEIGHT = 25

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []
        self.particles = []

        self.score = 0
        self.lives = self.STARTING_LIVES
        self.spawn_delay = self.STARTING_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 20)

    def handle_event(self, event):
        if (self.game_state == "GAME_OVER" and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r):
            self.reset()

    def _lose_life(self):
        self.lives = max(0, self.lives - 1)
        if self.lives == 0:
            self.game_state = "GAME_OVER"

    def _make_splash(self, x, y, color, amount=12):
        self.particles.extend(
            SplashParticle(x, y, color) for _ in range(amount)
        )

    def _catch(self, fruit):
        if fruit.kind in Fruit.FRUIT_COLORS:
            self.score += 1
            self._make_splash(fruit.x, fruit.y, fruit.color, 12)
        elif fruit.kind == "rotten":
            self.score = max(0, self.score - 1)
            self._make_splash(fruit.x, fruit.y, fruit.color, 14)
        else:
            self._lose_life()
            self._make_splash(fruit.x, fruit.y, (255, 125, 45), 18)

    def _handle_miss(self, fruit, ground_y):
        self._make_splash(fruit.x, ground_y, fruit.color, 12)
        # Fruit missed at the floor costs a life. Hazards are harmful only
        # when caught, so they can safely be dodged.
        if fruit.kind in Fruit.FRUIT_COLORS:
            self._lose_life()

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        now = pygame.time.get_ticks()
        self.spawn_delay = max(
            self.MIN_SPAWN_DELAY,
            self.STARTING_SPAWN_DELAY - self.score * 12,
        )
        if now - self.last_spawn_time >= self.spawn_delay:
            baseline_speed = 4.0 + min(4.0, self.score * 0.08)
            self.fruits.append(Fruit(self.width, base_speed=baseline_speed))
            self.last_spawn_time = now

        ground_y = self.height - self.GROUND_HEIGHT
        basket_rect = self.basket.rect
        for fruit in self.fruits[:]:
            fruit.update()

            if basket_rect.colliderect(fruit.rect):
                self._catch(fruit)
                self.fruits.remove(fruit)
                if self.game_state == "GAME_OVER":
                    break
                continue

            if fruit.rect.bottom >= ground_y:
                self._handle_miss(fruit, ground_y)
                self.fruits.remove(fruit)
                if self.game_state == "GAME_OVER":
                    break

        if self.game_state == "GAME_OVER":
            # Freeze the game at the end of the run, including the effects.
            return

        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.particles.clear()
        self.score = 0
        self.lives = self.STARTING_LIVES
        self.spawn_delay = self.STARTING_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - self.GROUND_HEIGHT
        pygame.draw.rect(screen, (45, 50, 60),
                         (0, ground_y, self.width, self.GROUND_HEIGHT))

        for fruit in self.fruits:
            fruit.render(screen)
        for particle in self.particles:
            particle.render(screen)
        self.basket.render(screen)

        score_surf = self.font_medium.render(
            f"Score: {self.score}", True, (255, 220, 80)
        )
        screen.blit(score_surf, (25, 20))

        lives_surf = self.font_medium.render(
            f"Lives: {self.lives}", True, (240, 80, 80)
        )
        screen.blit(lives_surf,
                    (self.width - lives_surf.get_width() - 25, 20))

        guide = self.font_small.render(
            "A/D or arrows: move   Rotten: -1 point   Bomb: -1 life",
            True, (190, 195, 205)
        )
        screen.blit(guide, (self.width // 2 - guide.get_width() // 2,
                            self.height - 20))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("GAME OVER", True, (235, 70, 70))
            screen.blit(over_surf,
                        (self.width // 2 - over_surf.get_width() // 2,
                         self.height // 2 - 40))

            final_surf = self.font_medium.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )
            screen.blit(final_surf,
                        (self.width // 2 - final_surf.get_width() // 2,
                         self.height // 2 + 10))

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again", True, (200, 200, 200)
            )
            screen.blit(restart_surf,
                        (self.width // 2 - restart_surf.get_width() // 2,
                         self.height // 2 + 50))

