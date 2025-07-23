# Complex Table Test Cases

## Basic Table with Code Blocks
|----------|----------|
| Normal text | ```python
def hello():
    print("Hello")
``` |
| More text | ```bash
echo "test"
``` |

## Table with Wrapped Content
|-------|--------------------------------------------------|
| Cell 1 | This is a cell with a lot of content that needs to be wrapped to multiple lines to fit within the column width |
| Cell 2 | Another cell with wrapped content and some `inline code` |

## Table with Mixed Content
|--------|-------------|------|
| ✅ | Working | ```python
def test():
    return True
``` |
| ❌ | Failed | ```bash
echo "error"
``` |

## Table with Empty Cells
|-------|-------|-------|
| Data 1 | | Data 3 |
| | Data 2 | |

## Table with Special Characters
|------|-------|-------|
| Test & More | 100% | Special chars: &, %, $ |
| Another | $50 | More $ and % | 