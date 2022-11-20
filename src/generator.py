import jinja2 as j2
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

def mini_calendar_dates(month, year):
  first_day = date(year, month, 1)
  current_day = first_day - timedelta(days=first_day.weekday())

  date_list = []

  while True:
    cur_month = True
    if current_day.month != month:
      cur_month = False
    date_list.append((current_day.strftime('%-d'), current_day.strftime('%Y-%m-%d'), cur_month, current_day.strftime('W%-W'), current_day.strftime('%Y-W%W')))
    if (current_day.month != month and current_day.weekday() == 6) or ((current_day + timedelta(days=1)).month != month and current_day.weekday() == 6):
      break
    current_day += timedelta(days=1)
  return date_list

def build_planner(pages, j2_env: j2.Environment):
  return j2_env.get_template('full_planner.html.j2') \
               .render(pages=pages)

def build_daily_pages(start: date, end: date, start_t: datetime, end_t: datetime, j2_env: j2.Environment):
  def build_daily_page(inp_date, j2_template: j2.Template, times):
    mini_cal = mini_calendar_dates(inp_date.month, inp_date.year)
    return j2_template.render(date=inp_date, times=times, mini_cal=mini_cal)

  num_days = (end - start).days
  num_hours = int((end_t - start_t).seconds / 60 / 60)
  day_templates = {}
  daily_template = j2_env.get_template('daily.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')

  times = [(start_t + timedelta(hours=i)).strftime('%-I %p').lower() for i in range(num_hours)]

  for i in range(num_days + 1):
    cur_date = start + timedelta(days=i)
    content = build_daily_page(cur_date, daily_template, times)
    day_templates[cur_date.strftime('%Y-%m-%d')] = frame_template.render(
      content=content,
      id=cur_date.strftime('%Y-%m-%d')
    )

  return day_templates

def build_weekly_pages(start: date, end: date, start_t: datetime, end_t: datetime, j2_env: j2.Environment):
  def build_weekly_page(inp_monday, j2_template: j2.Template, times):
    days = []
    for i in range(7):
      days.append(inp_monday + timedelta(days=i))
    return j2_template.render(days=days, times=times, mini_cal=mini_calendar_dates(inp_monday.month, inp_monday.year)) 

  cur_monday = start - timedelta(days=start.weekday())
  num_hours = int((end_t - start_t).seconds / 60 / 60) + 1
  week_templates = {}
  weekly_template = j2_env.get_template('weekly.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')

  times = [(start_t + timedelta(hours=i)).strftime('%-I').lower() for i in range(num_hours)]

  while cur_monday < end:
    content = build_weekly_page(cur_monday, weekly_template, times)
    week_templates[cur_monday.strftime('%Y-W%W')] = frame_template.render(
      content=content,
      id=cur_monday.strftime('%Y-W%W')
    )
    cur_monday += timedelta(days=7)

  return week_templates

def build_monthly_pages(start: date, end: date, j2_env: j2.Environment):
  def build_monthly_page(cur_month, j2_template: j2.Template):
    return j2_template.render(month=cur_month, mini_cal=mini_calendar_dates(cur_month.month, cur_month.year)) 

  cur_month = start + relativedelta(months=+0)
  month_templates = {}
  monthly_template = j2_env.get_template('monthly.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')

  while cur_month <= end:
    content = build_monthly_page(cur_month, monthly_template)
    month_templates[cur_month.strftime('%Y-%m')] = frame_template.render(
      content=content,
      id=cur_month.strftime('%Y-%m')
    )
    cur_month += relativedelta(months=+1)

  return month_templates


if __name__ == "__main__":
  env = j2.Environment(
    loader=j2.FileSystemLoader('./src/templates')
  )

  start_date = date(2022, 12, 26)
  end_date = date(2023, 4, 2)

  start_time = datetime(2022, 12, 26, 7, 0, 0)
  end_time = datetime(2022, 12, 26, 19, 0, 0)

  months = build_monthly_pages(date(2023, 1, 1), date(2023, 3, 1), env)
  weeks = build_weekly_pages(start_date, end_date, start_time, end_time, env)
  days = build_daily_pages(start_date, end_date, start_time, end_time, env)

  pages = list(months.values())
  pages.extend(list(weeks.values()))
  pages.extend(list(days.values()))
  planner = build_planner(pages, env)

  with open('./dest/index.html', 'w') as fp:
    fp.write(planner)
