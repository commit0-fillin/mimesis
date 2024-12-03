"""Specific data provider for Brazil (pt-br)."""
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['BrazilSpecProvider']

class BrazilSpecProvider(BaseDataProvider):
    """Class that provides special data for Brazil (pt-br)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.PT_BR, seed=seed)

    class Meta:
        name = 'brazil_provider'
        datafile = None

    @staticmethod
    def __get_verifying_digit_cpf(cpf: list[int], weight: int) -> int:
        """Calculate the verifying digit for the CPF.

        :param cpf: List of integers with the CPF.
        :param weight: Integer with the weight for the modulo 11 calculate.
        :returns: The verifying digit for the CPF.
        """
        total = sum(digit * (weight - i) for i, digit in enumerate(cpf))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    def cpf(self, with_mask: bool=True) -> str:
        """Get a random CPF.

        :param with_mask: Use CPF mask (###.###.###-##).
        :returns: Random CPF.

        :Example:
            001.137.297-40
        """
        cpf = [self.random.randint(0, 9) for _ in range(9)]
        cpf.append(self.__get_verifying_digit_cpf(cpf, 10))
        cpf.append(self.__get_verifying_digit_cpf(cpf, 11))

        if with_mask:
            return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}." \
                   f"{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"
        return ''.join(map(str, cpf))

    @staticmethod
    def __get_verifying_digit_cnpj(cnpj: list[int], weight: int) -> int:
        """Calculate the verifying digit for the CNPJ.

        :param cnpj: List of integers with the CNPJ.
        :param weight: Integer with the weight for the modulo 11 calculate.
        :returns: The verifying digit for the CNPJ.
        """
        total = sum((cnpj[i] * weight[i] for i in range(len(cnpj))))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    def cnpj(self, with_mask: bool=True) -> str:
        """Get a random CNPJ.

        :param with_mask: Use cnpj mask (###.###.###-##)
        :returns: Random cnpj.

        :Example:
            77.732.230/0001-70
        """
        cnpj = [self.random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
        weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        cnpj.append(self.__get_verifying_digit_cnpj(cnpj, weight))
        
        weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        cnpj.append(self.__get_verifying_digit_cnpj(cnpj, weight))

        if with_mask:
            return f"{cnpj[0]}{cnpj[1]}.{cnpj[2]}{cnpj[3]}{cnpj[4]}." \
                   f"{cnpj[5]}{cnpj[6]}{cnpj[7]}/{cnpj[8]}{cnpj[9]}{cnpj[10]}{cnpj[11]}-" \
                   f"{cnpj[12]}{cnpj[13]}"
        return ''.join(map(str, cnpj))
