# Contributing to Botix Firmware

Thank you for your interest in contributing to the **Botix** mobile robot firmware project!  
This document defines the standards, architecture, and review process that every contribution must follow.

> **Note:** This document is a supplement to the main [`CONTRIBUTING.md`](../CONTRIBUTING.md) in the repository root. Please read that first for general contribution guidelines, branching strategy, and workflow.

We use a [**coded rule system**](#common-violations-vcodes) (`V...P.`) to keep reviews concise, consistent, and diplomatic. Please read this document carefully before opening a pull request.

## Table of Contents

- [Contributing to Botix Firmware](#contributing-to-botix-firmware)
  - [Table of Contents](#table-of-contents)
  - [Core Principles](#core-principles)
  - [Code Style](#code-style)
    - [Include Organization](#include-organization)
    - [Key Rules](#key-rules)
  - [Architectural Conventions](#architectural-conventions)
    - [Folder and Namespace Structure](#folder-and-namespace-structure)
    - [Layer Dependencies](#layer-dependencies)
    - [Configuration Handling](#configuration-handling)
    - [Error Handling](#error-handling)
    - [Mixins](#mixins)
    - [Memory Management (Arena)](#memory-management-arena)
    - [Console Commands](#console-commands)
  - [Development Process](#development-process)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Useful Scripts](#useful-scripts)
  - [Common Violations (V‑Codes)](#common-violations-vcodes)
    - [Priority Legend](#priority-legend)
    - [V1xx - Architecture](#v1xx---architecture)
    - [V2xx - Project Structure](#v2xx---project-structure)
    - [V3xx - Toolkit Usage](#v3xx---toolkit-usage)
    - [V4xx - C++ Idioms and Practices](#v4xx---c-idioms-and-practices)
    - [V5xx - Documentation and Process](#v5xx---documentation-and-process)
    - [V6xx - Testing and Debugging](#v6xx---testing-and-debugging)
  - [How to Use This Document in Reviews](#how-to-use-this-document-in-reviews)
  - [AI‑Generated Code Policy](#aigenerated-code-policy)
  - [Review Checklist](#review-checklist)

## Core Principles

- **C++20** - the firmware targets C++20 (GCC native / xtensa for ESP32).
- **PlatformIO** - the project is built with PlatformIO; use the provided `platformio.ini` and `makefile`.
- **Header‑only library code** - all modules inside `src/botix/` are header‑only; only `src/main.cpp` and test files may contain `.cpp` implementations.
- **Static polymorphism via CRTP** - prefer compile‑time polymorphism; use virtual functions only where runtime flexibility is genuinely required (type‑erased callbacks, abstract transports).
- **Error handling** - never throw exceptions. Use **three distinct mechanisms** depending on the situation:
  - **`bool`** - when the outcome is purely success/failure and no additional context is needed.
  - **`Option<T>`** - when the method may fail, but the failure is trivial and self‑explanatory (e.g., parsing an integer from a string - only one reason to fail).
  - **`Result<T, E>`** - when there are multiple distinct failure modes, and the caller needs to know *why* the operation failed.
  All three are provided by the Toolkit; use them exclusively.
- **Performance** - prefer `constexpr`, `noexcept`, `[[nodiscard]]`.
- **Testability** - algorithmic parts (console parsing, configuration, commands) must be testable natively (x86) with Unity; hardware‑dependent code is isolated.
- **Minimal Arduino dependencies** - avoid including `<Arduino.h>` in algorithmic code; use portable abstractions from the Toolkit (`kf::gpio`, `kf::Timer`, `kf::rtos`).
- **No default constructors for resource‑dependent types** - types that require configuration or external resources must be constructed with all dependencies.
- **No global state** - mutable static variables, static contexts, and singleton‑like objects that store runtime state are forbidden. Dependencies must be passed explicitly via constructor or method arguments.

## Code Style

We follow the same style as the [KiraFlux Toolkit](https://github.com/KiraFlux/KiraFlux-Toolkit/blob/dev/CONTRIBUTING.md#code-style), with the additions below.

### Include Organization

Includes are grouped; each group has related headers sorted in alphabetic order. Groups are separated by blank lines.

| #   | Header Group              | Note                                               |
| --- | ------------------------- | -------------------------------------------------- |
| 1   | Std                       |                                                    |
| 2   | KiraFlux Toolkit          |                                                    |
| 3   | KiraFlux Toolkit mixins   |                                                    |
| 4   | Project                   |                                                    |
| 5   | Protect Interface headers | Only then included in the interface implementation |

Use `#pragma once` in all headers.

Examples:

- Some component `botix::Foo` in `botix/Foo.hpp`
  ```cpp
  #pragma once

  #include <limits>  // For std::numeric_limits
  #include <utility> // For std::move, std::forward

  #include <kf/Option.hpp>
  
  #include <kf/mixin/Initable.hpp>
  #include <kf/mixin/Resettable.hpp>

  #include "botix/Periphery.hpp"
  #include "botix/transport/Transport.hpp"   
  ```

- Some BarService (Service implementation) `botix/service/BarService.hpp`
  ```cpp
  #pragma once

  #include <kf/math.hpp> // For kf::math::clamp, For kf::math::Vector3f

  #include "botix/Foo.hpp"
  #include "botix/transport/Transport.hpp"   

  #include "botix/service/Service.hpp"
  ```

### Key Rules
- Always use `[[nodiscard]]` for functions whose result should not be ignored.
- Add `constexpr` and `noexcept` whenever possible.
- Avoid `using namespace` in global scope of headers.
- Use Doxygen comments for public API.

## Architectural Conventions

### Folder and Namespace Structure

- Folders mirror the logical modules:
  - `src/botix/system/` - system‑level components (lifecycle, initialization)
  - `src/botix/transport/` - communication transports (ESP‑NOW, WiFi UDP)
  - `src/botix/protocol/` - application protocols (MAVLink, raw)
  - `src/botix/behavior/` - robot behaviors
- **Namespaces must mirror folder structure**:
  - `botix::system`, `botix::service`, `botix::transport`, etc.
  - **Only one nested namespace is allowed**: `botix::internal` for implementation details that are not part of the public API. No other nested namespaces (e.g., `botix::config::internal` is forbidden).
- **File naming**: each file must export exactly one primary type (struct or enum class) with the same name as the file, except for helper functions that naturally belong to that type. Example: `Transport.hpp` defines `botix::transport::Transport`; `EspnowTransport.hpp` defines `botix::transport::EspnowTransport`.

### Layer Dependencies

- **Systems** (`botix::system`) are the highest level; they may depend on services and other systems.
- **Services** (`botix::service`) must not depend on systems; they may depend on other services and configuration.
- **Commands** (`botix::command`) must depend only on services (and configuration), **never on systems**.
- **Transport** and **Protocol** modules are independent and communicate via interfaces.

### Configuration Handling

- All persistent settings are stored in POD structures that inherit from `botix::config::Config<Impl, Version>`.
- Configurations are versioned to handle upgrades.

### Error Handling

We use **three distinct mechanisms** from the Toolkit, each with a specific use case:

| Mechanism    | When to use                                                                                           | Example                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **`bool`**   | The operation either succeeds or fails, and there is **no need** to know why.                         | `sendBuffer(buffer)` - it either sends or not.                                                                                |
| **`Option`** | The operation may produce a value **or** fail for a single, obvious reason.                           | `parseInt(str) -> Option<int>` - failure means “not an integer”.                                                              |
| **`Result`** | The operation may fail for **multiple distinct reasons** and the caller must handle them differently. | `addFoo(arena, bar) -> Result<void, Error>` where `Error` can be `FooStackFull`, `FooAllocationFailed`, or `FooBarMalformed`. |

**Rules:**
- Never throw exceptions.
- Never use `std::optional`, `std::variant`, or `std::expected` - use the Toolkit equivalents.
- Always check return values - do not ignore `bool`, `Option`, or `Result`.
- If a function returns `Result`, prefer `KF_TRY` for early‑error propagation.
- Use `kf::some()`, `kf::none` to construct Option.
- Use `kf::ok()`, `kf::error()` to construct Result.

**Note**  

If you have already checked the invariant

For example:

- if `availableForRead() > 0`, you may safely call `unwrap()` without extra checks, as the condition guarantees that `read()` will return `Some`. This avoids redundant branching and keeps code clean.

    ```cpp
    while (queue.availableForRead() > 0) {
        char const c = queue.read().unwrap();
        // ... process c ...
    }
    ```

Here, the `while` condition ensures that `read()` will always succeed, so `unwrap()` is safe and expresses the intent clearly.

### Mixins

- Use the mixins provided by the Toolkit (`kf/mixin/`):
  - `Initable<Impl, Signature>` - for objects that require initialization.
  - `Poll<Impl>` - for periodic tasks that receive a timestamp.
  - `Configured<Config>` - for objects that hold a configuration reference.
  - `Callbacked<Signature>` - for optional callbacks.
  - `Resettable<Impl>` - for resettable state.
  - `NonCopyable` - for move‑only or singleton objects.
- **Do not duplicate mixin functionality** - if you need a callback, use `Callbacked`; if you need a flush, use `Flush`.

### Memory Management (Arena)

- The `Arena` allocator is provided by the Toolkit and should be used for allocations.
- **Arena must NOT be stored as a member** in systems or services. It must be passed as an argument to methods that need it (e.g., `init(Arena &arena)` or `registerCommands(Arena &arena)`).
- This ensures that ownership and lifetime of the arena are clear and not hidden.
- **`new` / `malloc` (heap allocation) IS STRONGLY FORBIDDEN!**

### Console Commands

- Each command group (e.g., `config`, `transport`, `system`) must be a **struct** that owns its dependencies (through a `Dependencies` struct).
- **No static contexts** - handlers must capture `this` and use member variables.
- Registration functions must be small and take only a console reference and an arena.
- Command handlers must return detailed errors (use `Result` or log messages).

## Development Process

For the overall branching strategy and contribution workflow, please refer to the main [`CONTRIBUTING.md`](../CONTRIBUTING.md) in the repository root. This section provides firmware‑specific clarifications.

## Testing

- **Unit tests** (if any) for algorithmic code are written using the Unity framework and placed in `test/unit/` when present.
- Run them with `pio test -e native`.

## Documentation

- **README.md** - overview, quick start, hardware pinout, build instructions.
- **CONTRIBUTING.md** - this file.
- **Public API** - all headers in `src/botix/` must have Doxygen comments for public types and functions.
- **Internal modules** - may have brief comments; the `internal` namespace is exempt from full documentation.

## Useful Scripts

The root `makefile` includes the Toolkit’s `common.mak`, providing the following shortcuts:

| Target                  | Description                          |
| ----------------------- | ------------------------------------ |
| `make` / `make all`     | Build the firmware.                  |
| `make clean` / `make c` | Clean build artifacts.               |
| `make upload` / `u`     | Build and upload to connected board. |
| `make monitor` / `m`    | Open serial monitor (115200 baud).   |
| `make help` / `h`       | Show help about targets.             |

## Common Violations (V‑Codes)

To keep reviews concise and objective, we use a numbered rule system. When you see a comment like `[V...P.]` in a review, look it up here.

### Priority Legend

| Priority | Name     | Meaning                                                    |
| -------- | -------- | ---------------------------------------------------------- |
| **P0**   | Critical | Security, data loss, hardware damage                       |
| **P1**   | High     | Correctness, architecture violation, broken error handling |
| **P2**   | Medium   | Maintainability, style, code duplication                   |
| **P3**   | Low      | Minor clarity, naming, cosmetic improvements               |

### V1xx - Architecture

| Code     | Name                       | Priority | Description                                                                                         | Example                                                                                                 |
| -------- | -------------------------- | -------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **V101** | Uncontrolled Global State  | P1       | Mutable global state (static, singleton) is forbidden. Dependencies must be passed explicitly.      | `ConfigCommands.hpp` had a static `Context`. Fixed: commands became structs with explicit dependencies. |
| **V102** | Layer Violation            | P1       | A layer depends on a higher layer (e.g., command -> system). Commands must depend only on services. | `TransportCommands` used `TransportSystem`. Fixed: uses `TransportLink` (service).                      |
| **V103** | Lifetime Ambiguity (Arena) | P2       | Storing an `Arena` as a member hides memory lifetime. Pass it as a method argument instead.         | `ConsoleSystem` stored `Arena`. Fixed: `init(Arena &arena)`.                                            |
| **V104** | Circular Dependency        | P1       | Cyclic dependency between modules. Break with interfaces or callbacks.                              | *(general case)*                                                                                        |

### V2xx - Project Structure

| Code     | Name                      | Priority | Description                                                                                      | Example                                                                                        |
| -------- | ------------------------- | -------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **V201** | Namespace‑Folder Mismatch | P2       | Namespace does not match the file path. Only `botix::internal` is allowed as a nested namespace. | `botix::parse` and `botix::foo::bar` violated. Fixed: structures moved to corresponding files. |
| **V202** | File‑Type Mismatch        | P2       | File exports more than one public entity or name does not match primary type.                    | `Foo.hpp` contained `Foo`, `FooBar`. Fixed: `Foo::Bar`.                                        |
| **V203** | Unclear Naming            | P3       | Names do not reflect purpose. Use `PascalCase` for types, `camelCase` for functions/variables.   | `Call` instead of `Context` in commands. Fixed: unified `Context`.                             |
| **V204** | Mixed Include Order       | P3       | Include order violates rule: system headers first, blank line, then project headers.             | *(general case)*                                                                               |

### V3xx - Toolkit Usage

| Code     | Name                           | Priority | Description                                                                                                           | Example                                                                                                              |
| -------- | ------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **V301** | Reinventing the Wheel          | P2       | Creating a custom container instead of using `kf::Array`, `kf::String`, `kf::Slice`.                                  | Created `Text<N>` instead of `kf::Array<char, N>` with null termination. Fixed: use `Array` and `.data()`.           |
| **V302** | Custom Mixin Duplicate         | P2       | Implementing behavior already provided by Toolkit mixins (`Callbacked`, `Resettable`).                                | Created `Sink` instead of `Callbacked`. Fixed: inherit from `Callbacked`.                                            |
| **V303** | Wrong Error‑Handling Mechanism | P1       | Using a custom enum with `Ok` or using `Result` where `bool` or `Option` would suffice - or vice versa.               | `SetStatus` with `Ok` when only success/failure matters. Fixed: used `bool` or `Result<void, Error>` as appropriate. |
| **V304** | Wrong Smart Pointer / Optional | P2       | Using `std::optional`, `std::variant`, or `std::unique_ptr` instead of `kf::Option`, `kf::Result`, or `kf::Function`. | Used `std::optional`. Fixed: `kf::Option`.                                                                           |
| **V305** | Missing Mixin Usage            | P2       | Type does not use an appropriate mixin (`Configured`, `Initable`, `Poll`).                                            | Class with config did not use `Configured`. Fixed: added mixin.                                                      |

### V4xx - C++ Idioms and Practices

| Code     | Name                             | Priority | Description                                                                                      | Example                                                                                                     |
| -------- | -------------------------------- | -------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **V401** | Macro Abuse                      | P2       | Macros for logic or code generation beyond stringification of tokens.                            | `BOTIX_FIELD` did everything. Fixed: macro only for field name, rest is templated factory with type traits. |
| **V402** | Missing constexpr / noexcept     | P3       | Functions that could be `constexpr` or `noexcept` are not marked.                                | *(general case)*                                                                                            |
| **V403** | Unnecessary Runtime Polymorphism | P2       | Using `virtual` where CRTP could be used.                                                        | *(general case)*                                                                                            |
| **V404** | Magic Constants                  | P2       | Using hard‑coded numbers instead of standard constants (`std::numeric_limits`, `INT_MAX`).       | `4294967295.0` instead of `std::numeric_limits<u32>::max()`. Fixed.                                         |
| **V405** | Unsafe Type Casting              | P2       | Using `reinterpret_cast` or C‑style casts without checks.                                        | *(general case)*                                                                                            |
| **V406** | Ignoring Return Value            | P1       | Calling a function that returns `Result` or `bool` without checking value or specific invariant. | `(void) something();` without check. Fixed: add `if (result.isError()) { ... }`.                            |

### V5xx - Documentation and Process

| Code     | Name                                | Priority | Description                                                                                                             | Example                                                                                                                    |
| -------- | ----------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **V501** | Missing API Documentation           | P3       | Public functions/types lack Doxygen comments (`@brief`, `@param`, `@return`).                                           | *(general case)*                                                                                                           |
| **V502** | Inconsistent License Header         | P3       | Missing or incorrect `SPDX-License-Identifier`, wrong copyright year.                                                   | *(general case)*                                                                                                           |
| **V503** | Outdated Comment                    | P3       | Comment does not match code or is obsolete.                                                                             | *(general case)*                                                                                                           |
| **V504** | Misleading Copyright (AI‑Generated) | P2       | Copyright notice claims authorship by someone who did not write the code (e.g., AI‑generated code without attribution). | Header with `Copyright (c) 2026 KiraFlux` on AI‑generated code. Fixed: remove or replace with operator's name + AI notice. |

### V6xx - Testing and Debugging

| Code     | Name                | Priority | Description                                                                          | Example                                                   |
| -------- | ------------------- | -------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| **V601** | Missing Unit Test   | P2       | Algorithmic code is not covered by tests (Unity).                                    | *(general case)*                                          |
| **V602** | Untestable Code     | P2       | Code is tightly coupled to hardware without abstractions, preventing native testing. | *(general case)*                                          |
| **V603** | No Logging on Error | P2       | Error is not logged, making debugging difficult.                                     | Ignoring return without `logger.error`. Fixed: added log. |
| **V604** | Debug Code Left In  | P3       | Debug code remains in the release version.                                           | *(general case)*                                          |

## How to Use This Document in Reviews

When you see a violation, write a short comment with the code and, optionally, a one‑line explanation:

> `V101` - remove the static context.  
> `V301` - use `kf::Array` instead.  
> `V303` - use `bool` here; there is only one failure reason.  
> `V406P1` - check the return value of `init()`.

If the issue is not covered here:
1. Explain it in the comment with enough detail.
2. After the PR, propose an update to this document (open an Issue or submit a PR).

## AI‑Generated Code Policy

If you use AI tools to generate code for this repository:

1. **You are responsible** for the correctness, quality, and compliance of the generated code with this document.
2. **You must ensure** that the code follows all architectural rules, uses the Toolkit correctly, and passes tests.
3. **Copyright attribution**:
   - Do not place the name of another contributor (including the maintainer) on AI‑generated code.
   - Use your own name as the author, or use a header without author attribution.
   - Add a comment indicating that the code was generated with AI assistance.
4. **Mark AI‑generated files** in the PR description so reviewers know what to focus on.
5. **AI‑generated code is still subject to GPL‑3.0‑or‑later** - you must ensure that all license headers are correct.

**Recommended header for AI‑generated code:**
```cpp
// Copyright (c) 2026 <Your Name>
// SPDX-License-Identifier: GPL-3.0-or-later
//
// This file was generated via <Tool Name>.
// Original repository: https://github.com/KiraFlux/botix
```

## Review Checklist

Before submitting a PR, verify the following:

- [ ] Code compiles with `pio run -e esp32dev`.
- [ ] All new algorithmic code has unit tests (`pio test -e native`) or is written in a way that makes testing straightforward.
- [ ] No global state introduced.
- [ ] Dependencies are passed explicitly (no static contexts).
- [ ] The correct error‑handling mechanism is used: `bool` for trivial success/failure, `Option<T>` for single‑point failures, `Result<T, E>` for multiple failure reasons. No custom `enum` with `Ok`.
- [ ] Toolkit mixins are used where applicable (`Callbacked`, `Resettable`, `Configured`).
- [ ] Namespaces match folder structure.
- [ ] All public APIs have Doxygen comments.
- [ ] License headers are correct (`SPDX-License-Identifier: GPL-3.0-or-later`).
- [ ] AI‑generated code is properly attributed.
- [ ] PR description links to relevant issues (`Closes #...`).

---

Thank you for contributing to Botix!
