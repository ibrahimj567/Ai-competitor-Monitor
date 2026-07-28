from app.crawler.playwright_engine import PlaywrightEngine

engine = PlaywrightEngine()

result = engine.fetch("https://openai.com")

print(result)