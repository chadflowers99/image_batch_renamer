import os
from PIL import Image

class ImageResizer:
    """
    Diagnostic Architect Tool: Slashing variable API fees by 
    normalizing image resolution to the 'Gemini Sweet Spot'.
    """
    def __init__(self, target_width=1024, quality=85):
        self.target_width = target_width
        self.quality = quality

    def optimize_for_api(self, image_path, output_folder="optimized_inventory"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with Image.open(image_path) as img:
            # Maintain aspect ratio while hitting the target width
            w_percent = (self.target_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            
            # Use LANCZOS for high-quality downsampling (audit-safe)
            img = img.resize((self.target_width, h_size), Image.Resampling.LANCZOS)
            
            base_name = os.path.basename(image_path)
            output_path = os.path.join(output_folder, base_name)
            
            # Save as optimized JPEG to minimize payload size
            img.convert('RGB').save(output_path, "JPEG", quality=self.quality)
            return output_path

# Quick Usage Test
# optimizer = ImageResizer()
# optimized_path = optimizer.optimize_for_api("raw_card_scan.png")
# print(f"Audit-ready image saved to: {optimized_path}")