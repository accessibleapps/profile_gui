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

 def handle_clear(self):
  yappi.clear_stats()
  self.parent.stats.clear()

 start = fields.Button(label="&Start", callback=handle_start)
 stop = fields.Button(label="St&op", callback=handle_stop, enabled=False)
 clear = fields.Button(label="&Clear", callback=handle_clear)

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


class StatsPanel(wx_forms.AutoSizedPanel):

 def __init__(self, function=None, *args, **kwargs):
  super(StatsPanel, self).__init__(*args, **kwargs)
  self.function = function
  if self.function is not None:
   self.function = function
  else:
   self.function = yappi.get_func_stats

 def handle_update_stats(self):
  func_stats = self.function()
  func_stats.sort(SORT_ORDERS[self.sort_order.get_index()], 'desc')
  if len(func_stats) > 50:
   func_stats = func_stats[:50]
  self.stats.set_value(func_stats)
  self.stats.set_index(0)

 def handle_activate(self):
  item = self.stats.get_selected_model()
  if not hasattr(item, 'children'):
   item = [new_item for new_item in yappi.get_func_stats() if new_item.full_name == item.full_name][0]
  dlg = ChildrenDialog(parent=self.parent, item=item, title="Children")
  dlg.display_modal()

 def render(self):
  super(StatsPanel, self).render()
  self.stats.register_callback('item_activated', self.handle_activate)

 stats = StatsList(label="Stats")
 sort_order = fields.ComboBox(label="Sort", choices=FIELDS, read_only=True)
 update_stats = fields.Button(label="&Update Statistics", callback=handle_update_stats)

class ProfileGui(wx_forms.AutoSizedFrame):

 stats_panel = StatsPanel()

 def handle_close(self):
  self.destroy()

 actions = ProfileActions(sizer_type='horizontal')
 close = fields.Button(close=True, callback=handle_close)

class ChildrenDialog(wx_forms.AutoSizedDialog):

 def __init__(self, item=None, *args, **kwargs):
  super(ChildrenDialog, self).__init__(*args, **kwargs)
  self.stats_panel.function = lambda: item.children

 def render(self):
  super(ChildrenDialog, self).render()
  self.stats_panel.handle_update_stats()

 stats_panel = StatsPanel()
 close = fields.ButtonSizer(close=True)
