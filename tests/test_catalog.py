from framework_cir.validate import validate_doc, repo_root


def test_catalog_documents_validate() -> None:
    catalog = repo_root() / "catalog"
    docs = list(catalog.glob("*.json"))
    assert docs, "catalog is empty"
    errors = []
    for path in docs:
        errors.extend(validate_doc(path))
    assert errors == []


def test_schema_exists() -> None:
    assert (repo_root() / "schema" / "cir.schema.json").is_file()
