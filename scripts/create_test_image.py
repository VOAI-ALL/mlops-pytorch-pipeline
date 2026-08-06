"""Create a deterministic RGB image for prediction endpoint smoke tests."""

from pathlib import Path

from PIL import Image


def main() -> None:
    output = Path("test_image.png")
    image = Image.new("RGB", (32, 32))
    pixels = image.load()
    for y in range(32):
        for x in range(32):
            pixels[x, y] = (x * 8, y * 8, (x + y) * 4)
    image.save(output)
    print(f"Created {output.resolve()}")


if __name__ == "__main__":
    main()

