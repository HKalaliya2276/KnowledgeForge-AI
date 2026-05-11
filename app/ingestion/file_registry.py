import json

from pathlib import Path


class FileRegistry:

    def __init__(self, registry_path):

        self.registry_path = Path(
            registry_path
        )

        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.registry_path.exists():

            with open(
                self.registry_path,
                "w"
            ) as f:

                json.dump([], f)

    def load_registry(self):

        with open(
            self.registry_path,
            "r"
        ) as f:

            return json.load(f)

    def save_registry(self, registry):

        with open(
            self.registry_path,
            "w"
        ) as f:

            json.dump(
                registry,
                f,
                indent=4
            )

    def is_hash_processed(
        self,
        content_hash
    ):

        registry = self.load_registry()

        for item in registry:

            if (
                item["content_hash"]
                == content_hash
            ):

                return True

        return False

    def add_file(
        self,
        file_path,
        content_hash,
        chunk_count
    ):

        registry = self.load_registry()

        registry.append({

            "file_path": str(file_path),

            "content_hash": content_hash,

            "chunks": chunk_count
        })

        self.save_registry(registry)