import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the ship image and scale it
        image_path = r'C:\Users\Dell\Downloads\rocket.bmp'
        image = pygame.image.load(image_path)
        new_width = 100
        new_height = 100
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        
        # Ship speed
        self.speed = 1.5  # Adjust the speed as necessary

    def update(self):
        # Update the ship's position based on movement flags
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed

    def blitme(self):
        # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
    	self.rect.midbottom=self.screen_rect.midbottom
    	self.x=float(self.rect.x)
