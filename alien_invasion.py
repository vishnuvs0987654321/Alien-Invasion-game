import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import Gamestats
class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bullets = pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        self.stats=Gamestats(self)
        self.ship = Ship(self)
    def _ship_hit(self):
    	if self.stats.ships_left>0:
    		self.stats.ships_left-=1
    		self.aliens.empty()
    		self.bullets.empty()
    		self._create_fleet()
    		self.ship.center_ship()
    		sleep(0.5)
    	else:
    		self.stats.game_active=False

    def _create_fleet(self):
    	alien=Alien(self)
    	alien_width=alien.rect.width
    	available_space_x=self.settings.screen_width-(2*alien_width)
    	number_aliens_x=available_space_x//(2*alien_width)
    	for alien_number in range(number_aliens_x):
    		    	alien=Alien(self)
    		    	alien.x=alien_width+2*alien_width*alien_number
    		    	alien.rect.x=alien.x
    		    	self.aliens.add(alien)
    def _check_fleet_edges(self):
    	for alien in self.aliens.sprites():
    		if alien.check_edges():
    			self._change_fleet_direction()
    			break
    def _change_fleet_direction(self):
    	for alien in self.aliens.sprites():
    		alien.rect.y+=self.settings.fleet_drop_speed
    	self.settings.fleet_direction*=-1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
    	if len(self.bullets)<self.settings.bullets_allowed:
    		new_bullet = Bullet(self)
    		self.bullets.add(new_bullet)
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()
    def _update_bullets(self):
    	self._check_bullet_alien_collision()
    	self.bullets.update()
    	for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        

    def _check_bullet_alien_collision(self):
    	collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
    	if not self.aliens:
    		self.bullets.empty()
    		self._create_fleet()
        
    def _update_aliens(self):
    	self._check_fleet_edges()
    	self.aliens.update()
    	if pygame.sprite.spritecollideany(self.ship,self.aliens):
    		self._ship_hit()
    	self._check_aliens_bottom()	
    def _check_aliens_bottom(self):
    	screen_rect=self.screen.get_rect()
    	for alien in self.aliens.sprites():
    		if alien.rect.bottom >=screen_rect.bottom:
    			self._ship_hit()
    			break



    def run_game(self):
        while True:
            self.check_events()
            if self.stats.game_active:
            	self.ship.update()
            	self._update_bullets()
            	self._update_aliens()            
            
            self._update_screen()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
