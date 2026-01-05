---
notion_page_id: 2dfff901-fc97-8106-90a4-fa2d5ee35e14
---

## Factory Design Pattern

### Intent

- **Encapsulate object creation** behind a common interface so that clients do not depend on concrete classes.

- **Defer the choice of concrete type to runtime**, enabling flexibility and easier changes.

### Problem

- **Object creation logic is scattered** across the codebase, making it hard to change or extend.

- **Clients depend directly on concrete classes**, reducing flexibility and increasing coupling.

### Solution

- **Introduce a factory** responsible for creating objects.

- **Expose a factory method** that returns an interface or abstract type, hiding the concrete implementation.

### When to Use

- **Exact type is not known at compile time** or may vary at runtime.

- **You want to centralize and control object creation**, e.g., based on configuration, environment, or input parameters.