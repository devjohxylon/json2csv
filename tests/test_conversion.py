import csv
import subprocess
import sys
from pathlib import Path

def test_json_to_csv(tmp_path):
    # Prepare input JSON
    inp = tmp_path / "in.json"
    inp.write_text('[{"foo":1,"bar":2}]', encoding="utf-8")

    # Run the converter
    out = tmp_path / "out.csv"
    result = subprocess.run(
        [sys.executable, "json2csv.py", str(inp), str(out)],
        capture_output=True,
        text=True,
        check=True
    )

    # Check output CSV exists
    assert out.exists(), "Converter did not produce an output file"

    # Read and validate contents
    reader = list(csv.DictReader(open(out, encoding="utf-8")))
    assert reader == [{"foo": "1", "bar": "2"}]
