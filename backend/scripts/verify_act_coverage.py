import sys
import xml.etree.ElementTree as ET
from pathlib import Path

COVERAGE_XML = Path(__file__).resolve().parents[1] / "coverage.xml"
ACT_DIR_SNIPPET = "services/act/"
THRESHOLD = 85.0


def main() -> int:
    if not COVERAGE_XML.exists():
        print(f"coverage xml not found at {COVERAGE_XML}")
        return 1
    tree = ET.parse(str(COVERAGE_XML))
    root = tree.getroot()

    total_lines = 0
    covered_lines = 0

    for pkg in root.findall(".//packages/package"):
        for cls in pkg.findall("classes/class"):
            filename = cls.get("filename") or ""
            if ACT_DIR_SNIPPET not in filename.replace("\\", "/"):
                continue
            lines = cls.find("lines")
            if lines is None:
                continue
            for line in lines.findall("line"):
                hits = int(line.get("hits") or "0")
                total_lines += 1
                if hits > 0:
                    covered_lines += 1

    if total_lines == 0:
        print("No act folder coverage data found; failing.")
        return 1

    pct = 100.0 * covered_lines / total_lines
    print(f"Act folder coverage: {pct:.2f}% ({covered_lines}/{total_lines})")
    if pct < THRESHOLD:
        print(f"Coverage below threshold {THRESHOLD}% for act folder")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
