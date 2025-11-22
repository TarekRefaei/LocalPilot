from app.core.config import settings


def test_act_settings_defaults():
    assert settings.act_apply_safety == "strict"
    assert settings.act_autoapprove_safe_creates is True
    assert settings.act_autoapprove_config_files is False
    assert settings.act_approval_timeout_seconds == 300
