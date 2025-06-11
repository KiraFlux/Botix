from typing import Any
from typing import Mapping

from projectmaster.abc.attributes.loader import AttributesLoader
from projectmaster.core.attributes import SectionAttributes


class SectionAttributesLoader(AttributesLoader[SectionAttributes]):

    def parse(self, data: Mapping[str, Any]) -> SectionAttributes:
        return SectionAttributes(
            name=self.path.name,
            level=int(data['level']),
            desc=str(data['desc'])
        )

    def getSuffix(self) -> str:
        return "section"
