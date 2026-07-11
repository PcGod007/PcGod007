from playwright.sync_api import sync_playwright
from PIL import Image
import io
import os
import pathlib

local_dir = os.path.dirname(os.path.abspath(__file__))
SVGS = [
    pathlib.Path(os.path.join(local_dir, "dark_mode.svg")).as_uri(),
    pathlib.Path(os.path.join(local_dir, "light_mode.svg")).as_uri(),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url in SVGS:
        page = browser.new_page(viewport={"width": 1200, "height": 850})
        page.goto(url, wait_until="networkidle")

        frames = []
        for _ in range(15):
            page.wait_for_timeout(200)
            frames.append(page.screenshot())
            
        name = url.split("/")[-1].replace(".svg", ".webp")
        images = [Image.open(io.BytesIO(f)) for f in frames]
        images[0].save(
            name,
            save_all=True,
            append_images=images[1:],
            duration=200,
            loop=0,
            lossless=False,
            quality=80,
            minimize_size=True,
            method=6,
        )
        print(f"Saved {name}")
        page.close()

    browser.close()
