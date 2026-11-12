import json

from validate_data import main


def run_validator(monkeypatch, file_path):
    monkeypatch.setattr("sys.argv", ["validate_data.py", str(file_path)])
    return main()


def test_valid_json_array(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "products.json"
    file_path.write_text(
        json.dumps([{
            "product_id": "P001",
            "product_name": "Laptop",
            "price": 50000,
            "category": "Electronics",
        }]),
        encoding="utf-8",
    )

    assert run_validator(monkeypatch, file_path) == 0
    assert "Data validation PASSED" in capsys.readouterr().out


def test_single_product_object(tmp_path, monkeypatch):
    file_path = tmp_path / "product.json"
    file_path.write_text(
        json.dumps({
            "product_id": "P001",
            "product_name": "Laptop",
            "price": 50000,
            "category": "Electronics",
        }),
        encoding="utf-8",
    )

    assert run_validator(monkeypatch, file_path) == 0


def test_invalid_json(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json}", encoding="utf-8")

    assert run_validator(monkeypatch, file_path) == 2
    assert "Unable to read valid JSON" in capsys.readouterr().out


def test_empty_json_array(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")

    assert run_validator(monkeypatch, file_path) == 1
    assert "expected a non-empty JSON" in capsys.readouterr().out


def test_missing_file(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "missing.json"

    assert run_validator(monkeypatch, file_path) == 2
    assert "Unable to read valid JSON" in capsys.readouterr().out


def test_invalid_product_record(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "invalid_product.json"
    file_path.write_text(
        json.dumps([{
            "product_id": "P001",
            "product_name": "",
            "price": -100,
            "category": "Electronics",
        }]),
        encoding="utf-8",
    )

    assert run_validator(monkeypatch, file_path) == 1

    output = capsys.readouterr().out
    assert "Record 1" in output
    assert "Data validation FAILED" in output


def test_wrong_number_of_arguments(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["validate_data.py"])

    assert main() == 2
    assert "Usage:" in capsys.readouterr().out
