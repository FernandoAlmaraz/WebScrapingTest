from datetime import datetime

months = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def split_dates(reference_date):
    date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    return {"year": year, "month": month, "day": day}


def number_to_month(month):

    return months[month - 1]


def check_older_months(values, month_reference):
    month_index = months.index(month_reference)
    return [
        months.index(current_month) > month_index
        for current_month in values
        if current_month in months
    ]
