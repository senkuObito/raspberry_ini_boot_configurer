from PIL import Image, ImageDraw
import math

def create_icon(path):
    # Create a 256x256 image with alpha channel
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # --- Draw Raspberry ---
    raspberry_color = "#C51A4A" # Raspberry Red
    
    # Draw berries (clusters of circles)
    # Row 1 (Top)
    draw.ellipse((60, 60, 110, 110), fill=raspberry_color)
    draw.ellipse((105, 60, 155, 110), fill=raspberry_color)
    draw.ellipse((150, 60, 200, 110), fill=raspberry_color)
    
    # Row 2
    draw.ellipse((40, 100, 90, 150), fill=raspberry_color)
    draw.ellipse((85, 100, 135, 150), fill=raspberry_color)
    draw.ellipse((130, 100, 180, 150), fill=raspberry_color)
    draw.ellipse((175, 100, 225, 150), fill=raspberry_color)

    # Row 3
    draw.ellipse((60, 140, 110, 190), fill=raspberry_color)
    draw.ellipse((105, 140, 155, 190), fill=raspberry_color)
    draw.ellipse((150, 140, 200, 190), fill=raspberry_color)

    # Row 4 (Bottom)
    draw.ellipse((105, 180, 155, 230), fill=raspberry_color)

    # Leaves (Green)
    leaf_color = "#6CC04A"
    draw.ellipse((60, 10, 120, 80), fill=leaf_color) # Left
    draw.ellipse((140, 10, 200, 80), fill=leaf_color) # Right
    draw.polygon([(130, 10), (100, 60), (160, 60)], fill=leaf_color) # Center

    # --- Draw Gear (White Overlay at Bottom Right) ---
    gear_center = (190, 190)
    gear_radius = 55
    gear_color = "#FFFFFF"
    
    # Draw central disk
    draw.ellipse((gear_center[0] - gear_radius, gear_center[1] - gear_radius, 
                  gear_center[0] + gear_radius, gear_center[1] + gear_radius), fill=gear_color)

    # Draw teeth
    num_teeth = 8
    tooth_len = 15
    tooth_width = 12 # Half width
    
    for i in range(num_teeth):
        angle = (360 / num_teeth) * i
        rad = math.radians(angle)
        
        # Center of tooth edge
        cx = gear_center[0] + math.cos(rad) * (gear_radius + tooth_len/2)
        cy = gear_center[1] + math.sin(rad) * (gear_radius + tooth_len/2)
        
        # Draw tooth as a circle or square
        draw.rectangle([cx - tooth_width, cy - tooth_width, cx + tooth_width, cy + tooth_width], fill=gear_color)

    # Inner hole
    hole_radius = 20
    hole_color = "#2B2B2B"  # Dark gray (matches standard dark theme bg approx)
    draw.ellipse((gear_center[0] - hole_radius, gear_center[1] - hole_radius, 
                  gear_center[0] + hole_radius, gear_center[1] + hole_radius), fill=hole_color)

    # Save as ICO
    img.save(path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

if __name__ == "__main__":
    create_icon("assets/icon.ico")
    print("Icon created at assets/icon.ico")
