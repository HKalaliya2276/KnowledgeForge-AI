import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        text = text.replace("\x00", " ")

        text = re.sub(r'\r', '\n', text)

        text = re.sub(r'\n{3,}', '\n\n', text)

        text = re.sub(r'[ \t]+', ' ', text)

        text = text.strip()

        return text