# Used in conjunction with main_frame_controller.MainFrameController

import wx

class EventManager:
    def __init__(self, parent_frame, ui_manager):
        self.parent_frame = parent_frame
        self.ui_manager = ui_manager

    def bind_events(self):
        self.ui_manager.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)

    def on_page_changed(self, event):
        new = event.GetSelection()
        event.Skip()

        if new == 2 and not hasattr(self.ui_manager.get_tab("Problem Generation"), 'contractors'):
            wx.MessageBox("Warning: A problem has not been generated yet. Some features may not be available.", "Warning", wx.OK | wx.ICON_WARNING)
        elif new == 3 and not hasattr(self.ui_manager.get_tab("Greedy Solution"), 'schedule'):
            wx.MessageBox("Warning: A greedy solution has not been generated yet. Some features may not be available.", "Warning", wx.OK | wx.ICON_WARNING)

    def enable_greedy_solution(self):
        self.ui_manager.get_tab("Greedy Solution").enable_generate_button()

    def update_contractor_schedule(self, schedule):
        self.ui_manager.get_tab("Contractor Schedules").update_schedule(schedule)
