from bs4 import BeautifulSoup
from bs4 import Comment


class HTMLCleaner:

    REMOVE_TAGS = [
        "script",
        "style",
        "svg",
        "iframe",
        "noscript",
        "meta",
        "link"
    ]

    KEEP_TAGS = [
        "title",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "p",
        "li",
        "a",
        "button",
        "span"
    ]

    def clean(self, html: str):

        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted tags
        for tag in self.REMOVE_TAGS:
            for t in soup.find_all(tag):
                t.decompose()

        # Remove HTML comments
        comments = soup.find_all(
            string=lambda text: isinstance(text, Comment)
        )

        for comment in comments:
            comment.extract()

        content = []

        for tag in soup.find_all(self.KEEP_TAGS):

            text = tag.get_text(
                separator=" ",
                strip=True
            )

            if len(text) > 3:

                content.append(text)

        return "\n".join(content)