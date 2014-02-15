from gui_builder import fields, forms
from wx_utils import fields as wx_fields, forms as wx_forms
import yappi

FIELDS = ["Name", "Number of Calls", "Total Time", "Sub", "Average Time"]

class ProfileActions(wx_forms.AutoSizedPanel):

 def handle_start(self):
  yappi.start()

 def handle_stop(self):
  yappi.stop()


 def handle_update_stats(self):
  stats = yappi.get_stats()
  stats.sort(self.parent.sort_field.get_index(), 1)
  func_stats = stats.func_stats[:50]
  self.parent.stats.set_items(func_stats)


 start = fields.Button(label="&Start", callback=handle_start)
 stop = fields.Button(label="St&op", callback=handle_stop)
 update_stats = fields.Button(label="&Update Statistics", callback=handle_update_stats)

class StatsList(wx_forms.SmartList):
 name = wx_fields.SmartColumn(title="name", model_field=0)
 ncalls = wx_fields.SmartColumn(title="Number of Calls", model_field=1)
 total_time = wx_fields.SmartColumn(title="Total Time", model_field=2)
 sub = wx_fields.SmartColumn(title="Sub", model_field=3)
 average_time = wx_fields.SmartColumn(title="Average Time", model_field=4)


class ProfileDialog(wx_forms.AutoSizedDialog):
 stats = StatsList(label="Stats")
 sort_order = fields.ComboBox(label="Sort", choices=FIELDS)
 actions = ProfileActions(sizer_type='horizontal')
 close = fields.ButtonSizer(close=True)