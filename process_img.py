from PIL import Image, ImageFilter
from pathlib import Path

def create_small(img, stem, path):
    small_dir = path.parent / f'{path.name}-small'
    small_dir.mkdir(parents=True, exist_ok=True)

    small_path = small_dir / f'{stem}-small.webp'
    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    img.save(small_path, format='webp', quality=10)
    

def process_image(img, filename, path):
    with Image.open(img) as im:
        stem = Path(filename).stem
        new_filename = f'{stem}.webp'
        hero_path = path / new_filename
        im.save(hero_path, format='webp', quality=90)
        create_small(im, stem, path)

        return new_filename