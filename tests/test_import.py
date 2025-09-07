def test_import_and_version():
    import attachments

    assert hasattr(attachments, "__version__")
    assert isinstance(attachments.__version__, str)
    assert attachments.__version__
