import pygame
from game_utils import asset_path, load_sound

WIDTH, HEIGHT = 500, 600

class ShopScene:
    def __init__(self, screen, player_name, api=None, storage=None):
        self.screen = screen
        self.player_name = player_name
        self.api = api
        self.storage = storage
        
        # Load background with fallback if missing
        try:
            self.bg = pygame.image.load(asset_path('assets', 'background-day.png')).convert()
        except Exception:
            # Fallback to generic background image
            self.bg = pygame.image.load(asset_path('assets', 'background.png')).convert()
        # Ensure correct size
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        
        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Bird Previews with fallback if specific sprites are missing
        def _load_bird(img_name):
            try:
                return pygame.transform.scale(pygame.image.load(asset_path('assets', img_name)), (60, 45))
            except Exception:
                # Fallback to the default yellow bird sprite
                return pygame.transform.scale(pygame.image.load(asset_path('assets', 'bird-mid.png')), (60, 45))

        self.birds = {
            "yellow": _load_bird('bird-mid.png'),
            "blue": _load_bird('bluebird-midflap.png'),
            "red": _load_bird('redbird-midflap.png')
        }
        
        # Prices & Info
        self.items = [
            {"id": "yellow", "name": "Classic", "price": 0, "desc": "Balanced"},
            {"id": "blue", "name": "Azure", "price": 50, "desc": "Floaty (Easy)"},
            {"id": "red", "name": "Crimson", "price": 100, "desc": "Heavy (x2 Score)"}
        ]
        
        self.coin_img = pygame.transform.scale(pygame.image.load(asset_path('assets', 'coin.png')), (30, 30))
        
        # UI State
        self.selected_idx = 0
        
        # Sounds
        self.buy_sound = load_sound('assets/hit.wav')  # Use hit sound for purchase
        self.click_sound = load_sound('assets/flap.wav')

    async def run(self):
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            
            # Get current data
            coins = self.storage.get_coins()
            inventory = self.storage.get_inventory()
            current_skin = self.storage.get_current_skin()
            
            # Event Handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit", {}
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "menu", {"player": self.player_name}
                    
                    if e.key == pygame.K_LEFT:
                        self.selected_idx = (self.selected_idx - 1) % len(self.items)
                        if self.click_sound: self.click_sound.play()
                        
                    if e.key == pygame.K_RIGHT:
                        self.selected_idx = (self.selected_idx + 1) % len(self.items)
                        if self.click_sound: self.click_sound.play()
                        
                    if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                        item = self.items[self.selected_idx]
                        skin_id = item["id"]
                        
                        if skin_id in inventory:
                            # Select
                            self.storage.set_skin(skin_id)
                            if self.buy_sound: self.buy_sound.play()
                        else:
                            # Buy
                            if coins >= item["price"]:
                                self.storage.spend_coins(item["price"])
                                self.storage.unlock_skin(skin_id)
                                self.storage.set_skin(skin_id)
                                if self.buy_sound: self.buy_sound.play()
            
            # Drawing
            self.screen.blit(self.bg, (0, 0))
            
            # Title
            title = self.font_title.render("BIRD SHOP", True, (255, 255, 255))
            title_shadow = self.font_title.render("BIRD SHOP", True, (0, 0, 0))
            self.screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, 53))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            # Coins Display
            self.screen.blit(self.coin_img, (WIDTH - 100, 20))
            coin_text = self.font_text.render(f"{coins}", True, (255, 215, 0))
            self.screen.blit(coin_text, (WIDTH - 65, 25))
            
            # Items Carousel
            start_x = 70
            gap = 130
            
            for i, item in enumerate(self.items):
                x = start_x + i * gap
                y = 200
                
                # Highlight selection
                if i == self.selected_idx:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x - 10, y - 10, 100, 150), 3)
                
                # Bird Image
                bird_img = self.birds[item["id"]]
                self.screen.blit(bird_img, (x + 10, y + 10))
                
                # Name
                name_txt = self.font_small.render(item["name"], True, (255, 255, 255))
                self.screen.blit(name_txt, (x + 10, y + 70))
                
                # Price / Status
                if item["id"] in inventory:
                    if item["id"] == current_skin:
                        status_txt = self.font_small.render("EQUIPPED", True, (0, 255, 0))
                    else:
                        status_txt = self.font_small.render("OWNED", True, (200, 200, 200))
                    self.screen.blit(status_txt, (x + 10, y + 100))
                else:
                    price_txt = self.font_small.render(f"{item['price']} Coins", True, (255, 215, 0))
                    self.screen.blit(price_txt, (x + 10, y + 100))
            
            # Description Box
            sel_item = self.items[self.selected_idx]
            desc_bg = pygame.Surface((400, 100))
            desc_bg.set_alpha(128)
            desc_bg.fill((0, 0, 0))
            self.screen.blit(desc_bg, (50, 400))
            
            desc_title = self.font_text.render(f"Ability: {sel_item['desc']}", True, (255, 255, 255))
            self.screen.blit(desc_title, (70, 420))
            
            instr = self.font_small.render("[Arrows] Move   [Space] Buy/Select   [Esc] Back", True, (200, 200, 200))
            self.screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 550))
            
            pygame.display.update()
            await asyncio.sleep(0)
