from . import client, wait_one_tick, TICK_DURATION
import pytest

#--------------------------------------------------------------------------------
# These tests assume that track 0, device 0 is a Looper device.
# Adjust the indices below to match your Live set.
#--------------------------------------------------------------------------------
LOOPER_TRACK = 0
LOOPER_DEVICE = 0

# A non-Looper device for the negative test case.
NON_LOOPER_TRACK = 0
NON_LOOPER_DEVICE = 1


def test_looper_get_loop_length(client):
    result = client.query("/live/looper/get/loop_length", [LOOPER_TRACK, LOOPER_DEVICE])
    assert result[0] == LOOPER_TRACK
    assert result[1] == LOOPER_DEVICE
    assert isinstance(result[2], float)


def test_looper_record(client):
    client.send_message("/live/looper/record", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()
    # Stop immediately so we don't leave the looper in record state
    client.send_message("/live/looper/stop", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()


def test_looper_overdub(client):
    client.send_message("/live/looper/overdub", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()
    client.send_message("/live/looper/stop", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()


def test_looper_play(client):
    client.send_message("/live/looper/play", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()
    client.send_message("/live/looper/stop", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()


def test_looper_stop(client):
    client.send_message("/live/looper/stop", [LOOPER_TRACK, LOOPER_DEVICE])
    wait_one_tick()


def test_looper_non_looper_device(client):
    """Targeting a non-Looper device should return no response."""
    result = client.query("/live/looper/get/loop_length",
                          [NON_LOOPER_TRACK, NON_LOOPER_DEVICE],
                          timeout=1.0)
    assert result is None
