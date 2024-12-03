"""Provides personal data."""
import hashlib
import re
import typing as t
import uuid
from datetime import date, datetime
from string import ascii_letters, digits, punctuation
from mimesis.datasets import BLOOD_GROUPS, CALLING_CODES, EMAIL_DOMAINS, GENDER_CODES, GENDER_SYMBOLS, USERNAMES
from mimesis.enums import Gender, TitleType
from mimesis.providers.base import BaseDataProvider
from mimesis.types import Date
__all__ = ['Person']

class Person(BaseDataProvider):
    """Class for generating personal data."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize attributes.

        :param locale: Current locale.
        :param seed: Seed.
        """
        super().__init__(*args, **kwargs)

    class Meta:
        name = 'person'
        datafile = f'{name}.json'

    def birthdate(self, min_year: int=1980, max_year: int=2023) -> Date:
        """Generates a random birthdate as a :py:class:`datetime.date` object.

        :param min_year: Maximum birth year.
        :param max_year: Minimum birth year.
        :return: Random date object.
        """
        year = self.random.randint(min_year, max_year)
        month = self.random.randint(1, 12)
        day = self.random.randint(1, 28)  # Using 28 to avoid invalid dates
        return date(year, month, day)

    def name(self, gender: Gender | None=None) -> str:
        """Generates a random name.

        :param gender: Gender's enum object.
        :return: Name.

        :Example:
            John.
        """
        gender = self.validate_enum(gender, Gender)
        names = self._dataset['names']
        return self.random.choice(names[gender.value])

    def first_name(self, gender: Gender | None=None) -> str:
        """Generates a random first name.

        ..note: An alias for :meth:`~.name`.

        :param gender: Gender's enum object.
        :return: First name.
        """
        return self.name(gender)

    def surname(self, gender: Gender | None=None) -> str:
        """Generates a random surname.

        :param gender: Gender's enum object.
        :return: Surname.

        :Example:
            Smith.
        """
        gender = self.validate_enum(gender, Gender)
        surnames = self._dataset['surnames']
        if isinstance(surnames, dict) and gender.value in surnames:
            return self.random.choice(surnames[gender.value])
        return self.random.choice(surnames)

    def last_name(self, gender: Gender | None=None) -> str:
        """Generates a random last name.

        ..note: An alias for :meth:`~.surname`.

        :param gender: Gender's enum object.
        :return: Last name.
        """
        return self.surname(gender)

    def title(self, gender: Gender | None=None, title_type: TitleType | None=None) -> str:
        """Generates a random title for name.

        You can generate a random prefix or suffix
        for name using this method.

        :param gender: The gender.
        :param title_type: TitleType enum object.
        :return: The title.
        :raises NonEnumerableError: if gender or title_type in incorrect format.

        :Example:
            PhD.
        """
        gender = self.validate_enum(gender, Gender)
        title_type = self.validate_enum(title_type, TitleType)
        
        titles = self._dataset['titles']
        if title_type == TitleType.ACADEMIC:
            return self.random.choice(titles['academic'])
        elif title_type == TitleType.SOCIAL:
            return self.random.choice(titles['social'][gender.value])
        else:
            return self.random.choice(titles['religious'])

    def full_name(self, gender: Gender | None=None, reverse: bool=False) -> str:
        """Generates a random full name.

        :param reverse: Return reversed full name.
        :param gender: Gender's enum object.
        :return: Full name.

        :Example:
            Johann Wolfgang.
        """
        gender = self.validate_enum(gender, Gender)
        if reverse:
            return f"{self.surname(gender)} {self.name(gender)}"
        return f"{self.name(gender)} {self.surname(gender)}"

    def username(self, mask: str | None=None, drange: tuple[int, int]=(1800, 2100)) -> str:
        """Generates a username by mask.

        Masks allow you to generate a variety of usernames.

        - **C** stands for capitalized username.
        - **U** stands for uppercase username.
        - **l** stands for lowercase username.
        - **d** stands for digits in the username.

        You can also use symbols to separate the different parts
        of the username: **.** **_** **-**

        :param mask: Mask.
        :param drange: Digits range.
        :raises ValueError: If template is not supported.
        :return: Username as string.

        Example:
            >>> username(mask='C_C_d')
            Cotte_Article_1923
            >>> username(mask='U.l.d')
            ELKINS.wolverine.2013
            >>> username(mask='l_l_d', drange=(1900, 2021))
            plasmic_blockader_1907
        """
        if mask is None:
            mask = self.random.choice(['C.l', 'C_l', 'C-l', 'U.l', 'U_l', 'U-l'])

        username = ''
        for char in mask:
            if char in 'CUl':
                word = self.random.choice(USERNAMES)
                if char == 'C':
                    username += word.capitalize()
                elif char == 'U':
                    username += word.upper()
                else:
                    username += word.lower()
            elif char == 'd':
                username += str(self.random.randint(drange[0], drange[1]))
            else:
                username += char

        return username

    def password(self, length: int=8, hashed: bool=False) -> str:
        """Generates a password or hash of password.

        :param length: Length of password.
        :param hashed: SHA256 hash.
        :return: Password or hash of password.

        :Example:
            k6dv2odff9#4h
        """
        characters = ascii_letters + digits + punctuation
        password = ''.join(self.random.choice(characters) for _ in range(length))
        
        if hashed:
            return hashlib.sha256(password.encode()).hexdigest()
        return password

    def email(self, domains: t.Sequence[str] | None=None, unique: bool=False) -> str:
        """Generates a random email.

        :param domains: List of custom domains for emails.
        :param unique: Makes email addresses unique.
        :return: Email address.
        :raises ValueError: if «unique» is True and the provider was seeded.

        :Example:
            foretime10@live.com
        """
        if unique and self._has_seed():
            raise ValueError('You cannot use «unique» parameter with the seeded provider')

        if domains is None:
            domains = EMAIL_DOMAINS

        domain = self.random.choice(domains)
        name = self.username(mask='l').lower()
        
        if unique:
            return f'{name}{uuid.uuid4().hex[:8]}@{domain}'
        return f'{name}@{domain}'

    def gender_symbol(self) -> str:
        """Generate a random sex symbol.

        :Example:
            ♂
        """
        return self.random.choice(GENDER_SYMBOLS)

    def gender_code(self) -> int:
        """Generate a random ISO/IEC 5218 gender code.

        Generate a random title of gender code for the representation
        of human sexes is an international standard that defines a
        representation of human sexes through a language-neutral single-digit
        code or symbol of gender.

        Codes for the representation of human sexes is an international
        standard (0 - not known, 1 - male, 2 - female, 9 - not applicable).

        :return:
        """
        return self.random.choice(GENDER_CODES)

    def gender(self) -> str:
        """Generates a random gender title.

        :Example:
            Male
        """
        return self.random.choice(self._dataset['gender'])

    def sex(self) -> str:
        """An alias for method :meth:`~.gender`.

        :return: Sex.
        """
        return self.gender()

    def height(self, minimum: float=1.5, maximum: float=2.0) -> str:
        """Generates a random height in meters.

        :param minimum: Minimum value.
        :param float maximum: Maximum value.
        :return: Height.

        :Example:
            1.85.
        """
        h = self.random.uniform(minimum, maximum)
        return f"{h:.2f}"

    def weight(self, minimum: int=38, maximum: int=90) -> int:
        """Generates a random weight in Kg.

        :param minimum: min value
        :param maximum: max value
        :return: Weight.

        :Example:
            48.
        """
        return self.random.randint(minimum, maximum)

    def blood_type(self) -> str:
        """Generates a random blood type.

        :return: Blood type (blood group).

        :Example:
            A+
        """
        return self.random.choice(BLOOD_GROUPS)

    def occupation(self) -> str:
        """Generates a random job.

        :return: The name of job.

        :Example:
            Programmer.
        """
        return self.random.choice(self._dataset['occupation'])

    def political_views(self) -> str:
        """Get a random political views.

        :return: Political views.

        :Example:
            Liberal.
        """
        return self.random.choice(self._dataset['political_views'])

    def worldview(self) -> str:
        """Generates a random worldview.

        :return: Worldview.

        :Example:
            Pantheism.
        """
        return self.random.choice(self._dataset['worldview'])

    def views_on(self) -> str:
        """Get a random views on.

        :return: Views on.

        :Example:
            Negative.
        """
        return self.random.choice(self._dataset['views_on'])

    def nationality(self, gender: Gender | None=None) -> str:
        """Generates a random nationality.

        :param gender: Gender.
        :return: Nationality.

        :Example:
            Russian
        """
        gender = self.validate_enum(gender, Gender)
        nationalities = self._dataset['nationality']
        
        if isinstance(nationalities, dict) and gender.value in nationalities:
            return self.random.choice(nationalities[gender.value])
        return self.random.choice(nationalities)

    def university(self) -> str:
        """Generates a random university name.

        :return: University name.

        :Example:
            MIT.
        """
        return self.random.choice(self._dataset['university'])

    def academic_degree(self) -> str:
        """Generates a random academic degree.

        :return: Degree.

        :Example:
            Bachelor.
        """
        return self.random.choice(self._dataset['academic_degree'])

    def language(self) -> str:
        """Generates a random language name.

        :return: Random language.

        :Example:
            Irish.
        """
        return self.random.choice(self._dataset['language'])

    def phone_number(self, mask: str='', placeholder: str='#') -> str:
        """Generates a random phone number.

        :param mask: Mask for formatting number.
        :param placeholder: A placeholder for a mask (default is #).
        :return: Phone number.

        :Example:
            +7-(963)-409-11-22.
        """
        if not mask:
            mask = self.random.choice(CALLING_CODES) + '-###-###-####'
        
        return ''.join(self.random.choice(digits) if char == placeholder else char for char in mask)

    def telephone(self, *args: t.Any, **kwargs: t.Any) -> str:
        """An alias for :meth:`~.phone_number`."""
        return self.phone_number(*args, **kwargs)

    def identifier(self, mask: str='##-##/##') -> str:
        """Generates a random identifier by mask.

        With this method, you can generate any identifiers that
        you need by specifying the mask.

        :param mask:
            The mask. Here ``@`` is a placeholder for characters and ``#`` is
            placeholder for digits.
        :return: An identifier.

        :Example:
            07-97/04
        """
        return ''.join(self.random.choice(ascii_letters) if char == '@' else
                       self.random.choice(digits) if char == '#' else char
                       for char in mask)
