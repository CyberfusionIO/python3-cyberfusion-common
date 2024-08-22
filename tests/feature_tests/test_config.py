from cyberfusion.Common.Config import CyberfusionConfig


def test_config_get() -> None:
    config = CyberfusionConfig("custom.cfg")

    assert config.get("section", "key") == "another_value"
