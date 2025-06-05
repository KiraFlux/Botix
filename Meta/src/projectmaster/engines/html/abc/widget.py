"""Виджет"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Mapping
from typing import Optional


class Widget(ABC):
    """Виджет"""

    @abstractmethod
    def getTag(self) -> str:
        """Получить HTML тэг элемента"""

    @abstractmethod
    def getContent(self) -> str:
        """Получить содержимое виджета"""

    def getAttributes(self) -> Optional[Mapping[str, str]]:
        """Атрибуты виджета"""
        return None

    def render(self) -> str:
        """Рендеринг виджета в HTML"""
        tag = self.getTag()
        return f"<{tag}{self._renderAttributes()}>{self.getContent()}</{tag}>"

    def _renderAttributes(self) -> str:
        attributes = self.getAttributes()

        if attributes is None:
            return " "

        return " " + " ".join(f'{k}="{v}"' for k, v in attributes.items())
