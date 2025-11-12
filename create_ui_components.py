"""
Download Premium UI Assets cho Game
Tai buttons, panels, sliders, checkboxes tu nguon free
"""

import os
import urllib.request
import sys
from PIL import Image, ImageDraw, ImageFont
import io

def create_button(width, height, color, text, filepath):
    """Tao button voi text"""
    try:
        # Tao image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve rounded rectangle
        draw.rounded_rectangle([(0, 0), (width, height)], radius=15, fill=color, outline=(255, 255, 255, 200), width=3)

        # Ve text (neu co)
        if text:
            try:
                # Thu dung font he thong
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()

            # Tinh vi tri text o giua
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2 - 5)

            # Ve text voi shadow
            draw.text((position[0] + 2, position[1] + 2), text, fill=(0, 0, 0, 150), font=font)
            draw.text(position, text, fill=(255, 255, 255, 255), font=font)

        # Luu file
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def create_panel(width, height, filepath):
    """Tao panel trong suot"""
    try:
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve panel voi gradient effect
        draw.rounded_rectangle([(0, 0), (width, height)], radius=20,
                              fill=(40, 40, 40, 220), outline=(100, 100, 100, 255), width=4)

        # Ve highlight
        draw.rounded_rectangle([(5, 5), (width-5, height//3)], radius=15,
                              fill=(255, 255, 255, 20))

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def create_slider(width, height, filepath):
    """Tao slider bar"""
    try:
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve slider track
        track_height = height // 3
        y_center = height // 2
        draw.rounded_rectangle([(0, y_center - track_height//2), (width, y_center + track_height//2)],
                              radius=track_height//2, fill=(80, 80, 80, 255))

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def create_slider_handle(size, filepath):
    """Tao slider handle (nut keo)"""
    try:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve circle voi gradient
        draw.ellipse([(2, 2), (size-2, size-2)], fill=(200, 200, 200, 255), outline=(255, 255, 255, 255), width=3)
        draw.ellipse([(size//4, size//4), (size*3//4, size*3//4)], fill=(255, 255, 255, 100))

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def create_checkbox(size, checked, filepath):
    """Tao checkbox"""
    try:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Ve box
        draw.rounded_rectangle([(0, 0), (size, size)], radius=5,
                              fill=(80, 80, 80, 255), outline=(200, 200, 200, 255), width=3)

        # Ve checkmark neu checked
        if checked:
            draw.line([(size*0.2, size*0.5), (size*0.4, size*0.7)], fill=(0, 255, 0, 255), width=5)
            draw.line([(size*0.4, size*0.7), (size*0.8, size*0.3)], fill=(0, 255, 0, 255), width=5)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def create_icon(size, icon_type, filepath):
    """Tao icon"""
    try:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if icon_type == "sound":
            # Ve speaker icon
            draw.polygon([(size*0.2, size*0.4), (size*0.4, size*0.4), (size*0.6, size*0.2),
                         (size*0.6, size*0.8), (size*0.4, size*0.6), (size*0.2, size*0.6)],
                        fill=(255, 255, 255, 255))
            # Ve sound waves
            for i in range(3):
                offset = size * (0.7 + i*0.1)
                draw.arc([(offset, size*0.3), (size*0.9, size*0.7)], 270, 90,
                        fill=(255, 255, 255, 255), width=3)

        elif icon_type == "music":
            # Ve music note
            draw.ellipse([(size*0.3, size*0.6), (size*0.5, size*0.8)], fill=(255, 255, 255, 255))
            draw.rectangle([(size*0.48, size*0.2), (size*0.55, size*0.7)], fill=(255, 255, 255, 255))
            draw.ellipse([(size*0.5, size*0.2), (size*0.7, size*0.4)], outline=(255, 255, 255, 255), width=3)

        elif icon_type == "settings":
            # Ve gear icon
            center = size // 2
            radius = size * 0.3
            for i in range(8):
                angle = i * 45
                import math
                x = center + radius * math.cos(math.radians(angle))
                y = center + radius * math.sin(math.radians(angle))
                draw.ellipse([(x-size*0.08, y-size*0.08), (x+size*0.08, y+size*0.08)],
                           fill=(255, 255, 255, 255))
            draw.ellipse([(center-radius*0.5, center-radius*0.5), (center+radius*0.5, center+radius*0.5)],
                        fill=(50, 50, 50, 255), outline=(255, 255, 255, 255), width=3)

        elif icon_type == "back":
            # Ve back arrow
            draw.polygon([(size*0.6, size*0.3), (size*0.3, size*0.5), (size*0.6, size*0.7)],
                        fill=(255, 255, 255, 255))
            draw.rectangle([(size*0.3, size*0.45), (size*0.7, size*0.55)], fill=(255, 255, 255, 255))

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)
        print(f"Tao thanh cong: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tao {os.path.basename(filepath)}: {e}")
        return False

def main():
    base_dir = "future_assets/ui"

    print("=" * 60)
    print("TAO CAC UI COMPONENTS")
    print("=" * 60)

    success_count = 0

    # Tao buttons
    print("\n1. Tao buttons:")
    buttons = [
        ("btn_large_play.png", 200, 60, (0, 180, 0, 255), "PLAY"),
        ("btn_large_settings.png", 200, 60, (0, 100, 200, 255), "SETTINGS"),
        ("btn_large_exit.png", 200, 60, (200, 0, 0, 255), "EXIT"),
        ("btn_medium_resume.png", 150, 50, (0, 150, 0, 255), "RESUME"),
        ("btn_medium_restart.png", 150, 50, (200, 100, 0, 255), "RESTART"),
        ("btn_medium_menu.png", 150, 50, (100, 100, 100, 255), "MENU"),
        ("btn_small_ok.png", 100, 40, (0, 200, 0, 255), "OK"),
        ("btn_small_cancel.png", 100, 40, (200, 0, 0, 255), "CANCEL"),
    ]

    for filename, width, height, color, text in buttons:
        if create_button(width, height, color, text, os.path.join(base_dir, filename)):
            success_count += 1

    # Tao panels
    print("\n2. Tao panels:")
    panels = [
        ("panel_large.png", 400, 500),
        ("panel_medium.png", 350, 300),
        ("panel_small.png", 250, 150),
    ]

    for filename, width, height in panels:
        if create_panel(width, height, os.path.join(base_dir, filename)):
            success_count += 1

    # Tao sliders
    print("\n3. Tao sliders:")
    if create_slider(200, 20, os.path.join(base_dir, "slider_track.png")):
        success_count += 1
    if create_slider_handle(30, os.path.join(base_dir, "slider_handle.png")):
        success_count += 1

    # Tao checkboxes
    print("\n4. Tao checkboxes:")
    if create_checkbox(40, False, os.path.join(base_dir, "checkbox_unchecked.png")):
        success_count += 1
    if create_checkbox(40, True, os.path.join(base_dir, "checkbox_checked.png")):
        success_count += 1

    # Tao icons
    print("\n5. Tao icons:")
    icons = [
        ("icon_sound.png", "sound"),
        ("icon_music.png", "music"),
        ("icon_settings.png", "settings"),
        ("icon_back.png", "back"),
    ]

    for filename, icon_type in icons:
        if create_icon(50, icon_type, os.path.join(base_dir, filename)):
            success_count += 1

    print("\n" + "=" * 60)
    print("KET QUA TAO UI COMPONENTS")
    print("=" * 60)
    print(f"Tao thanh cong: {success_count} components")
    print(f"\nTat ca UI assets da san sang trong: {base_dir}/")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except ImportError:
        print("\nLoi: Can cai dat Pillow (PIL)")
        print("Chay lenh: pip install Pillow")
        sys.exit(1)

