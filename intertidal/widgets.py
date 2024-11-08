from django.forms import SelectDateWidget
from partial_date import PartialDate
from django_select2.forms import Select2TagWidget, Select2MultipleWidget, Select2AdminMixin

# see: https://github.com/ktowen/django_partial_date/issues/6#issuecomment-2107085570
class PartialDateWidget(SelectDateWidget):
  def get_context(self, name, value, attrs):
      # reorder the subwidgets to year, month, day
      context = super().get_context(name, value, attrs)
      m, d, y = context["widget"]["subwidgets"]
      context["widget"]["subwidgets"] = [y, m, d]
      return context

  def format_value(self, value):
      # convert PartialDate to dict for SelectDateWidget
      if isinstance(value, PartialDate):
          return {
              "year": value.date.year,
              "month": value.date.month if value.precision >= PartialDate.MONTH else None,
              "day": value.date.day if value.precision == PartialDate.DAY else None,
          }
      return {"year": None, "month": None, "day": None}

  def value_from_datadict(self, data, files, name):
      # build a PartialDate from the separate fields
      y = data.get(self.year_field % name)
      m = data.get(self.month_field % name)
      d = data.get(self.day_field % name)
      if y == m == d == "":
          return None

      # build the date string
      value = y
      if m:
          value += f"-{m}"
      if m and d:
          value += f"-{d}"

      return value

class Select2TagArrayWidget(Select2AdminMixin, Select2TagWidget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {
            "data-allow-clear": False,
            "data-token-separators": '|',
            "data-width": '500px',
        }
        default_attrs.update(base_attrs)
        return super().build_attrs(default_attrs, extra_attrs=extra_attrs)

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return "|".join(values)

    def optgroups(self, name, value, attrs=None):
        values = value[0].split('|') if value[0] else []
        selected = set(values)
        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
        return [(None, subgroup, 0)]

class Select2ChoiceArrayWidget(Select2AdminMixin, Select2MultipleWidget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {
            "data-allow-clear": False,
            "data-minimum-input-length": 0,
            "data-token-separators": '[",", " "]',
            "data-width": '500px',
        }
        default_attrs.update(base_attrs)
        return super().build_attrs(default_attrs, extra_attrs=extra_attrs)

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ",".join(values)

    def optgroups(self, name, value, attrs=None):
        values = value[0].split('|') if value[0] else []
        return super().optgroups(name, values, attrs=attrs)