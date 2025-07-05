import csv
import subprocess
import sys

def test_json_to_csv(tmp_path):
    # 1. Create a tiny JSON file
    inp = tmp_path / "in.json"
    inp.write_text('[{"foo":1,"bar":2}]', encoding="utf-8")

    # 2. Run your converter
    out = tmp_path / "out.csv"
    subprocess.run(
        [sys.executable, "json2csv.py", str(inp), str(out)],
        check=True
    )

    # 3. Assert the CSV was created and has the right contents
    assert out.exists()
    reader = list(csv.DictReader(open(out, encoding="utf-8")))
    assert reader == [{"foo": "1", "bar": "2"}]
