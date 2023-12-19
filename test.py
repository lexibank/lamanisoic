def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 11676
    assert any(f["Form"] == "phet55" for f in cldf_dataset["FormTable"])


def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset["LanguageTable"])) == 41


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset["ParameterTable"])) == 301


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 1
