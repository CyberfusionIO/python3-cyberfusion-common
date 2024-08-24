from cyberfusion.Common.Config import CyberfusionConfig


def test_config_default_path() -> None:
    config = CyberfusionConfig(path=None)

    assert config.path == "/etc/cyberfusion/cyberfusion.cfg"
