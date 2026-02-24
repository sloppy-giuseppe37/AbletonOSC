from . import client, wait_one_tick, TICK_DURATION
import pytest

#--------------------------------------------------------------------------------
# These tests assume an Ableton Live set with at least one return track.
#--------------------------------------------------------------------------------


def test_song_get_num_return_tracks(client):
    result = client.query("/live/song/get/num_return_tracks")
    assert result is not None
    assert isinstance(result[0], int)
    assert result[0] >= 1


def test_song_get_return_track_names(client):
    result = client.query("/live/song/get/return_track_names")
    assert result is not None
    assert len(result) >= 1
    for name in result:
        assert isinstance(name, str)


def test_return_get_name(client):
    result = client.query("/live/return/get/name", [0])
    assert result is not None
    assert result[0] == 0
    assert isinstance(result[1], str)


def test_return_set_name(client):
    # Get original name
    original = client.query("/live/return/get/name", [0])
    original_name = original[1]

    # Set a new name
    client.send_message("/live/return/set/name", [0, "TestReturn"])
    wait_one_tick()

    result = client.query("/live/return/get/name", [0])
    assert result[1] == "TestReturn"

    # Restore original name
    client.send_message("/live/return/set/name", [0, original_name])
    wait_one_tick()


def test_return_get_set_volume(client):
    result = client.query("/live/return/get/volume", [0])
    assert result is not None
    assert result[0] == 0
    original_volume = result[1]
    assert isinstance(original_volume, float)

    client.send_message("/live/return/set/volume", [0, 0.5])
    wait_one_tick()

    result = client.query("/live/return/get/volume", [0])
    assert abs(result[1] - 0.5) < 0.01

    # Restore
    client.send_message("/live/return/set/volume", [0, original_volume])
    wait_one_tick()


def test_return_get_set_panning(client):
    result = client.query("/live/return/get/panning", [0])
    assert result is not None
    assert result[0] == 0
    original_panning = result[1]
    assert isinstance(original_panning, float)

    client.send_message("/live/return/set/panning", [0, 0.25])
    wait_one_tick()

    result = client.query("/live/return/get/panning", [0])
    assert abs(result[1] - 0.25) < 0.01

    # Restore
    client.send_message("/live/return/set/panning", [0, original_panning])
    wait_one_tick()


def test_return_get_set_mute(client):
    result = client.query("/live/return/get/mute", [0])
    assert result is not None
    original_mute = result[1]

    client.send_message("/live/return/set/mute", [0, 1])
    wait_one_tick()
    result = client.query("/live/return/get/mute", [0])
    assert result[1] == 1

    client.send_message("/live/return/set/mute", [0, 0])
    wait_one_tick()
    result = client.query("/live/return/get/mute", [0])
    assert result[1] == 0

    # Restore
    client.send_message("/live/return/set/mute", [0, original_mute])
    wait_one_tick()


def test_return_get_set_solo(client):
    result = client.query("/live/return/get/solo", [0])
    assert result is not None
    original_solo = result[1]

    client.send_message("/live/return/set/solo", [0, 1])
    wait_one_tick()
    result = client.query("/live/return/get/solo", [0])
    assert result[1] == 1

    client.send_message("/live/return/set/solo", [0, 0])
    wait_one_tick()
    result = client.query("/live/return/get/solo", [0])
    assert result[1] == 0

    # Restore
    client.send_message("/live/return/set/solo", [0, original_solo])
    wait_one_tick()


def test_return_get_num_devices(client):
    result = client.query("/live/return/get/num_devices", [0])
    assert result is not None
    assert result[0] == 0
    assert isinstance(result[1], int)


def test_return_get_devices_name(client):
    num_result = client.query("/live/return/get/num_devices", [0])
    if num_result[1] > 0:
        result = client.query("/live/return/get/devices/name", [0])
        assert result is not None
        assert result[0] == 0
        # Rest of the tuple should be device names
        for name in result[1:]:
            assert isinstance(name, str)


def test_return_invalid_index(client):
    """Out-of-bounds return track index should return None (no crash)."""
    result = client.query("/live/return/get/name", [999], timeout=1.0)
    assert result is None
