from difflib import SequenceMatcher


class DiffService:

    IGNORE_WORDS = [
        "cookie",
        "cookies",
        "privacy",
        "analytics",
        "timestamp",
        "session",
        "csrf",
        "google tag manager",
        "gtm"
    ]

    def compare_files(self, old_path, new_path):

        old = open(old_path, encoding="utf-8").read()

        new = open(new_path, encoding="utf-8").read()

        old_lines = [
            x.strip()
            for x in old.splitlines()
            if x.strip()
        ]

        new_lines = [
            x.strip()
            for x in new.splitlines()
            if x.strip()
        ]

        added = []

        removed = []

        matcher = SequenceMatcher(
            None,
            old_lines,
            new_lines
        )

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "insert":

                added.extend(new_lines[j1:j2])

            elif tag == "delete":

                removed.extend(old_lines[i1:i2])

            elif tag == "replace":

                removed.extend(old_lines[i1:i2])
                added.extend(new_lines[j1:j2])

        def keep(line):

            text = line.lower()

            for word in self.IGNORE_WORDS:

                if word in text:
                    return False

            return True

        added = [
            x for x in added
            if keep(x)
        ]

        removed = [
            x for x in removed
            if keep(x)
        ]

        result = []

        if added:

            result.append("ADDED CONTENT\n")

            result.extend(added)

        if removed:

            result.append("\nREMOVED CONTENT\n")

            result.extend(removed)

        return "\n".join(result)