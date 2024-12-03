"""Specific data provider for the USA (en)."""
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['USASpecProvider']

class USASpecProvider(BaseDataProvider):
    """Class that provides special data for the USA (en)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.EN, seed=seed)

    class Meta:
        name = 'usa_provider'
        datafile = None

    def tracking_number(self, service: str='usps') -> str:
        """Generate random tracking number.

        Supported services: USPS, FedEx and UPS.

        :param str service: Post service.
        :return: Tracking number.
        """
        service = service.lower()
        if service == 'usps':
            return f"{self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)} {self.random.randint(10, 99)}"
        elif service == 'fedex':
            return f"{self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)}"
        elif service == 'ups':
            return f"1Z {self.random.randint(100, 999)} {self.random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{self.random.randint(10, 99)} {self.random.randint(1000, 9999)} {self.random.randint(1000, 9999)} {self.random.randint(1, 9)}"
        else:
            raise ValueError("Unsupported service. Choose 'usps', 'fedex', or 'ups'.")

    def ssn(self) -> str:
        """Generate a random, but valid SSN.

        :returns: SSN.

        :Example:
            569-66-5801
        """
        area = self.random.randint(1, 899)
        group = self.random.randint(1, 99)
        serial = self.random.randint(1, 9999)
        
        # Ensure the area number is not 666 and the group number is not 00
        if area == 666:
            area = 667
        if group == 0:
            group = 1
        
        return f"{area:03d}-{group:02d}-{serial:04d}"
