from platform_core.checkpoint import CommitCheckpoint

def test_checkpoint_is_not_advanced_until_saved(tmp_path):
    c = CommitCheckpoint(tmp_path / "checkpoint.json")
    assert c.load() is None
    c.save_after_publish("001")
    assert c.load() == "001"
