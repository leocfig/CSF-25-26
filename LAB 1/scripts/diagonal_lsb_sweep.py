from PIL import Image

im = Image.open("RaceCar.png").convert("RGB")
w, h = im.size
pixels = im.load()

max_height = 552 # (552 pixels 0-551)
# This is the last pixel in the last diagonal. 
# Once it's reached the program stops retrieving data. (It also doesnt include this point)
last_pixel = (220, 331)

bit_stream = ""

for i in range(max_height):
    for j in range(i, -1, -1):
        if (i == max_height - 1) and (j == last_pixel[1]):
            break
        r, g, b = pixels[i - j, j]

        bit_stream += f"{r & 0xF:04b}"  # 0xF masks the last 4 bits
        bit_stream += f"{g & 0xF:04b}"
        bit_stream += f"{b & 0xF:04b}"


byte_array = bytearray()
for k in range(0, len(bit_stream), 8):
    byte_chunk = bit_stream[k:k+8]
    if len(byte_chunk) < 8:
        byte_chunk = byte_chunk.ljust(8, '0')  # pad last byte if needed
    byte_array.append(int(byte_chunk, 2))

# Save or print the extracted data
with open("extracted_data.bin", "wb") as f:
    f.write(byte_array)

print("Extraction complete. Saved to extracted_data.bin")
