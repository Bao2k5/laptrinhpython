"""
Tao cac UI Button dep va ro rang cho Flappy Bird
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_beautiful_button(width, height, text, color_bg, color_text, filepath):
    """Tao button dep voi gradient va shadow"""
    try:
        # Tao image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve shadow
        shadow_offset = 4
        draw.rounded_rectangle(
            [(shadow_offset, shadow_offset), (width, height)],
            radius=15,
            fill=(0, 0, 0, 100)
        )

        # Ve button background
        draw.rounded_rectangle(
            [(0, 0), (width - shadow_offset, height - shadow_offset)],
            radius=15,
            fill=color_bg,
            outline=(255, 255, 255, 200),
            width=4
        )

        # Ve highlight (phan sang ben tren)
        draw.rounded_rectangle(
            [(5, 5), (width - shadow_offset - 5, (height - shadow_offset)//3)],
            radius=10,
            fill=(255, 255, 255, 60)
        )

        # Ve text
        try:
            # Thu cac font
            fonts_to_try = [
                "C:\\Windows\\Fonts\\arial.ttf",
                "C:\\Windows\\Fonts\\verdana.ttf",
                "arial.ttf",
                "verdana.ttf"
            ]
            font = None
            for font_path in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_path, int(height * 0.4))
                    break
                except:
                    continue

            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Tinh vi tri text o giua
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - shadow_offset - text_width) // 2
        y = (height - shadow_offset - text_height) // 2 - 5

        # Ve text shadow
        draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 150), font=font)

        # Ve text chinh
        draw.text((x, y), text, fill=color_text, font=font)

        # Luu file
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"✓ Tao: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"✗ Loi: {os.path.basename(filepath)} - {e}")
        return False

def create_icon_button(size, icon_type, color_bg, filepath):
    """Tao button icon (play, pause, settings, etc)"""
    try:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve shadow
        shadow_offset = 3
        draw.ellipse([(shadow_offset, shadow_offset), (size, size)], fill=(0, 0, 0, 100))

        # Ve button background
        draw.ellipse([(0, 0), (size - shadow_offset, size - shadow_offset)],
                    fill=color_bg, outline=(255, 255, 255, 200), width=3)

        # Ve icon
        center = (size - shadow_offset) // 2
        icon_color = (255, 255, 255, 255)

        if icon_type == "play":
            # Triangle play icon
            points = [
                (center - size*0.15, center - size*0.2),
                (center + size*0.2, center),
                (center - size*0.15, center + size*0.2)
            ]
            draw.polygon(points, fill=icon_color)

        elif icon_type == "pause":
            # Two bars
            bar_width = size * 0.1
            bar_height = size * 0.3
            draw.rectangle([
                (center - bar_width*1.5, center - bar_height//2),
                (center - bar_width*0.5, center + bar_height//2)
            ], fill=icon_color)
            draw.rectangle([
                (center + bar_width*0.5, center - bar_height//2),
                (center + bar_width*1.5, center + bar_height//2)
            ], fill=icon_color)

        elif icon_type == "restart":
            # Circular arrow
            import math
            for angle in range(0, 270, 10):
                rad1 = math.radians(angle)
                rad2 = math.radians(angle + 10)
                x1 = center + (size * 0.2) * math.cos(rad1)
                y1 = center + (size * 0.2) * math.sin(rad1)
                x2 = center + (size * 0.2) * math.cos(rad2)
                y2 = center + (size * 0.2) * math.sin(rad2)
                draw.line([(x1, y1), (x2, y2)], fill=icon_color, width=4)
            # Arrow head
            draw.polygon([
                (center + size*0.2, center - size*0.15),
                (center + size*0.2, center - size*0.05),
                (center + size*0.3, center - size*0.1)
            ], fill=icon_color)

        elif icon_type == "home":
            # House icon
            # Roof
            draw.polygon([
                (center - size*0.2, center),
                (center, center - size*0.2),
                (center + size*0.2, center)
            ], fill=icon_color)
            # House body
            draw.rectangle([
                (center - size*0.15, center),
                (center + size*0.15, center + size*0.2)
            ], fill=icon_color)

        elif icon_type == "settings":
            # Gear icon
            import math
            radius_outer = size * 0.2
            radius_inner = size * 0.12
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                x = center + radius_outer * math.cos(rad)
                y = center + radius_outer * math.sin(rad)
                draw.ellipse([
                    (x - size*0.04, y - size*0.04),
                    (x + size*0.04, y + size*0.04)
                ], fill=icon_color)
            # Center circle
            draw.ellipse([
                (center - radius_inner, center - radius_inner),
                (center + radius_inner, center + radius_inner)
            ], fill=color_bg, outline=icon_color, width=3)

        elif icon_type == "close":
            # X icon
            offset = size * 0.15
            draw.line([
                (center - offset, center - offset),
                (center + offset, center + offset)
            ], fill=icon_color, width=5)
            draw.line([
                (center - offset, center + offset),
                (center + offset, center - offset)
            ], fill=icon_color, width=5)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"✓ Tao: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"✗ Loi: {os.path.basename(filepath)} - {e}")
        return False

def main():
    base_dir = "future_assets/ui"

    print("=" * 60)
    print("TAO UI BUTTONS DEP CHO FLAPPY BIRD")
    print("=" * 60)

    # Mau sac
    GREEN = (34, 177, 76, 255)
    BLUE = (0, 122, 204, 255)
    RED = (231, 76, 60, 255)
    ORANGE = (230, 126, 34, 255)
    PURPLE = (142, 68, 173, 255)
    GRAY = (127, 140, 141, 255)
    WHITE = (255, 255, 255, 255)

    success = 0

    print("\n1. Text Buttons:")
    # Large buttons (cho main menu)
    buttons_large = [
        ("btn_play_large.png", 220, 70, "PLAY", GREEN),
        ("btn_settings_large.png", 220, 70, "SETTINGS", BLUE),
        ("btn_help_large.png", 220, 70, "HELP", PURPLE),
        ("btn_exit_large.png", 220, 70, "EXIT", RED),
    ]

    for filename, width, height, text, color in buttons_large:
        if create_beautiful_button(width, height, text, color, WHITE,
                                  os.path.join(base_dir, filename)):
            success += 1

    # Medium buttons (cho pause menu)
    buttons_medium = [
        ("btn_resume_medium.png", 180, 60, "RESUME", GREEN),
        ("btn_restart_medium.png", 180, 60, "RESTART", ORANGE),
        ("btn_menu_medium.png", 180, 60, "MENU", GRAY),
    ]

    for filename, width, height, text, color in buttons_medium:
        if create_beautiful_button(width, height, text, color, WHITE,
                                  os.path.join(base_dir, filename)):
            success += 1

    # Small buttons
    buttons_small = [
        ("btn_ok_small.png", 120, 50, "OK", GREEN),
        ("btn_cancel_small.png", 120, 50, "CANCEL", RED),
        ("btn_save_small.png", 120, 50, "SAVE", BLUE),
        ("btn_back_small.png", 120, 50, "BACK", GRAY),
    ]

    for filename, width, height, text, color in buttons_small:
        if create_beautiful_button(width, height, text, color, WHITE,
                                  os.path.join(base_dir, filename)):
            success += 1

    print("\n2. Icon Buttons:")
    # Icon buttons (tron)
    icon_buttons = [
        ("btn_play_icon.png", 80, "play", GREEN),
        ("btn_pause_icon.png", 80, "pause", BLUE),
        ("btn_restart_icon.png", 80, "restart", ORANGE),
        ("btn_home_icon.png", 80, "home", GRAY),
        ("btn_settings_icon.png", 80, "settings", PURPLE),
        ("btn_close_icon.png", 60, "close", RED),
    ]

    for filename, size, icon_type, color in icon_buttons:
        if create_icon_button(size, icon_type, color,
                             os.path.join(base_dir, filename)):
            success += 1

    print("\n" + "=" * 60)
    print(f"HOAN THANH: Tao thanh cong {success} buttons")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nLoi: {e}")
        print("Kiem tra da cai Pillow: pip install Pillow")
