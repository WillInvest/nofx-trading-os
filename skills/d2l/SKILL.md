# D2L Annotated Notebook Skill

Creates annotated Jupyter notebooks from D2L (Dive into Deep Learning) textbook chapters.

## Trigger

When user says: "do d2l assignment for chapter X, Y, Z" or similar

## Workflow

### 1. Setup (first time only)
```bash
# Ensure d2l source is available
cd ~/projects/d2l-assignment
git clone https://github.com/d2l-ai/d2l-en.git d2l-source 2>/dev/null || (cd d2l-source && git pull)
```

### 2. Identify Source Files
- Chapter 3: `d2l-source/chapter_linear-regression/`
- Chapter 4: `d2l-source/chapter_linear-classification/`
- Chapter 5: `d2l-source/chapter_multilayer-perceptrons/`
- Chapter 6: `d2l-source/chapter_builders-guide/`
- Chapter 7: `d2l-source/chapter_convolutional-neural-networks/`
- Chapter 8: `d2l-source/chapter_modern-convolutional-neural-networks/`
- (etc. - check `d2l-source/` for exact folder names)

Each chapter folder has multiple `.md` files. Check `index.md` for the order.

### 3. Create One Notebook Per Chapter
- Output: `Chapter_X_Title.ipynb`
- Location: `projects/d2l-assignment/`
- Kernel: "Python (d2l)"

### 4. For Each Source .md File

**Extract ALL code blocks:**
- Look for ` ```python ` fenced blocks
- Also check for `#@tab pytorch` markers (use PyTorch version)
- Include EVERY code block, in order

**Add to notebook:**
```
[Markdown Cell] ## Section Title (from .md filename/header)
[Markdown Cell] Brief explanation + 🔑 KEY INSIGHT for important concepts
[Code Cell] <actual code from source>
... repeat for all code blocks ...
```

### 5. Annotation Style
- **DO** mark genuinely important concepts with 🔑 KEY INSIGHT
- **DON'T** annotate everything - be selective
- **DO** add brief explanations before complex code
- **DON'T** rewrite the textbook - keep it concise
- **NEVER** leave placeholders like "see textbook for remaining sections" — include ALL code

### 5.1 ⚠️ Completeness Check
After creating a notebook, verify ALL source files were included:
```bash
# Count source files (excluding index.md)
ls d2l-source/chapter_X/*.md | grep -v index.md | wc -l

# Count sections in notebook (look for ## headers)
grep -c "^## " Chapter_X.ipynb  # Should roughly match
```

### 6. ⚠️ CRITICAL: Indentation
When copying Python code from markdown to notebook cells:
- Verify indentation is exactly correct (4 spaces per level)
- Pay extra attention to:
  - Class methods
  - Nested loops/conditionals
  - Multi-line function calls
  - `with` blocks
- **Run every cell** to catch IndentationError before delivering

### 7. Verify & Test

**Syntax check (run after creating notebooks):**
```python
import json, ast
nb = json.load(open('Chapter_X.ipynb'))
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        code = ''.join(cell['source'])
        # Skip IPython magic lines
        code_clean = '\n'.join(l for l in code.split('\n') if not l.strip().startswith('%'))
        if code_clean.strip():
            ast.parse(code_clean)  # Raises SyntaxError if invalid
```

**Full execution test:**
```bash
conda activate d2l
jupyter nbconvert --execute --to notebook Chapter_X_*.ipynb
```

## Output Structure

```
projects/d2l-assignment/
├── Chapter_3_Linear_Regression.ipynb
├── Chapter_4_Linear_Classification.ipynb
├── Chapter_5_Multilayer_Perceptrons.ipynb
├── Chapter_6_....ipynb  (future)
└── d2l-source/          (reference)
```

## Environment

- Conda env: `d2l`
- Key packages: torch, d2l, jupyter, matplotlib
- Activate: `conda activate d2l`
- Run notebooks: `jupyter notebook projects/d2l-assignment/`

## Example

User: "do d2l assignment for chapter 6, 7"

Action:
1. Check d2l-source for chapter 6 & 7 folders
2. Read each .md file in order (per index.md)
3. Create `Chapter_6_Builders_Guide.ipynb` with all code + annotations
4. Create `Chapter_7_CNNs.ipynb` with all code + annotations
5. Run notebooks to verify no errors
6. Report completion
