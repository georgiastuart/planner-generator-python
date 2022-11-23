import jinja2 as j2
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from playwright.sync_api import sync_playwright
from os.path import abspath
from argparse import ArgumentParser

AREAS_OF_FOCUS = [
  ('Personal Growth', 'fa-solid fa-brain'),
  ('Relationships', 'fa-solid fa-heart'),
  ('Health & Wellness', 'fa-solid fa-dumbbell'),
  ('Household Management', 'fa-solid fa-house'),
]

def generate_html(planner_html, out_file):
  with open(out_file, 'w') as fp:
    fp.write(planner_html)

def generate_pdf(html_file, css_file, out_file):
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{abspath(html_file)}")
    page.add_style_tag(path=abspath(css_file))
    page.pdf(path=abspath(out_file), width='18.83in', height='11.77in')
    browser.close()

def mini_calendar_dates(month, year):
  first_day = date(year, month, 1)
  current_day = first_day - timedelta(days=first_day.weekday())

  date_list = []

  while True:
    cur_month = True
    if current_day.month != month:
      cur_month = False
    date_list.append((current_day.strftime('%-d'), current_day.strftime('%Y-%m-%d'), cur_month, current_day.strftime('W%-W'), current_day.strftime('%Y-W%W'), first_day.strftime('%B').lower(), first_day.strftime('%Y-%m')))
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
      id=cur_monday.strftime('%Y-W%W'),
      goal_link=f"{cur_monday.strftime('%Y-W%W')}-goals",
      work_goal_link=f"{cur_monday.strftime('%Y-W%W')}-work-goals"
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
      id=cur_month.strftime('%Y-%m'),
      goal_link=f"{cur_month.strftime('%Y-%m')}-goals",
      work_goal_link=f"{cur_month.strftime('%Y-%m')}-work-goals"
    )
    cur_month += relativedelta(months=+1)

  return month_templates

def build_annual_pages(start_year, end_year, j2_env: j2.Environment):
  def build_annual_page(year, j2_template: j2.Template):
    mini_cal_list = []
    for i in range(12):
      mini_cal_list.append(mini_calendar_dates(i + 1, year))
    return j2_template.render(year=year, mini_cal_list=mini_cal_list)

  annual_template = j2_env.get_template('annual_overview.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  annual_templates = {}

  for year in range(start_year, end_year + 1):
    content = build_annual_page(year, annual_template)
    annual_templates[str(year)] = frame_template.render(
      content=content,
      id=str(year),
      goal_link=f'{year}-goals'
    )

  return annual_templates

def build_annual_goal_pages(start_year, end_year, j2_env: j2.Environment):
  def build_annual_goal_page(year, j2_template: j2.Template):
    return j2_template.render(year=year, areas_of_focus=AREAS_OF_FOCUS)

  annual_template = j2_env.get_template('annual_goals.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  annual_templates = {}

  for year in range(start_year, end_year + 1):
    content = build_annual_goal_page(year, annual_template)
    annual_templates[str(year)] = frame_template.render(
      content=content,
      id=f'{year}-goals'
    )

  return annual_templates

def build_monthly_goal_pages(start, end, j2_env: j2.Environment):
  def build_monthly_goal_page(first, j2_template: j2.Template):
    return j2_template.render(first=first, areas_of_focus=AREAS_OF_FOCUS)

  annual_template = j2_env.get_template('monthly_goals.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  monthly_templates = {}
  cur_month = start + relativedelta(months=+0)


  while cur_month <= end:
    content = build_monthly_goal_page(cur_month, annual_template)
    monthly_templates[f"{cur_month.strftime('%Y-%m')}-goals"] = frame_template.render(
      content=content,
      id=f"{cur_month.strftime('%Y-%m')}-goals"
    )
    cur_month += relativedelta(months=+1)

  return monthly_templates

def build_weekly_goal_pages(start, end, j2_env: j2.Environment):
  def build_monthly_goal_page(first, j2_template: j2.Template):
    return j2_template.render(first=first, last=first+relativedelta(days=6), areas_of_focus=AREAS_OF_FOCUS)

  weekly_template = j2_env.get_template('weekly_goals.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  weekly_templates = {}
  cur_week = start + relativedelta(weeks=+0)


  while cur_week < end:
    content = build_monthly_goal_page(cur_week, weekly_template)
    weekly_templates[f"{cur_week.strftime('%Y-W%W')}-goals"] = frame_template.render(
      content=content,
      id=f"{cur_week.strftime('%Y-W%W')}-goals"
    )
    cur_week += relativedelta(weeks=+1)

  return weekly_templates

def build_monthly_work_goal_pages(start, end, j2_env: j2.Environment):
  def build_monthly_goal_page(first, j2_template: j2.Template):
    return j2_template.render(first=first)

  monthly_template = j2_env.get_template('monthly_work_goals.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  monthly_templates = {}
  cur_month = start + relativedelta(months=+0)


  while cur_month <= end:
    content = build_monthly_goal_page(cur_month, monthly_template)
    monthly_templates[f"{cur_month.strftime('%Y-%m')}-work-goals"] = frame_template.render(
      content=content,
      id=f"{cur_month.strftime('%Y-%m')}-work-goals"
    )
    cur_month += relativedelta(months=+1)

  return monthly_templates

def build_weekly_work_goal_pages(start, end, j2_env: j2.Environment):
  def build_weekly_work_goal_page(first, j2_template: j2.Template):
    return j2_template.render(first=first, last=first+relativedelta(days=6))

  weekly_template = j2_env.get_template('weekly_work_goals.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  weekly_templates = {}
  cur_week = start + relativedelta(weeks=+0)


  while cur_week < end:
    content = build_weekly_work_goal_page(cur_week, weekly_template)
    weekly_templates[f"{cur_week.strftime('%Y-W%W')}-work-goals"] = frame_template.render(
      content=content,
      id=f"{cur_week.strftime('%Y-W%W')}-work-goals"
    )
    cur_week += relativedelta(weeks=+1)

  return weekly_templates

if __name__ == "__main__":
  parser = ArgumentParser(prog='Python Planner Generator',
                          description='GoodNotes 5 Optimized PDF Planner')

  parser.add_argument('start', help='Start date in YYYY-MM-DD format')
  parser.add_argument('end', help='End date in YYYY-MM-DD format')
  parser.add_argument('--start-time', default=7, help='Start hour for daily agenda (24 hour time)')
  parser.add_argument('--end-time', default=19, help='End hour for daily agenda (24 hour time)')
  parser.add_argument('--file-suffix', default='', help='Suffix to add to output file names')

  args = parser.parse_args()


  env = j2.Environment(
    loader=j2.FileSystemLoader('./src/templates')
  )

  # start_date = date(2022, 10, 31)
  # end_date = date(2023, 1, 1)
  start_date = date.fromisoformat(args.start)
  end_date = date.fromisoformat(args.end)

  start_time = datetime(2022, 12, 26, args.start_time, 0, 0)
  end_time = datetime(2022, 12, 26, args.end_time, 0, 0)

  annuals = build_annual_pages(start_date.year, end_date.year, env)
  months = build_monthly_pages(start_date, end_date, env)
  weeks = build_weekly_pages(start_date, end_date, start_time, end_time, env)
  days = build_daily_pages(start_date, end_date, start_time, end_time, env)
  annual_goals = build_annual_goal_pages(start_date.year, end_date.year, env)
  monthly_goals = build_monthly_goal_pages(start_date, end_date, env)
  weekly_goals = build_weekly_goal_pages(start_date, end_date, env)
  monthly_work_goals = build_monthly_work_goal_pages(start_date, end_date, env)
  weekly_work_goals = build_weekly_work_goal_pages(start_date, end_date, env)


  pages = list(annuals.values())
  pages.extend(list(months.values()))
  pages.extend(list(weeks.values()))
  pages.extend(list(days.values()))
  pages.extend(list(annual_goals.values()))
  pages.extend(list(monthly_goals.values()))
  pages.extend(list(weekly_goals.values()))
  pages.extend(list(monthly_work_goals.values()))
  pages.extend(list(weekly_work_goals.values()))

  planner = build_planner(pages, env)

  generate_html(planner, f'./dest/index{args.file_suffix}.html')
  generate_pdf(f'dest/index{args.file_suffix}.html', f'dest/main.css', f'dest/planner{args.file_suffix}.pdf')
