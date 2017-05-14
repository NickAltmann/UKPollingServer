import pandas as pd
import re
import datetime
import calendar
from collections import OrderedDict
from xlrd import open_workbook as load_workbook


def get_index(item, container):
    """Find index of item in container, returning None if not there."""
    try:
        ind = container.index(item)
    except:
        ind = None
    return ind


def get_workbook(path):
    wb = load_workbook(path)
    return wb


def get_data_tabs(wb):
    """Return list of interesting tabs from the workbook."""
    tab_pattern = "^\d\d-?(\d\d)?$"
    tabs = [x for x in wb.sheets() if re.match(tab_pattern, x.name)]
    return tabs


def end_day(ss):
    """
    Returns the end day, or None, for examples like this:
    '2', '22', '9-11', '-3', ''
    """
    pat = "^.*?(\d{1,2})$"
    try:
        m = re.match(pat, ss)
        if m:
            end_day = int(m.groups()[-1])
        else:
            end_day = None
    except:
        end_day = None
    return end_day


def get_data_from_sheet(sheet):
    interesting_cols = ['Year', 'Month', 'Fieldwork', 'Polling', 'Con', 'Lab', 'LD', 'UKIP', 'Green']
    month_map = {datetime.date(2016, x, 1).strftime("%b"): x for x in range(1, 13)}
    header_row = [sheet.cell(0, x).value for x in range(sheet.ncols)]
    ri = {x: get_index(x, header_row) for x in interesting_cols}

    year = None
    month = None
    data_list = []
    row_count = sheet.nrows
    for row in range(1, row_count):
        # Year
        yr = sheet.cell(row, ri['Year']).value
        try:
            year = int(yr) if yr and yr > 1900 else year
        except:
            pass
        if not year:
            continue

        # Month
        mn = sheet.cell(row, ri['Month']).value
        try:
            month = int(month_map[mn[:3]])
        except:
            pass

        # Get polls themselves
        data = {}
        for c in ['Con', 'Lab', 'LD', 'UKIP', 'Green']:
            ind = ri[c]
            if ind is not None:
                try:
                    val = float(sheet.cell(row, ind).value)
                except:
                    val = 0
            else:
                val = 0
            data[c] = val

        # Skip if they don't look populated
        if not (data['Con'] and data['Lab'] and data['LD']):
            continue

        # If we reach the election result we're done
        org = sheet.cell(row, ri['Polling']).value
        if org and org.strip().lower().startswith("result"):
            break
        data['Pollster'] = org.lower().strip()

        # If we've reached exit polls we're done
        fieldwork = sheet.cell(row, ri['Fieldwork']).value
        if fieldwork and "exit" in str(fieldwork).lower():
            break

        # Day
        day = end_day(fieldwork)

        if day:
            poll_date = datetime.date(year, month, day)
        else:
            month_span = calendar.monthrange(year, month)
            poll_date = datetime.date(year, month, month_span[1])
        data['Date'] = poll_date
        data_list.append(data)
    return data_list


def get_frame_from_workbook(path, selected_tab=None):
    wb = get_workbook(path)
    tabs = get_data_tabs(wb)

    dl = []
    for tab in tabs:
        if selected_tab is not None and tab.name != selected_tab:
            continue
        data = get_data_from_sheet(tab)
        dl.extend(data)

    h = ['Date', 'Pollster', 'Con', 'Lab', 'LD', 'UKIP', 'Green']
    t = OrderedDict([(k, [x[k] for x in dl]) for k in h])
    df = pd.DataFrame(t).sort_values("Date")
    return df
