from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".docx"
}


class FileScanner:

    @staticmethod
    def scan(data_dir):

        files = []

        for path in Path(data_dir).rglob("*"):

            if (
                path.is_file()
                and path.suffix.lower()
                in SUPPORTED_EXTENSIONS
            ):

                files.append(path)

        return files