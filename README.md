<!--
OmniCore-Robotics
Copyright (C) 2025  Naumov Maxim

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

<div align="center">
  <h1>OmniCore Robotics</h1>
  <p>Открытая модульная платформа для создания мобильных роботов</p>
</div>

> ### Обзор
> Проект разрабатывает совместимые модули и шасси для мобильных роботов
>
> **Разработка происходит с использованием:**
> - 3D-печати (FFF/FDM)
> - Лазерной резки
> - Модульного подхода в проектировании
>
> **Цели**
> 1. Создание экосистемы модулей и шасси для быстрой сборки роботов
> 2. Обеспечение доступности производства (домашние 3D-принтеры или лазерная резка)
> 3. Поддержка модернизации и обратная совместимость
>
> <sub>Платформа для разработки</sub>

---

## Структура репозитория

> ### [Модели](./Модели)
> Основные проектные файлы для аппаратных компонентов
>
> **Компоненты:**
> - [Механика](./Модели/Механика) — Сборочные единицы механики
> - [Модули](./Модели/Модули) — Универсальные модули
> - [Колеса](./Модели/Колеса) — Серии дисков и шин
> - [Электроника](./Модели/Электроника) — Модели электрических компонентов
> - [Конструктив](./Модели/Конструктив) — Конструкционные элементы
> - [Шасси](./Модели/Шасси) — Серии шасси
> - [Профили](./Модели/Профили) — Вспомогательные модели
> - [Формы](./Модели/Формы) — Формы для отливки
>
> <sub>Для проектирования используется КОМПАС 3D v23: `.m3d`, `.a3d`  
> Подготовка к печати - PrusaSlicer: `.3mf`, `.stp`</sub>

> ### [Код](./Код)
> Программное обеспечение для управления роботами
>
> **Разделы:**
> - [Arduino](./Код/Arduino) — Скетчи (Примеры)
> - [PlatformIO](./Код/PlatformIO) — Проекты PIO
>
> <sub>Используется Clion или VS Code для разработки</sub>

> ### [.meta](./.meta)
> Служебные данные и утилиты проекта
>
> <sub>Метаданные проекта и вспомогательные инструменты</sub>

---

## Участие в проекте

Для вклада в разработку:

1. Создайте форк репозитория
2. Ознакомьтесь с [правилами участия](./CONTRIBUTING.md)
3. Выполните pull request с вашими изменениями

## Лицензия

Проект распространяется под лицензией **GNU General Public License v3.0**.  
Любые производные работы должны оставаться открытыми и распространяться под той же лицензией.

Подробнее: [LICENSE](./LICENSE)