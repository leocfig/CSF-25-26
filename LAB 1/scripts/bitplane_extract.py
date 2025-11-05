#!/usr/bin/env python3
from PIL import Image
import argparse
from pathlib import Path

def apply_mask_all_bitplanes_scaled(image_path: Path, outdir: Path):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    outdir.mkdir(parents=True, exist_ok=True)

    for bit in range(8):
        mask = 1 << bit
        # create a new image for this mask
        masked_img = Image.new("RGB", (width, height))
        masked_pixels = masked_img.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # apply mask and scale to 0-255
                r_masked = 255 if (r & mask) else 0
                g_masked = 255 if (g & mask) else 0
                b_masked = 255 if (b & mask) else 0
                masked_pixels[x, y] = (r_masked, g_masked, b_masked)

        out_file = outdir / f"{image_path.stem}_mask_0x{mask:02X}.png"
        masked_img.save(out_file)
        print(f"Saved scaled bitplane image: {out_file}")

def main():
    parser = argparse.ArgumentParser(description="Create scaled bitplane images for RGB channels")
    parser.add_argument("input", help="Input PNG file")
    parser.add_argument("--outdir", default="bitplanes", help="Directory to save output images")
    args = parser.parse_args()

    apply_mask_all_bitplanes_scaled(Path(args.input), Path(args.outdir))

if __name__ == "__main__":
    main()

