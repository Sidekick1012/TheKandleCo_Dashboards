from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def main():
    try:
        input_path = "assets/logo.png"
        output_path = "assets/logo_cropped.png"
        
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        # Trim white borders
        cropped_img = trim(img)
        
        # Save as the new logo
        cropped_img.save(output_path)
        # Also overwrite the original for the app
        cropped_img.save("assets/logo.png")
        
        print(f"Successfully cropped logo and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
