import clinical_trials_data


def test_no_module_version_attribute():
    # We don't expect the "module" to have a "__version__" attribute
    assert not hasattr(clinical_trials_data, "__version__")


def test_get_package_version():
    # We do expect the "package" to have a version associated with it
    from importlib.metadata import version

    package_version = version("clinical-trials-data")
    assert package_version is not None
