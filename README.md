# Python Planner Generator

This code creates a digital planner (maybe printable someday) for use with the
iPad app goodnotes 5.

## Prerequisites 

- Python3 >= 3.9 
- Jinja2
- python-dateutil
- playwright (Python)
- Node / NPM

## Install

Run 

```bash
npm install
```

to install the tailwind dependency.

## Building the planner

```bash
npm run build -- <start date (YYYY-MM-DD format)> <end date (YYYY-MM-DD format)> <optional arguments> 
```

To create the PDF from the HTML output, I recommend opening `index.html` in 
Chrome and using the "Save as PDF" feature in the print menu. If using this 
technique, set margins to none and enable background images.

### Optional Arguments 

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
