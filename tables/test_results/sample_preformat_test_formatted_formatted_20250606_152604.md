# Table Formatter Test Cases

## Simple Table

| -------- | ----- | ----------- |
| -------- | ----- | ----------- |
| Alice    | 30    | New York    |
| Bob      | 25    | San Diego   |

## Table with Code Block

| ---------- | --------- |
| ---------- | --------- |
| add        | ```python |
def add(a, b):
    return a + b
``` |
| sub      | ```python
def sub(a, b):
    return a - b
``` |

## Table with Multi-line Cell

|--------|----------------------------|
| Apple  | A fruit.
Red or green.     |
| Banana | A yellow fruit.
Soft inside.   |

## Minimal Table

| --- |
| --- |
| 1   |
| 2   |

## Table with Empty Cells

| --- | --- | --- |
| --- | --- | --- |
| 1   |     | 3   |
|     | 2   |     |

## Table with Status Column

| -------- | ---------- |
| -------- | ---------- |
| Task 1   | Complete   |
| Task 2   | Pending    |

## Table with Long Content

| ---- | -------                                                                |
| --- | ---------------------------------------------------------------------- |
| 1   | This is a very long note that should test how the formatter handles wrapping or truncation in a single cell. |
| 2   | Short note.                                                            |