#!/usr/bin/env python

"""Tests for `open_flow_through` package."""

import time

from open_flow_through import OpenFlowThrough


def test_preconditioner():
    usb_port = "COM5"
    preconditioner_fsm = OpenFlowThrough(usb_port)
    assert preconditioner_fsm.state == "idle"
    preconditioner_fsm.safety()
    assert preconditioner_fsm.state == "idle"

    preconditioner_fsm.load_blank(flush_delay=2, fill_delay=1)
    assert preconditioner_fsm.state == "blank"

    preconditioner_fsm.conduct_measurement()
    assert preconditioner_fsm.state == "measurement"

    measurement_duration = 1
    print("Conducting blank measurement for %d seconds" % measurement_duration)
    time.sleep(measurement_duration)

    preconditioner_fsm.load_sample(flush_delay=1, fill_delay=1)
    assert preconditioner_fsm.state == "sample"
    preconditioner_fsm.conduct_measurement()
    assert preconditioner_fsm.state == "measurement"

    print("Conducting sample measurement for %d seconds" % measurement_duration)
    time.sleep(measurement_duration)

    preconditioner_fsm.safety()
    assert preconditioner_fsm.state == "idle"
