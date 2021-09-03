#!/usr/bin/env python

"""Tests for `openflowthrough` package."""

import time

from openflowthrough import OpenFlowThrough


def test_openflowthrough():
    usb_port = "COM5"
    oft_fsm = OpenFlowThrough(usb_port)
    assert oft_fsm.state == "idle"
    oft_fsm.safety()
    assert oft_fsm.state == "idle"

    oft_fsm.load_blank(flush_delay=2, fill_delay=1)
    assert oft_fsm.state == "blank"

    oft_fsm.conduct_measurement()
    assert oft_fsm.state == "measurement"

    measurement_duration = 1
    print("Conducting blank measurement for %d seconds" % measurement_duration)
    time.sleep(measurement_duration)

    oft_fsm.load_sample(flush_delay=1, fill_delay=1)
    assert oft_fsm.state == "sample"
    oft_fsm.conduct_measurement()
    assert oft_fsm.state == "measurement"

    print("Conducting sample measurement for %d seconds" % measurement_duration)
    time.sleep(measurement_duration)

    oft_fsm.safety()
    assert oft_fsm.state == "idle"
