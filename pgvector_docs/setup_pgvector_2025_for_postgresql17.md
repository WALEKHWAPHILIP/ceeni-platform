
---

# 🧠 Installing pgvector v0.7.4 on Windows with PostgreSQL 17 and Visual Studio 2022

This guide walks you step-by-step to compile and install the `pgvector` PostgreSQL extension from source on **Windows**, using **Visual Studio 2022 Build Tools**. It ensures compatibility with PostgreSQL 17 and is suitable for integration into Django apps.

---

## ✅ Prerequisites

### 1. Install Visual Studio 2022 Build Tools

> 📦 You don’t need the full Visual Studio IDE — just the **Build Tools**.

- Download from [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/)
- Select: **"Build Tools for Visual Studio 2022"**
- During installation, check these components:

  - ✅ **MSVC v143 - VS 2022 C++ x64/x86 build tools**
  - ✅ **Windows 10 SDK** or **Windows 11 SDK**
  - ✅ **MSBuild**

> You’ll find these under the **“C++ build tools”** workload during setup.

---

## 🧪 Step-by-Step: pgvector Build + Install

### 2. Launch the correct shell (Native x64)

Open the **"x64 Native Tools Command Prompt for VS 2022"** as **Administrator**:

- Search in Start Menu for: `x64 Native Tools for VS 2022`
- Right click → **Run as Administrator**

You’ll see something like:

```

---

\*\* Visual Studio 2022 Developer Command Prompt v17.xx.xx
\*\* Copyright (c) 2025 Microsoft Corporation

---

\[vcvarsall.bat] Environment initialized for: 'x64'

````

---

### 3. Clone pgvector and check out a compatible version

```cmd
cd %USERPROFILE%
git clone https://github.com/pgvector/pgvector.git
cd pgvector
git checkout v0.7.4
````

✅ `v0.7.4` is confirmed stable with PostgreSQL 17.

---

### 4. Set environment variables

```cmd
set PGROOT=C:\Program Files\PostgreSQL\17
set PATH=%PGROOT%\bin;%PATH%
```

> Adjust `C:\Program Files\PostgreSQL\17` if your PostgreSQL is installed in a different directory.

---

### 5. Clean previous build artifacts (optional but recommended)

```cmd
del /s src\*.obj
```

---

### 6. Compile the extension

```cmd
nmake /f Makefile.win
```

If successful, you'll see something like:

```
Microsoft (R) Program Maintenance Utility Version 14.44.35215.0
Copyright (C) Microsoft Corporation.  All rights reserved.

Creating library vector.lib and object vector.exp
```

---

### 7. Install pgvector to PostgreSQL directories

```cmd
nmake /f Makefile.win install
```

This will:

* ✅ Copy `vector.dll` → `C:\Program Files\PostgreSQL\17\lib`
* ✅ Copy SQL files → `C:\Program Files\PostgreSQL\17\share\extension`
* ✅ Copy headers → `C:\Program Files\PostgreSQL\17\include\server\extension\vector`

> If you see an "Access Denied" error, make sure your shell is running as **Administrator**.

---

## 🧩 Enable pgvector in PostgreSQL

### 8. Connect using psql:

```cmd
psql -U postgres -d your_database_name
```

Then in the PostgreSQL prompt:

```sql
CREATE EXTENSION vector;
```

To verify:

```sql
\dx
```

You should see something like:

```
 vector | 0.7.4 | public | vector similarity search
```

---

## 🛠️ Troubleshooting

### ❌ Error: `LNK1112: module machine type 'x64' conflicts with target machine type 'x86'`

**Cause**: You’re running the wrong shell (e.g., x86 instead of x64).
**Fix**: Use the **"x64 Native Tools Command Prompt for VS 2022"**.

---

## ✅ Optional: Using pgvector in Django

If you're building a Django project with vector embeddings, define your model like this:

```python
from pgvector.django import VectorField

class CommentAIAnalysis(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    embedding = VectorField(dimensions=384)
    summary = models.TextField()
    topic_label = models.CharField(max_length=255)
    analyzed_at = models.DateTimeField(auto_now_add=True)
```

> You’ll need to install `pgvector` Python package: `pip install pgvector`.

---

## 🧼 Cleanup (optional)

After installation, you can delete the source code:

```cmd
cd %USERPROFILE%
rmdir /s /q pgvector
```

---

## 📚 References

* 🔗 [pgvector GitHub](https://github.com/pgvector/pgvector)
* 🔗 [PostgreSQL for Windows](https://www.postgresql.org/download/windows/)
* 🔗 [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

---

> ✅ You’re all set to run similarity search with pgvector on Windows. Happy hacking!

```

