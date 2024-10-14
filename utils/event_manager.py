"""
EventManager: Manages event bindings and handling for the application.
"""

import wx

class EventManager:
    PROBLEM_DEFINED = wx.NewEventType()
    PROBLEM_GENERATED = wx.NewEventType()
    SOLUTION_GENERATED = wx.NewEventType()

    def __init__(self, parent_frame, ui_manager):
        self.parent_frame = parent_frame
        self.ui_manager = ui_manager
        self.event_handlers = {}
        self.problem_generated = False
        self.solution_generated = False

    def bind(self, event_type, handler):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        self.parent_frame.Bind(wx.PyEventBinder(event_type), self._on_event)

    def emit(self, event_type, data=None):
        event = wx.PyCommandEvent(event_type)
        if data:
            for k, v in data.items():
                setattr(event, k, v)
        wx.PostEvent(self.parent_frame, event)

        if event_type == self.PROBLEM_GENERATED:
            self.problem_generated = True
        elif event_type == self.SOLUTION_GENERATED:
            self.solution_generated = True

    def _on_event(self, event):
        event_type = event.GetEventType()
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                handler(event)

    def bind_ui_events(self):
        self.ui_manager.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)

    def on_page_changed(self, event):
        new = event.GetSelection()
        event.Skip()

    def enable_greedy_solution(self):
        self.ui_manager.get_tab("Greedy Solution").enable_generate_button()

    def update_contractor_schedule(self, schedule):
        self.ui_manager.get_tab("Contractor Schedules").update_schedule(schedule)
