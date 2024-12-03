"""Address module.

This module contains provider Address() and other utils which represent
data related to location, such as street name, city etc.
"""
import typing as t
from mimesis.datasets import CALLING_CODES, CONTINENT_CODES, COUNTRY_CODES, SHORTENED_ADDRESS_FMT
from mimesis.enums import CountryCode
from mimesis.providers.base import BaseDataProvider
__all__ = ['Address']

class Address(BaseDataProvider):
    """Class for generate fake address data.

    This object provides all the data related to
    geographical location.
    """

    class Meta:
        name = 'address'
        datafile = f'{name}.json'

    @staticmethod
    def _dd_to_dms(num: float, _type: str) -> str:
        """Converts decimal number to DMS format.

        :param num: Decimal number.
        :param _type: Type of number.
        :return: Number in DMS format.
        """
        degrees = int(num)
        minutes = int((num - degrees) * 60)
        seconds = round(((num - degrees) * 60 - minutes) * 60, 2)
        direction = 'N' if _type == 'lat' else 'E'
        if num < 0:
            direction = 'S' if _type == 'lat' else 'W'
            degrees = abs(degrees)
        return f"{degrees}°{minutes}'{seconds}\"{direction}"

    def street_number(self, maximum: int=1400) -> str:
        """Generates a random street number.

        :param maximum: Maximum value.
        :return: Street number.
        """
        return str(self.random.randint(1, maximum))

    def street_name(self) -> str:
        """Generates a random street name.

        :return: Street name.
        """
        return self.random.choice(self._dataset['street']['name'])

    def street_suffix(self) -> str:
        """Generates a random street suffix.

        :return: Street suffix.
        """
        return self.random.choice(self._dataset['street']['suffix'])

    def address(self) -> str:
        """Generates a random full address.

        :return: Full address.
        """
        fmt = self.random.choice(SHORTENED_ADDRESS_FMT)
        return fmt.format(
            st_num=self.street_number(),
            st_name=self.street_name(),
            st_sfx=self.street_suffix(),
            city=self.city(),
            state=self.state(),
            postal=self.postal_code(),
        )

    def state(self, abbr: bool=False) -> str:
        """Generates a random administrative district of the country.

        :param abbr: Return ISO 3166-2 code.
        :return: Administrative district.
        """
        key = 'abbr' if abbr else 'name'
        return self.random.choice(self._dataset['state'][key])

    def region(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random region.

        An alias for :meth:`~.state()`.
        """
        return self.state(*args, **kwargs)

    def province(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random province.

        An alias for :meth:`~.state()`.
        """
        return self.state(*args, **kwargs)

    def federal_subject(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random federal_subject (Russia).

        An alias for :meth:`~.state()`.
        """
        return self.state(*args, **kwargs)

    def prefecture(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random prefecture.

        An alias for :meth:`~.state()`.
        """
        return self.state(*args, **kwargs)

    def postal_code(self) -> str:
        """Generates a postal code for current locale.

        :return: Postal code.
        """
        return self.random.custom_code(mask=self._dataset['postal_code_fmt'])

    def zip_code(self) -> str:
        """Generates a zip code.

        An alias for :meth:`~.postal_code()`.

        :return: Zip code.
        """
        return self.postal_code()

    def country_code(self, code: CountryCode | None=CountryCode.A2) -> str:
        """Generates a random code of country.

        Default format is :attr:`~enums.CountryCode.A2` (ISO 3166-1-alpha2),
        you can change it by passing parameter ``fmt``.

        :param code: Country code.
        :return: Country code in selected format.
        :raises KeyError: if fmt is not supported.
        """
        code = self.validate_enum(code, CountryCode)
        return self.random.choice(COUNTRY_CODES[code.value])

    def country_emoji_flag(self) -> str:
        """Generates a randomly chosen country emoji flag.

        :example:
            🇹🇷

        :return: Flag emoji.
        """
        country_code = self.country_code(CountryCode.A2)
        return ''.join([chr(ord(c) + 127397) for c in country_code])

    def default_country(self) -> str:
        """Returns the country associated with the current locale.

        :return: The country associated with current locale.
        """
        return self._dataset['default_country']

    def country(self) -> str:
        """Generates a random country.

        :return: The Country.
        """
        return self.random.choice(self._dataset['country']['name'])

    def city(self) -> str:
        """Generates a random city.

        :return: City name.
        """
        return self.random.choice(self._dataset['city'])

    def _get_fs(self, key: str, dms: bool=False) -> str | float:
        """Get float number.

        :param key: Key (`lt` or `lg`).
        :param dms: DMS format.
        :return: Float number
        """
        from_val, to_val = self._dataset['coordinate'][key]
        number = self.random.uniform(from_val, to_val)
        return self._dd_to_dms(number, key) if dms else number

    def latitude(self, dms: bool=False) -> str | float:
        """Generates a random value of latitude.

        :param dms: DMS format.
        :return: Value of latitude.
        """
        return self._get_fs('lt', dms)

    def longitude(self, dms: bool=False) -> str | float:
        """Generates a random value of longitude.

        :param dms: DMS format.
        :return: Value of longitude.
        """
        return self._get_fs('lg', dms)

    def coordinates(self, dms: bool=False) -> dict[str, str | float]:
        """Generates random geo coordinates.

        :param dms: DMS format.
        :return: Dict with coordinates.
        """
        return {
            'latitude': self.latitude(dms),
            'longitude': self.longitude(dms),
        }

    def continent(self, code: bool=False) -> str:
        """Returns a random continent name or continent code.

        :param code: Return code of a continent.
        :return: Continent name.
        """
        key = 'code' if code else 'name'
        return self.random.choice(self._dataset['continent'][key])

    def calling_code(self) -> str:
        """Generates a random calling code of random country.

        :return: Calling code.
        """
        return self.random.choice(CALLING_CODES)

    def isd_code(self) -> str:
        """Generates a random ISD code.

        An alias for :meth:`~Address.calling_code()`.
        """
        return self.calling_code()
