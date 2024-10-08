import wx
import wx.lib.scrolledpanel as scrolled
from typing import List, Dict, Tuple, Union
from models.customer import Customer
from models.contractor import Contractor
from models.schedule import Schedule
from utils.travel_time import calculate_travel_time
from datetime import datetime, date, timedelta
import logging
import colorsys

logger = logging.getLogger(__name__)

class GreedyScheduleVisualizerTab(scrolled.ScrolledPanel):
    def __init__(self, parent: wx.Window, main_frame) -> None:
        super().__init__(parent)
        self.main_frame = main_frame
        self.InitUI()
        self.schedule = None
        self.contractors = None
        logger.debug("GreedyScheduleVisualizerTab initialized")

    def InitUI(self) -> None:
        self.SetupScrolling(scroll_x=True, scroll_y=True, rate_x=20, rate_y=20)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        logger.debug("GreedyScheduleVisualizerTab UI initialized")

    def OnSize(self, event):
        self.Refresh()  # Redraw the panel when it's resized
        event.Skip()

    def OnPaint(self, event):
        if self.schedule and self.contractors:
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            self.DrawSchedule(dc)

    def DrawSchedule(self, dc):
        width, height = self.GetSize()
        colors = self.generate_colors(len(self.contractors))

        # Get the current scroll position
        scroll_x, scroll_y = self.GetViewStart()
        scroll_unit_x, scroll_unit_y = self.GetScrollPixelsPerUnit()
        offset_x = scroll_x * scroll_unit_x
        offset_y = scroll_y * scroll_unit_y

        # Find the earliest date and latest end time in the schedule
        start_date = min(day for day in self.schedule.assignments.keys())
        end_date = max(day for day in self.schedule.assignments.keys())
        num_days = (end_date - start_date).days + 1

        time_scale = 100  # pixels per hour
        day_width = 24 * time_scale
        label_width = 150  # Width for contractor labels
        total_width = label_width + num_days * day_width
        contractor_height = 80
        total_height = contractor_height * len(self.contractors) + 100  # Add space for day labels and legend

        self.SetVirtualSize((total_width, total_height))

        # Draw contractor labels
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        for i, contractor in enumerate(self.contractors):
            y = i * contractor_height - offset_y
            dc.SetTextForeground(colors[i])
            dc.DrawText(f'Contractor {contractor.id}', 5, int(y + contractor_height / 2 - 10))

        # Draw schedule
        for i, contractor in enumerate(self.contractors):
            y = i * contractor_height - offset_y
            prev_end_time = None
            prev_location = contractor.location
            for day, assignments in self.schedule.assignments.items():
                day_offset = (day - start_date).days
                contractor_assignments = [a for a in assignments if a[1].id == contractor.id]
                for j, (customer, assigned_contractor, start_time) in enumerate(contractor_assignments):
                    errand_duration = customer.desired_errand.base_time.total_seconds() / 3600  # Convert to hours
                    
                    travel_time, _ = calculate_travel_time(prev_location, customer.location)
                    travel_time = travel_time.total_seconds() / 3600  # Convert to hours

                    # Calculate start hour relative to the beginning of the schedule
                    start_hour = (start_time - datetime.combine(start_date, datetime.min.time())).total_seconds() / 3600
                    
                    # Draw travel time
                    if prev_end_time:
                        travel_start = max(prev_end_time, start_time - timedelta(hours=travel_time))
                        travel_start_hour = (travel_start - datetime.combine(start_date, datetime.min.time())).total_seconds() / 3600
                        travel_x1 = int(label_width + travel_start_hour * time_scale - offset_x)
                        travel_x2 = int(label_width + start_hour * time_scale - offset_x)
                        travel_color = self.lighten_color(colors[i], 0.5)  # Adjusted brightness for better visibility
                        dc.SetBrush(wx.Brush(travel_color))
                        dc.SetPen(wx.Pen(travel_color))
                        travel_rect_width = max(travel_x2 - travel_x1, 1)  # Ensure width is positive
                        dc.DrawRoundedRectangle(travel_x1, y + 5, travel_rect_width, contractor_height - 10, 5)

                    # Draw errand
                    errand_x1 = int(label_width + start_hour * time_scale - offset_x)
                    errand_x2 = int(label_width + (start_hour + errand_duration) * time_scale - offset_x)
                    dc.SetBrush(wx.Brush(colors[i]))
                    dc.SetPen(wx.Pen(colors[i]))
                    errand_rect_width = max(errand_x2 - errand_x1, 1)  # Ensure width is positive
                    dc.DrawRoundedRectangle(errand_x1, y + 5, errand_rect_width, contractor_height - 10, 5)

                    # Draw errand label
                    dc.SetTextForeground(wx.BLACK)
                    label = f'E{customer.id}'
                    text_width, text_height = dc.GetTextExtent(label)
                    dc.DrawText(label, int((errand_x1 + errand_x2) / 2 - text_width / 2), int(y + contractor_height / 2 - text_height / 2))

                    prev_end_time = start_time + timedelta(hours=errand_duration)
                    prev_location = customer.location

        # Draw day separators and labels
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 1, wx.DOT))
        for i in range(num_days):
            x = label_width + i * day_width - offset_x
            dc.DrawLine(x, 0, x, total_height - 80)
            day_date = start_date + timedelta(days=i)
            dc.DrawText(day_date.strftime('%Y-%m-%d'), x + 5, total_height - 75 - offset_y)

        # Draw legend
        legend_y = total_height - 50 - offset_y
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText("Legend:", label_width - offset_x, legend_y)
        
        # Errand color
        dc.SetBrush(wx.Brush(colors[0]))
        dc.SetPen(wx.Pen(colors[0]))
        dc.DrawRectangle(label_width + 100 - offset_x, legend_y, 20, 20)
        dc.DrawText("Errand", label_width + 130 - offset_x, legend_y)
        
        # Travel time color
        travel_color = self.lighten_color(colors[0], 0.5)
        dc.SetBrush(wx.Brush(travel_color))
        dc.SetPen(wx.Pen(travel_color))
        dc.DrawRectangle(label_width + 250 - offset_x, legend_y, 20, 20)
        dc.DrawText("Travel Time", label_width + 280 - offset_x, legend_y)

    def generate_colors(self, num_colors: int) -> List[str]:
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            saturation = 0.7
            value = 0.9
            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, saturation, value)]
            colors.append(f'#{r:02x}{g:02x}{b:02x}')
        return colors

    def lighten_color(self, color: str, factor: float = 0.7) -> str:
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return f'#{int(r + (255 - r) * factor):02x}{int(g + (255 - g) * factor):02x}{int(b + (255 - b) * factor):02x}'

    def plot_schedule(self, schedule: Schedule, contractors: List[Contractor]) -> None:
        logger.info("Plotting greedy schedule")
        try:
            self.schedule = schedule
            self.contractors = contractors
            self.Refresh()
            logger.info("Greedy schedule plotted successfully")
        except Exception as e:
            logger.error(f"Error plotting greedy schedule: {str(e)}", exc_info=True)
            wx.MessageBox(f"An error occurred while plotting the greedy schedule: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def update_visualization(self, customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> None:
        logger.info("Updating GreedyScheduleVisualizerTab visualization")
        try:
            self.plot_schedule(schedule, contractors)
            self.Layout()
            logger.info("GreedyScheduleVisualizerTab visualization updated successfully")
        except Exception as e:
            logger.error(f"Error updating GreedyScheduleVisualizerTab visualization: {str(e)}", exc_info=True)
            wx.MessageBox(f"An error occurred while updating the visualization: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)