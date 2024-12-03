"""Provides pseudo-scientific data."""
from mimesis.datasets import SI_PREFIXES, SI_PREFIXES_SYM
from mimesis.enums import MeasureUnit, MetricPrefixSign
from mimesis.providers.base import BaseProvider
__all__ = ['Science']

class Science(BaseProvider):
    """Class for generating pseudo-scientific data."""

    class Meta:
        name = 'science'

    def rna_sequence(self, length: int=10) -> str:
        """Generates a random RNA sequence.

        :param length: Length of block.
        :return: RNA sequence.

        :Example:
            AGUGACACAA
        """
        rna_nucleotides = ['A', 'G', 'C', 'U']
        return ''.join(self.random.choice(rna_nucleotides) for _ in range(length))

    def dna_sequence(self, length: int=10) -> str:
        """Generates a random DNA sequence.

        :param length: Length of block.
        :return: DNA sequence.

        :Example:
            GCTTTAGACC
        """
        dna_nucleotides = ['A', 'G', 'C', 'T']
        return ''.join(self.random.choice(dna_nucleotides) for _ in range(length))

    def measure_unit(self, name: MeasureUnit | None=None, symbol: bool=False) -> str:
        """Returns unit name from the International System of Units.

        :param name: Enum object UnitName.
        :param symbol: Return only symbol
        :return: Unit.
        """
        unit = self.validate_enum(name, MeasureUnit)
        units = {
            MeasureUnit.MASS: ('kilogram', 'kg'),
            MeasureUnit.TIME: ('second', 's'),
            MeasureUnit.TEMPERATURE: ('kelvin', 'K'),
            MeasureUnit.ELECTRIC_CURRENT: ('ampere', 'A'),
            MeasureUnit.AMOUNT_OF_SUBSTANCE: ('mole', 'mol'),
            MeasureUnit.LUMINOUS_INTENSITY: ('candela', 'cd'),
            MeasureUnit.LENGTH: ('metre', 'm'),
        }
        return units[unit][1] if symbol else units[unit][0]

    def metric_prefix(self, sign: MetricPrefixSign | None=None, symbol: bool=False) -> str:
        """Generates a random prefix for the International System of Units.

        :param sign: Sign of prefix (positive/negative).
        :param symbol: Return the symbol of the prefix.
        :return: Metric prefix for SI measure units.
        :raises NonEnumerableError: if sign is not supported.

        :Example:
            mega
        """
        sign = self.validate_enum(sign, MetricPrefixSign)
        prefixes = SI_PREFIXES_SYM if symbol else SI_PREFIXES
        
        if sign == MetricPrefixSign.POSITIVE:
            return self.random.choice(prefixes['positive'])
        elif sign == MetricPrefixSign.NEGATIVE:
            return self.random.choice(prefixes['negative'])
        else:
            return self.random.choice(prefixes['positive'] + prefixes['negative'])
