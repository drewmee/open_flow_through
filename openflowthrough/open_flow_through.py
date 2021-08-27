import json
import logging
import time

from pkg_resources import resource_filename
from pyfirmata import ArduinoNano
from transitions import Machine

log = logging.getLogger(__name__)


class OpenFlowThrough:
    def __init__(self, usb_port="/dev/arduino_nano"):
        """[summary]

        Args:
            usb_port (str, optional): [description]. Defaults to "/dev/arduino_nano".
        """
        self.duration = 10
        self.board = ArduinoNano(usb_port)
        self.pin_dict = dict(
            pump=2,
            on_off_valve=3,
            diverter_valve_1=5,
            diverter_valve_2=4,
            flow_sensor=6,
        )
        json_filepath = resource_filename(__name__, "json/fsm.json")
        with open(json_filepath, "r") as f:
            fsm_config = json.load(f)

        self.machine = Machine(model=self, send_event=True, **fsm_config)

    def load_flowcell_routine(self, measurement_type, flush_delay, fill_delay):
        """[summary]

        Args:
            measurement_type ([type]): [description]
            flush_delay ([type]): [description]
            fill_delay ([type]): [description]

        Raises:
            ValueError: [description]
        """
        print("loading %s" % measurement_type)

        self.board.digital[self.pin_dict["pump"]].write(1)
        if measurement_type == "blank":
            self.board.digital[self.pin_dict["on_off_valve"]].write(0)
            self.board.digital[self.pin_dict["diverter_valve_1"]].write(1)
            self.board.digital[self.pin_dict["diverter_valve_2"]].write(1)
        elif measurement_type == "sample":
            self.board.digital[self.pin_dict["on_off_valve"]].write(0)
            self.board.digital[self.pin_dict["diverter_valve_1"]].write(0)
            self.board.digital[self.pin_dict["diverter_valve_2"]].write(1)
        else:
            raise ValueError("measurement_type must be 'blank' or 'sample'.")

        print("flushing for %d seconds" % flush_delay)
        time.sleep(flush_delay)

        self.board.digital[self.pin_dict["on_off_valve"]].write(1)
        print("filling for %d seconds" % fill_delay)
        time.sleep(fill_delay)
        self.board.digital[self.pin_dict["diverter_valve_1"]].write(0)
        self.board.digital[self.pin_dict["diverter_valve_2"]].write(0)

    def load_blank_routine(self, event):
        flush_delay = event.kwargs.get("flush_delay", 20)
        fill_delay = event.kwargs.get("fill_delay", 10)
        self.load_flowcell_routine(
            "blank", flush_delay=flush_delay, fill_delay=fill_delay
        )

    def load_sample_routine(self, event):
        """[summary]"""
        flush_delay = event.kwargs.get("flush_delay", 10)
        fill_delay = event.kwargs.get("fill_delay", 10)
        self.load_flowcell_routine(
            "sample", flush_delay=flush_delay, fill_delay=fill_delay
        )

    def measurement_routine(self, event):
        """[summary]"""
        self.board.digital[self.pin_dict["pump"]].write(0)

        # Route flow around filter
        self.board.digital[self.pin_dict["diverter_valve_1"]].write(0)
        # Route flow  around flowcell
        self.board.digital[self.pin_dict["diverter_valve_2"]].write(0)
        # Close one-way ON/OFF valve
        self.board.digital[self.pin_dict["on_off_valve"]].write(1)

    def safety_routine(self, event):
        """[summary]"""
        self.board.digital[self.pin_dict["pump"]].write(0)

        # Route flow around filter
        self.board.digital[self.pin_dict["diverter_valve_1"]].write(0)
        # Route flow  around flowcell
        self.board.digital[self.pin_dict["diverter_valve_2"]].write(0)
        # Close one-way ON/OFF valve
        self.board.digital[self.pin_dict["on_off_valve"]].write(0)
