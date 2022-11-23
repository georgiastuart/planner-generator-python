# Python Planner Generator

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/georgiastuart/planner-generator-python/Test%20Build%20Configurations/main)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/georgiastuart/planner-generator-python)

This code creates a digital planner (maybe printable someday) for use with the
iPad app goodnotes 5.

## Features

- An annual overview page with months, days, and optional personal / work goals hyperlinked.
- Monthly pages with weeks, days, and optional personal / work goals hyperlinked.
- Weekly pages with the month, days, and optional personal / work goals hyperlinked.
- Daily pages with a hyperlinked mini calendar and week.
- Annual/Monthly/Weekly personal goals (hyperlinked on each page with the target symbol in the bottom right corner).
- Monthly/Weekly work goals (hyperlinked with briefcase symbol in bottom right corner of monthly/weekly pages).
- Lots of hyperlinking. If it seems like it should direct to another page, it probably does.

### Screen shots

#### Annual view 

![Annual view](https://user-images.githubusercontent.com/8276147/203629183-412e0cf9-9ba0-4311-9542-54396dd96521.png)

#### Monthly view

![Monthly view](https://user-images.githubusercontent.com/8276147/203629487-03726b4c-6ef8-418c-bc34-cf41a60100f0.png)

#### Weekly view


![Weekly view](https://user-images.githubusercontent.com/8276147/203629643-d0aa6bb7-b904-4685-bf6a-ae9adc9a6a5b.png)

#### Daily view

![Daily view](https://user-images.githubusercontent.com/8276147/203629772-3317b5e0-ee10-425d-b1a4-c175b2050454.png)

#### Monthly personal goals

![Monthly personal goals](https://user-images.githubusercontent.com/8276147/203632411-63bc909a-2687-4a4e-825c-27084cdf25fd.png)

#### Weekly personal goals

![Weekly personal goals](https://user-images.githubusercontent.com/8276147/203632731-09e8f814-845d-42ab-82c5-07b39fbb858c.png)

#### Monthly work goals

![Monthly work goals](https://user-images.githubusercontent.com/8276147/203632843-0e60341f-3373-4653-9fc5-46cbc9f1e098.png)

#### Weekly work goals

![Weekly work goals](https://user-images.githubusercontent.com/8276147/203632936-8860454b-5de8-4c1d-9826-5b426bd2bee1.png)

## Using the generator locally

### Prerequisites 

- Python3 >= 3.9 
- Jinja2
- python-dateutil
- playwright (Python)
- Node / NPM

### Install

Run 

```bash
npm install
```

to install the tailwind dependency.

### Building the planner

```bash
npm run build -- <start date (YYYY-MM-DD format)> <end date (YYYY-MM-DD format)> <optional arguments> 
```

To create the PDF from the HTML output, I recommend opening `index.html` in 
Chrome and using the "Save as PDF" feature in the print menu. If using this 
technique, set margins to none and enable background images.

#### Optional Arguments 

```
usage: Python Planner Generator [-h] [--start-time START_TIME] [--end-time END_TIME] [--file-suffix FILE_SUFFIX] [--work-goals | --no-work-goals]
                                [--personal-goals | --no-personal-goals] [--daily-pages | --no-daily-pages] [--weekly-pages | --no-weekly-pages]
                                start end

GoodNotes 5 Optimized PDF Planner

positional arguments:
  start                 Start date in YYYY-MM-DD format
  end                   End date in YYYY-MM-DD format

options:
  -h, --help            show this help message and exit
  --start-time START_TIME
                        Start hour for daily agenda (24 hour time)
  --end-time END_TIME   End hour for daily agenda (24 hour time)
  --file-suffix FILE_SUFFIX
                        Suffix to add to output file names
  --work-goals, --no-work-goals
  --personal-goals, --no-personal-goals
  --daily-pages, --no-daily-pages
  --weekly-pages, --no-weekly-pages
```
