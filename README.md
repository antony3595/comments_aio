### Запуск линтера "black"
```black --config .black --check --target-version py310 --diff ./```

### Запуск линтера "MyPy"
```mypy --ignore-missing-imports ./```

### Запуск логов
```python -m cli.logs http news```