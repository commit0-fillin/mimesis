"""The data provider of a variety of codes."""
from mimesis.datasets import EAN_MASKS, IMEI_TACS, ISBN_GROUPS, ISBN_MASKS, LOCALE_CODES
from mimesis.enums import EANFormat, ISBNFormat
from mimesis.locales import Locale
from mimesis.providers.base import BaseProvider
from mimesis.shortcuts import luhn_checksum
__all__ = ['Code']

class Code(BaseProvider):
    """A class, which provides methods for generating codes."""

    class Meta:
        name = 'code'

    def locale_code(self) -> str:
        """Generates a random locale code (MS-LCID).

        See Windows Language Code Identifier Reference
        for more information.

        :return: Locale code.
        """
        return self.random.choice(LOCALE_CODES)

    def issn(self, mask: str='####-####') -> str:
        """Generates a random ISSN.

        :param mask: Mask of ISSN.
        :return: ISSN.
        """
        issn = self.random.custom_code(mask=mask)
        check_digit = self._calculate_check_digit(issn)
        return f"{issn}{check_digit}"

    def _calculate_check_digit(self, issn: str) -> str:
        """Calculate the check digit for ISSN."""
        total = sum((8 - i) * int(digit) for i, digit in enumerate(issn.replace('-', '')))
        check = (11 - (total % 11)) % 11
        return 'X' if check == 10 else str(check)

    def isbn(self, fmt: ISBNFormat | None=None, locale: Locale=Locale.DEFAULT) -> str:
        """Generates ISBN for current locale.

        To change ISBN format, pass parameter ``code`` with needed value of
        the enum object :class:`~mimesis.enums.ISBNFormat`

        :param fmt: ISBN format.
        :param locale: Locale code.
        :return: ISBN.
        :raises NonEnumerableError: if code is not enum ISBNFormat.
        """
        fmt = self.validate_enum(fmt, ISBNFormat)
        mask = ISBN_MASKS[fmt.value]
        
        if locale in ISBN_GROUPS:
            isbn = f"{ISBN_GROUPS[locale]}{self.random.custom_code(mask=mask[1:])}"
        else:
            isbn = self.random.custom_code(mask=mask)
        
        check_digit = self._calculate_isbn_check_digit(isbn)
        return f"{isbn}{check_digit}"

    def _calculate_isbn_check_digit(self, isbn: str) -> str:
        """Calculate the check digit for ISBN."""
        total = sum((10 if x == 'X' else int(x)) * (10 - i) for i, x in enumerate(isbn))
        check = (11 - (total % 11)) % 11
        return 'X' if check == 10 else str(check)

    def ean(self, fmt: EANFormat | None=None) -> str:
        """Generates EAN.

        To change an EAN format, pass parameter ``code`` with needed value of
        the enum object :class:`~mimesis.enums.EANFormat`.

        :param fmt: Format of EAN.
        :return: EAN.
        :raises NonEnumerableError: if code is not enum EANFormat.
        """
        fmt = self.validate_enum(fmt, EANFormat)
        mask = EAN_MASKS[fmt.value]
        ean = self.random.custom_code(mask=mask[:-1])
        check_digit = luhn_checksum(ean)
        return f"{ean}{check_digit}"

    def imei(self) -> str:
        """Generates a random IMEI.

        :return: IMEI.
        """
        tac = self.random.choice(IMEI_TACS)
        serial = self.random.custom_code(mask='######')
        imei = f"{tac}{serial}"
        check_digit = luhn_checksum(imei)
        return f"{imei}{check_digit}"

    def pin(self, mask: str='####') -> str:
        """Generates a random PIN code.

        :param mask: Mask of pin code.
        :return: PIN code.
        """
        return self.random.custom_code(mask=mask)
