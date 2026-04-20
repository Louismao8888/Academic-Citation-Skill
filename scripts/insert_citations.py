# -*- coding: utf-8 -*-
"""
insert_citations.py — CLI wrapper around docx_utils.py

Usage:
    python insert_citations.py <input.docx> <output.docx> <plan.json>

plan.json format:
{
  "insertions": [
    {
      "target": "text substring to search for",
      "marker": "[1]",
      "occurrence": 1
    }
  ],
  "references": [
    "[1] HOCHREITER S, SCHMIDHUBER J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.",
    "[2] VASWANI A, et al. Attention is all you need[C]//NeurIPS. 2017: 5998-6008."
  ],
  "options": {
    "font_name": "Times New Roman",
    "font_name_cn": "宋体",
    "font_size_pt": 10.5
  }
}
"""

import sys
import json
import io

# Fix stdout encoding for Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from pathlib import Path

# Allow running from any directory
script_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(script_dir))

from scripts.docx_utils import insert_citation_in_doc, append_references
from docx import Document


def main():
    if len(sys.argv) != 4:
        print("Usage: python insert_citations.py <input.docx> <output.docx> <plan.json>")
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    plan_path = Path(sys.argv[3])

    if not src.exists():
        print(f"ERROR: input file not found: {src}")
        sys.exit(1)

    with open(plan_path, encoding="utf-8") as f:
        plan = json.load(f)

    doc = Document(str(src))

    options = plan.get("options", {})
    font_name = options.get("font_name", "Times New Roman")
    font_name_cn = options.get("font_name_cn", "宋体")
    font_size_pt = options.get("font_size_pt", 10.5)

    # --- Insert citation markers ---
    insertions = plan.get("insertions", [])
    ok_count = 0
    fail_targets = []

    for item in insertions:
        target = item["target"]
        marker = item["marker"]
        occurrence = item.get("occurrence", 1)

        success = insert_citation_in_doc(doc, target, marker, occurrence)
        if success:
            print(f"  OK  {marker} → after: {target[:50]}{'…' if len(target)>50 else ''}")
            ok_count += 1
        else:
            print(f"  MISS {marker}: target not found — {target[:60]}")
            fail_targets.append((marker, target))

    print(f"\nInserted: {ok_count}/{len(insertions)} markers")

    # --- Append reference list ---
    references = plan.get("references", [])
    if references:
        append_references(
            doc,
            references,
            font_name=font_name,
            font_name_cn=font_name_cn,
            font_size_pt=font_size_pt,
        )
        print(f"Appended {len(references)} reference entries")

    # --- Save ---
    dst.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(dst))
    print(f"\nSaved → {dst}")

    if fail_targets:
        print("\nFailed insertions (check target substrings):")
        for marker, t in fail_targets:
            print(f"  {marker}: {t}")
        sys.exit(2)


if __name__ == "__main__":
    main()
