"""Base data provider."""
import contextlib
import json
import operator
import typing as t
from functools import reduce
from mimesis import random as _random
from mimesis.constants import DATADIR, LOCALE_SEP
from mimesis.exceptions import NonEnumerableError
from mimesis.locales import Locale, validate_locale
from mimesis.types import JSON, MissingSeed, Seed
__all__ = ['BaseDataProvider', 'BaseProvider']

class BaseProvider:
    """This is a base class for all providers.


    :attr: random: An instance of :class:`mimesis.random.Random`.
    :attr: seed: Seed for random.
    """

    class Meta:
        name: str

    def __init__(self, *, seed: Seed=MissingSeed, random: _random.Random | None=None) -> None:
        """Initialize attributes.

        Keep in mind that locale-independent data providers will work
        only with keyword-only arguments.

        :param seed: Seed for random.
            When set to `None` the current system time is used.
        :param random: Custom random.
            See https://github.com/lk-geimfari/mimesis/issues/1313 for details.
        """
        if random is not None:
            if not isinstance(random, _random.Random):
                raise TypeError('The random must be an instance of mimesis.random.Random')
            self.random = random
        else:
            self.random = _random.Random()
        self.seed = seed
        self.reseed(seed)

    def reseed(self, seed: Seed=MissingSeed) -> None:
        """Reseeds the internal random generator.

        In case we use the default seed, we need to create a per instance
        random generator. In this case, two providers with the same seed
        will always return the same values.

        :param seed: Seed for random.
            When set to `None` the current system time is used.
        """
        if seed is not MissingSeed:
            self.seed = seed
            self.random.seed(seed)
        else:
            self.random.seed()

    def validate_enum(self, item: t.Any, enum: t.Any) -> t.Any:
        """Validates various enum objects that are used as arguments for methods.

        :param item: Item of an enum object.
        :param enum: Enum object.
        :return: Value of item.
        :raises NonEnumerableError: If enums has not such an item.
        """
        if item is None:
            return self.random.choice_enum_item(enum)
        if isinstance(item, enum):
            return item
        if item in enum.__members__:
            return enum[item]
        raise NonEnumerableError(enum)

    def _read_global_file(self, file_name: str) -> t.Any:
        """Reads JSON file and return dict.

        Reads JSON file from mimesis/data/global/ directory.

        :param file_name: Path to file.
        :raises FileNotFoundError: If the file was not found.
        :return: JSON data.
        """
        file_path = DATADIR.joinpath('global', file_name)
        try:
            with open(file_path, encoding='utf8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found")

    def _has_seed(self) -> bool:
        """Internal API to check if seed is set."""
        return self.seed is not MissingSeed

    def __str__(self) -> str:
        """Human-readable representation of locale."""
        return self.__class__.__name__

class BaseDataProvider(BaseProvider):
    """This is a base class for all data providers."""

    def __init__(self, locale: Locale=Locale.DEFAULT, seed: Seed=MissingSeed, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize attributes for data providers.

        :param locale: Current locale.
        :param seed: Seed to all the random functions.
        """
        super().__init__(*args, seed=seed, **kwargs)
        self._dataset: JSON = {}
        self._setup_locale(locale)
        self._load_dataset()

    def _setup_locale(self, locale: Locale=Locale.DEFAULT) -> None:
        """Set up locale after pre-check.

        :param str locale: Locale
        :raises UnsupportedLocale: When locale not supported.
        :return: Nothing.
        """
        self.locale = validate_locale(locale)

    def _extract(self, keys: list[str], default: t.Any=None) -> t.Any:
        """Extracts nested values from JSON file by list of keys.

        :param keys: List of keys (order extremely matters).
        :param default: Default value.
        :return: Data.
        """
        try:
            return reduce(operator.getitem, keys, self._dataset)
        except (KeyError, TypeError):
            return default

    def _update_dict(self, initial: JSON, other: JSON) -> JSON:
        """Recursively updates a dictionary.

        :param initial: Dict to update.
        :param other: Dict to update from.
        :return: Updated dict.
        """
        for key, value in other.items():
            if isinstance(value, dict):
                initial[key] = self._update_dict(initial.get(key, {}), value)
            else:
                initial[key] = value
        return initial

    def _load_dataset(self) -> None:
        """Loads the content from the JSON dataset.

        :return: The content of the file.
        :raises UnsupportedLocale: Raises if locale is unsupported.
        """
        locale = self.locale.replace(LOCALE_SEP, '/')
        file_path = DATADIR.joinpath(locale, f'{self.Meta.name}.json')
        try:
            with open(file_path, encoding='utf8') as f:
                self._dataset = json.load(f)
        except FileNotFoundError:
            raise UnsupportedLocale(self.locale)

    def update_dataset(self, data: JSON) -> None:
        """Updates dataset merging a given dict into default data.

        This method may be useful when you need to override data
        for a given key in JSON file.
        """
        self._dataset = self._update_dict(self._dataset, data)

    def get_current_locale(self) -> str:
        """Returns current locale.

        If locale is not defined, then this method will always return ``en``,
        because ``en`` is default locale for all providers, excluding builtins.

        :return: Current locale.
        """
        return getattr(self, 'locale', Locale.EN)

    def _override_locale(self, locale: Locale=Locale.DEFAULT) -> None:
        """Overrides current locale with passed and pull data for new locale.

        :param locale: Locale
        :return: Nothing.
        """
        self._setup_locale(locale)
        self._load_dataset()

    @contextlib.contextmanager
    def override_locale(self, locale: Locale) -> t.Generator['BaseDataProvider', None, None]:
        """Context manager that allows overriding current locale.

        Temporarily overrides current locale for
        locale-dependent providers.

        :param locale: Locale.
        :return: Provider with overridden locale.
        """
        original_locale = self.locale
        original_dataset = self._dataset.copy()
        try:
            self._override_locale(locale)
            yield self
        finally:
            self.locale = original_locale
            self._dataset = original_dataset

    def __str__(self) -> str:
        """Human-readable representation of locale."""
        locale = Locale(getattr(self, 'locale', Locale.DEFAULT))
        return f'{self.__class__.__name__} <{locale}>'
