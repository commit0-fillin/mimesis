"""File data provider."""
from mimesis.datasets import EXTENSIONS, FILENAMES, MIME_TYPES
from mimesis.enums import FileType, MimeType
from mimesis.providers.base import BaseProvider
__all__ = ['File']

class File(BaseProvider):
    """Class for generate data related to files."""

    class Meta:
        name = 'file'

    def extension(self, file_type: FileType | None=None) -> str:
        """Generates a random file extension.

        :param file_type: Enum object FileType.
        :return: Extension of the file.

        :Example:
            .py
        """
        file_type = self.validate_enum(file_type, FileType)
        extensions = EXTENSIONS[file_type.value]
        return self.random.choice(extensions)

    def mime_type(self, type_: MimeType | None=None) -> str:
        """Generates a random mime type.

        :param type_: Enum object MimeType.
        :return: Mime type.
        """
        type_ = self.validate_enum(type_, MimeType)
        mime_types = MIME_TYPES[type_.value]
        return self.random.choice(mime_types)

    def size(self, minimum: int=1, maximum: int=100) -> str:
        """Generates a random file size as string.

        :param minimum: Minimum value.
        :param maximum: Maximum value.
        :return: Size of file.

        :Example:
            56 kB
        """
        size = self.random.randint(minimum, maximum)
        return f"{size} kB"

    def file_name(self, file_type: FileType | None=None) -> str:
        """Generates a random file name with an extension.

        :param file_type: Enum object FileType
        :return: File name.

        :Example:
            legislative.txt
        """
        name = self.random.choice(FILENAMES)
        ext = self.extension(file_type)
        return f"{name}{ext}"
