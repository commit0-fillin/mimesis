"""Provides data related to payment."""
import re
import string
import typing as t
from mimesis.datasets import CREDIT_CARD_NETWORKS
from mimesis.enums import CardType, Gender
from mimesis.exceptions import NonEnumerableError
from mimesis.locales import Locale
from mimesis.providers.base import BaseProvider
from mimesis.providers.person import Person
from mimesis.shortcuts import luhn_checksum
__all__ = ['Payment']

class Payment(BaseProvider):
    """Class that provides data related to payments."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize attributes.

        :param args: Arguments.
        :param kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._person = Person(locale=Locale.EN, seed=self.seed, random=self.random)

    class Meta:
        name = 'payment'

    def cid(self) -> str:
        """Generates a random CID.

        :return: CID code.

        :Example:
            7452
        """
        return ''.join(self.random.choice(string.digits) for _ in range(3))

    def paypal(self) -> str:
        """Generates a random PayPal account.

        :return: Email of PapPal user.

        :Example:
            wolf235@gmail.com
        """
        return self._person.email(domains=['paypal.com'])

    def bitcoin_address(self) -> str:
        """Generates a random bitcoin address.

        Keep in mind that although it generates **valid-looking** addresses,
        it does not mean that they are actually valid.

        :return: Bitcoin address.

        :Example:
            3EktnHQD7RiAE6uzMj2ZifT9YgRrkSgzQX
        """
        address = ''.join(self.random.choice(string.ascii_letters + string.digits) for _ in range(33))
        return f"1{address}"

    def ethereum_address(self) -> str:
        """Generates a random Ethereum address.

        ..note: The address will look like Ethereum address,
        but keep in mind that it is not the valid address.

        :return: Ethereum address.

        :Example:
            0xe8ece9e6ff7dba52d4c07d37418036a89af9698d
        """
        address = ''.join(self.random.choice(string.hexdigits.lower()) for _ in range(40))
        return f"0x{address}"

    def credit_card_network(self) -> str:
        """Generates a random credit card network.

        :return: Credit card network

        :Example:
            MasterCard
        """
        return self.random.choice(list(CREDIT_CARD_NETWORKS.keys()))

    def credit_card_number(self, card_type: CardType | None=None) -> str:
        """Generates a random credit card number.

        :param card_type: Issuing Network. Default is Visa.
        :return: Credit card number.
        :raises NotImplementedError: if card_type not supported.

        :Example:
            4455 5299 1152 2450
        """
        card_type = self.validate_enum(card_type, CardType)
        prefix = self.random.choice(CREDIT_CARD_NETWORKS[card_type.value])
        number = prefix + ''.join(self.random.choice(string.digits) for _ in range(14 - len(prefix)))
        number += luhn_checksum(number)
        return ' '.join([number[i:i+4] for i in range(0, 16, 4)])

    def credit_card_expiration_date(self, minimum: int=16, maximum: int=25) -> str:
        """Generates a random expiration date for credit card.

        :param minimum: Date of issue.
        :param maximum: Maximum of expiration_date.
        :return: Expiration date of credit card.

        :Example:
            03/19.
        """
        month = self.random.randint(1, 12)
        year = self.random.randint(minimum, maximum)
        return f"{month:02d}/{year:02d}"

    def cvv(self) -> str:
        """Generates a random CVV.

        :return: CVV code.

        :Example:
            069
        """
        return ''.join(self.random.choice(string.digits) for _ in range(3))

    def credit_card_owner(self, gender: Gender | None=None) -> dict[str, str]:
        """Generates a random credit card owner.

        :param gender: Gender of the card owner.
        :type gender: Gender enum.
        :return: Dictionary with credit card owner details.
        """
        gender = self.validate_enum(gender, Gender)
        return {
            "full_name": self._person.full_name(gender=gender),
            "gender": gender.value,
            "birthday": str(self._person.birthdate()),
            "credit_card": self.credit_card_number(),
            "expiration_date": self.credit_card_expiration_date(),
            "cvv": self.cvv()
        }
