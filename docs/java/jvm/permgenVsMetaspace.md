---
title: PermGen vs Metaspace
tags: [java, jvm, memory, performance, interview]
---

# PermGen vs Metaspace

PermGen was replaced by Metaspace because PermGen had a fixed, JVM-managed size that frequently caused `OutOfMemoryError` when loading many classes (especially in frameworks like Spring).

Metaspace moved class metadata to native memory, allowing it to grow dynamically and reducing class-loading failures.

## Overview

### PermGen (Before Java 8)

**Stored:**

* Class metadata
* Method metadata
* Constant pool

**Fixed size**

**Configured via:**

```bash
-XX:PermSize
-XX:MaxPermSize
```

**Common failure:**

```
OutOfMemoryError: PermGen space
```

### Problems with PermGen

* Hard to size correctly
* Frequent crashes in:
  * Spring / Hibernate
  * App servers
  * Hot redeployments
* JVM had to manage resizing → fragile

### Metaspace (Java 8+)

**Stores:**

* Class metadata
* Method metadata

**Key characteristics:**

* Lives in native memory (outside heap)
* Grows dynamically
* Limited by OS memory (not JVM heap)

**New flags introduced:**

```bash
-XX:MetaspaceSize
-XX:MaxMetaspaceSize
```

### Benefits

* Fewer class-loading crashes
* Better behavior for large frameworks
* No artificial JVM memory ceiling by default

## JVM Memory Model

Understanding where different Java elements are stored in memory is crucial for debugging and performance optimization.

### The Golden Rule

> 💡 **Stack holds execution.**  
> 💡 **Heap holds objects.**  
> 💡 **Metaspace holds class definitions.**

If you remember only this, you're solid.

### Important Note About Static Fields

**Metaspace knows about static fields, but does not store their values.**

* Static field **definitions** → Metaspace
* Static field **values** → Heap

### Memory Location Summary

| Thing | Lives Where | Notes |
|-------|-------------|-------|
| Class structure | Metaspace | Class metadata, method definitions |
| Methods | Metaspace | Method bytecode and metadata |
| Local variables | Stack | Method-local variables |
| Method parameters | Stack | Function arguments |
| Object instances (`new`) | Heap | All object instances |
| Static objects | Heap | Static object references point to heap |
| Static primitives | Heap | Static primitive values stored in heap |
| References | Stack | Pointers to objects in heap |

### Quick Self-Check

Test your understanding with these examples:

**Example Code:**
```java
class User {
    static User staticUser = new User("Static");
    String name;
    
    User(String name) {
        this.name = name;
    }
}

// In a method:
User user = new User("Naman");
```

**Questions:**

* **Where does `user` live?** → Stack (reference variable)
* **Where does `new User("Naman")` live?** → Heap (object instance)
* **Where does `User` class live?** → Metaspace (class definition)
* **Where does `staticUser` object live?** → Heap (static object instance)
* **Where does `staticUser` reference live?** → Metaspace (static field definition)

## One-Line Interview Answer

> 💡 **"PermGen was replaced by Metaspace because PermGen had a fixed size and caused frequent OutOfMemoryErrors during class loading. Metaspace uses native memory, grows dynamically, and is more suitable for modern frameworks like Spring."**

```
Metaspace stores class metadata and lives in native memory.
It grows dynamically and is independent of heap.
Heavy frameworks like Spring consume Metaspace aggressively through class loading and proxies.
Metaspace issues often come from classloader leaks, not object leaks.
```
