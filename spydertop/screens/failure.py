#
# failure.py
#
# Author: Griffith Thomas
# Copyright 2022 Spyderbat, Inc.  All rights reserved.
#

"""
A failure screen to alert the user that data has failed to load, and 
to allow them to recover or quit.
"""

from datetime import datetime
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.event import KeyboardEvent
from asciimatics.parsers import AsciimaticsParser

from spydertop.model import AppModel
from spydertop.widgets import Padding, FuncLabel


class FailureFrame(Frame):
    _model: AppModel

    def __init__(self, screen: Screen, model: AppModel) -> None:
        super().__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            reduce_cpu=True,
            can_scroll=False,
        )

        self._model = model

        layout = Layout([1])
        self.add_layout(layout)

        layout.add_widget(Padding((screen.height - 1) // 2 - 3))
        layout.add_widget(
            FuncLabel(
                lambda: "${1,1}Data failed to load:",
                align="^",
                parser=AsciimaticsParser(),
            )
        )
        layout.add_widget(FuncLabel(lambda: model.failure_reason, align="^"))
        layout.add_widget(
            FuncLabel(
                lambda: "What do you want to do?",
                align="^",
            )
        )
        layout.add_widget(Padding(2))

        layout2 = Layout([1])
        self.add_layout(layout2)

        layout2.add_widget(
            Button("Revert to last loaded time", lambda: self._recover())
        )
        layout2.add_widget(
            Button("Go to the earliest loaded time", lambda: self._recover())
        )
        self._time_button = Button(
            f"Load {datetime.fromtimestamp(self._model.timestamp)}",
            lambda: self._recover(),
        )
        layout2.add_widget(self._time_button)
        layout2.add_widget(Button("Quit", lambda: self._quit()))

        self.set_theme(model.config["theme"])
        self.fix()

    def update(self, frame_no):
        self.set_theme(self._model.config["theme"])
        self._time_button.text = f"Load {datetime.fromtimestamp(self._model.timestamp)}"
        super().update(frame_no)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in {ord("q"), ord("Q")}:
                self._quit()
        return super().process_event(event)

    def _recover(self):
        self._model.recover()
        raise NextScene("Main")

    @staticmethod
    def _quit():
        raise StopApplication("User quit after failure")
