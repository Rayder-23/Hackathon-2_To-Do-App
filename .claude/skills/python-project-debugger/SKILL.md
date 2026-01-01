---
name: python-project-debugger
description: This skill should be used when debugging Python import errors, module not found errors, path configuration issues, and other Python project structure problems. Provides systematic diagnosis and resolution of Python project setup issues.
---

# Python Project Debugger Skill

## Purpose

This skill provides systematic debugging and resolution of Python import errors, module not found errors, path configuration issues, and other Python project structure problems. The skill helps identify and fix common Python project setup issues that prevent successful execution.

## When to Use This Skill

Use this skill when encountering:
- ModuleNotFoundError or ImportError exceptions
- "No module named X" errors during import
- Python path configuration issues in multi-directory projects
- Import problems when running Python applications from different directories
- Virtual environment or uv-related import issues
- Project structure configuration problems that affect module discovery

## How to Use This Skill

### Phase 1: Problem Diagnosis

1. **Identify the specific error message**
   - Note the exact ModuleNotFoundError or ImportError
   - Identify which module cannot be found
   - Note the current working directory when the error occurs

2. **Analyze the project structure**
   - Map the directory structure of the project
   - Identify where the problematic module is located
   - Determine the intended import path vs. actual path

3. **Check Python path configuration**
   - Examine sys.path to see available import paths
   - Verify if the intended module directory is included
   - Check for __init__.py files in relevant directories

### Phase 2: Common Solutions

1. **Fix Python path issues**
   ```python
   import sys
   import os
   from pathlib import Path

   # Add the parent directory or src directory to Python path
   project_root = Path(__file__).parent
   src_path = project_root / "src"  # or appropriate path
   sys.path.insert(0, str(src_path))
   ```

2. **Verify __init__.py files**
   - Ensure all directories in the import path contain __init__.py files
   - This includes the package directory and any parent directories
   - Empty __init__.py files are sufficient

3. **Use relative imports appropriately**
   - For modules within the same package, use relative imports
   - Example: `from . import module_name` or `from ..package import module_name`

4. **Install as editable package**
   - For development: `pip install -e .` in the project directory
   - This makes the package available system-wide during development

### Phase 3: Advanced Troubleshooting

1. **Virtual environment verification**
   - Ensure the correct virtual environment is activated
   - Verify packages are installed in the active environment
   - Check that the Python interpreter is from the virtual environment

2. **uv-specific considerations**
   - Verify pyproject.toml has correct package configuration
   - Check that [tool.setuptools.packages.find] or similar is properly configured
   - Ensure the source directory is correctly specified in build configuration

3. **Package installation verification**
   - Check if the package is properly installed with `pip list`
   - Verify the installation path with `pip show package-name`
   - Confirm the package location in site-packages

### Phase 4: Validation

1. **Test the fix**
   - Run the application to confirm the import error is resolved
   - Verify all related imports work correctly
   - Test from different execution contexts if applicable

2. **Document the solution**
   - Add comments explaining any sys.path modifications
   - Update README or documentation if the fix is project-specific
   - Consider adding a setup.py or pyproject.toml if missing

## Common Patterns and Solutions

### Pattern 1: Multi-directory project structure
**Problem**: `from package.module import function` fails when package is in subdirectory
**Solution**: Add the parent directory of the package to sys.path before import

### Pattern 2: Backend/src structure
**Problem**: Running from project root, imports like `from todo.cli import TodoCLI` fail
**Solution**: Insert backend/src into sys.path: `sys.path.insert(0, str(Path(__file__).parent / "src"))`

### Pattern 3: Missing __init__.py files
**Problem**: Directory structure exists but Python doesn't recognize it as a package
**Solution**: Add empty __init__.py files to all directories in the import path

## Prevention Strategies

1. **Consistent project structure**: Use standard Python project layouts (src/package/ or package/)
2. **Early path configuration**: Set up Python path in main entry points
3. **Virtual environment setup**: Use proper virtual environment configuration
4. **Build system configuration**: Configure pyproject.toml or setup.py for complex projects
5. **Testing from multiple contexts**: Test imports from different execution directories