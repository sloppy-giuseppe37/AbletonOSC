from typing import Tuple, Any
from .handler import AbletonOSCHandler


class LooperDeviceHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "looper"

    def init_api(self):
        self._register_looper_handlers("/live/looper", self.song.tracks)
        self._register_looper_handlers("/live/return/looper", self.song.return_tracks)

    def _register_looper_handlers(self, prefix: str, track_list):
        def create_looper_callback(func, *args, include_ids: bool = False):
            def looper_callback(params: Tuple[Any]):
                track_index, device_index = int(params[0]), int(params[1])
                if track_index < 0 or track_index >= len(track_list):
                    self.logger.warning("Invalid track index: %d" % track_index)
                    return None
                device = track_list[track_index].devices[device_index]
                if device.class_name != "Looper":
                    self.logger.warning("Device %d on track %d is not a Looper (class_name: %s)" %
                                        (device_index, track_index, device.class_name))
                    return None
                if include_ids:
                    rv = func(device, *args, params[0:])
                else:
                    rv = func(device, *args, params[2:])
                if rv is not None:
                    return (track_index, device_index, *rv)

            return looper_callback

        #--------------------------------------------------------------------------------
        # Property: loop_length (read-only, observable)
        #--------------------------------------------------------------------------------
        self.osc_server.add_handler("%s/get/loop_length" % prefix,
                                    create_looper_callback(self._get_property, "loop_length"))
        self.osc_server.add_handler("%s/start_listen/loop_length" % prefix,
                                    create_looper_callback(self._start_listen, "loop_length", include_ids=True))
        self.osc_server.add_handler("%s/stop_listen/loop_length" % prefix,
                                    create_looper_callback(self._stop_listen, "loop_length", include_ids=True))

        #--------------------------------------------------------------------------------
        # Methods: record, overdub, play, stop, undo, clear
        #--------------------------------------------------------------------------------
        for method in ["record", "overdub", "play", "stop", "undo", "clear"]:
            self.osc_server.add_handler("%s/%s" % (prefix, method),
                                        create_looper_callback(self._call_method, method))
