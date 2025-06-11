from dataclasses import dataclass

from engines.html.abc.widget import Widget


@dataclass(frozen=True)
class Text(Widget):
    def getTag(self) -> str:
        pass

    value: str

    def getContent(self) -> str:
        return self.value
