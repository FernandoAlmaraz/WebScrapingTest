from datetime import datetime


class DateHelper:
    @staticmethod
    def split_dates(reference_date):
        date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        return {"year": year, "month": month, "day": day}

    @staticmethod
    def number_to_month(month):
        month_names = [
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
        return month_names[month - 1]
