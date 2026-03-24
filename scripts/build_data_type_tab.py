from pathlib import Path
from collections import defaultdict
import nbformat

BOOK_ROOT = Path(".")
NOTEBOOK_DIR = BOOK_ROOT / "tutorials"
OUTDIR = BOOK_ROOT / "_generated"

def is_real_notebook(nb_path):
    return (
        ".ipynb_checkpoints" not in nb_path.parts
        and not nb_path.stem.endswith("-checkpoint")
    )


def build_tabset(field, outfile, header, preferred_order=None):
    grouped = defaultdict(list)

    for nb_path in sorted(NOTEBOOK_DIR.rglob("*.ipynb")):
        if not is_real_notebook(nb_path):
            continue

        nb = nbformat.read(nb_path, as_version=4)
        meta = nb.metadata

        values = meta.get(field, [])
        if not values:
            continue

        rel_path = nb_path.with_suffix("").as_posix()
        title = meta.get(
            "title",
            nb_path.stem.replace("_", " ").replace("-", " ").title()
        )

        for val in values:
            grouped[val].append({
                "title": title,
                "path": rel_path,
            })

    # Sort entries within each tab
    for key in grouped:
        grouped[key] = sorted(grouped[key], key=lambda x: x["title"].lower())

    # Apply preferred ordering if provided
    if preferred_order:
        keys = [k for k in preferred_order if k in grouped]
        keys += sorted(k for k in grouped if k not in preferred_order)
    else:
        keys = sorted(grouped.keys())

    lines = []
    lines.append(f"{header}\n")
    lines.append("::::{tab-set}\n")

    for key in keys:
        lines.append(f":::{{tab-item}} {key}")
        for entry in grouped[key]:
            lines.append(f"- []({entry['path']})")
        lines.append(":::\n")

    lines.append("::::\n")

    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {outfile}")

build_tabset(
    field="data_types",
    outfile=OUTDIR / "data_type_tabs.md",
    header="### Looking for examples on a specific dataset?",
    preferred_order=[
        "Halo Properties",
        "Halo Lightcones",
        "Halo Particles",
        "Healpix Map",
        "Lightcone Halo Properties",
        "Diffsky Galaxies",
    ],
)

build_tabset(
    field="tasks",
    outfile=OUTDIR / "task_tabs.md",
    header="### Looking for examples by task?",
    preferred_order=[
        "Query",
        "Select",
        "Filter",
        "Add Columns",
        "Evaluate",
        "Spatial Selection",
        "Visualization",
    ],
)
