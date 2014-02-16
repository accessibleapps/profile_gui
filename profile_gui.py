from gui_builder import fields, forms
from wx_utils import fields as wx_fields, forms as wx_forms
import yappi

FIELDS = ["Name", "Number of Calls", "Total Time", "Sub", "Average Time"]
SORT_ORDERS = ["name", "callcount", "totaltime", "subtime", "avgtime"]

class ProfileActions(wx_forms.AutoSizedPanel):

 def handle_start(self):
  yappi.start()
  self.start.disable()
  self.stop.enable()

 def handle_stop(self):
  yappi.stop()
  self.start.enable()
  self.stop.disable()

 def handle_update_stats(self):
  func_stats = yappi.get_func_stats()
  func_stats.sort(SORT_ORDERS[self.parent.sort_order.get_index()], 'desc')
  if len(func_stats) > 50:
   func_stats = func_stats[:50]
  self.parent.stats.set_value(func_stats)
  self.parent.stats.set_index(0)

 start = fields.Button(label="&Start", callback=handle_start)
 stop = fields.Button(label="St&op", callback=handle_stop, enabled=False)
 update_stats = fields.Button(label="&Update Statistics", callback=handle_update_stats)

 def render(self, *args, **kwargs):
  super(ProfileActions, self).render(*args, **kwargs)
  if yappi.is_running():
   self.start.disable()
   self.stop.enable()

class StatsList(wx_forms.SmartList):
 name = wx_fields.SmartColumn(title="name", model_field='name')
 ncalls = wx_fields.SmartColumn(title="Number of Calls", model_field='nactualcall')
 total_time = wx_fields.SmartColumn(title="Total Time", model_field='ttot')
 sub = wx_fields.SmartColumn(title="Sub", model_field='tsub')
 average_time = wx_fields.SmartColumn(title="Average Time", model_field='tavg')


class ProfileGui(wx_forms.AutoSizedFrame):

 def handle_close(self):
  self.destroy()

 stats = StatsList(label="Stats")
 sort_order = fields.ComboBox(label="Sort", choices=FIELDS, read_only=True)
 actions = ProfileActions(sizer_type='horizontal')
 close = fields.Button(close=True, callback=handle_close)
