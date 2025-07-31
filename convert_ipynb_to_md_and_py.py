# -*- coding: utf-8 -*-
"""Script de conversão simples para README.ipynb.

Gera README.md e README.py sem depender de pacotes externos.
"""

import json
from pathlib import Path
from typing import List


def read_ipynb(path: Path) -> List[dict]:
    with path.open('r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data.get('cells', [])


def convert_to_md(cells: List[dict]) -> str:
    lines = []
    for cell in cells:
        if cell.get('cell_type') == 'markdown':
            lines.extend(cell.get('source', []))
            lines.append("\n")
        elif cell.get('cell_type') == 'code':
            lines.append('```python\n')
            lines.extend(cell.get('source', []))
            lines.append('\n```\n')
    return ''.join(lines)


def convert_to_py(cells: List[dict]) -> str:
    lines = ["# -*- coding: utf-8 -*-\n"]
    count = 1
    for cell in cells:
        if cell.get('cell_type') == 'code':
            lines.append(f"# In[{count}]\n")
            lines.extend(cell.get('source', []))
            lines.append('\n')
            count += 1
    return ''.join(lines)


def main() -> None:
    ipynb_path = Path('README.ipynb')
    cells = read_ipynb(ipynb_path)
    Path('README.md').write_text(convert_to_md(cells), encoding='utf-8')
    Path('README.py').write_text(convert_to_py(cells), encoding='utf-8')


if __name__ == '__main__':
    main()
