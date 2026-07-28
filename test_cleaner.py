from pathlib import Path

print("Step 1")

from app.services.html_cleaner import HTMLCleaner

print("Step 2")

html = Path(
    "snapshots/1782812892.html"
).read_text(
    encoding="utf-8"
)

print("Step 3")

cleaner = HTMLCleaner()

print("Step 4")

result = cleaner.clean(html)

print("Step 5")

print(result[:1000])