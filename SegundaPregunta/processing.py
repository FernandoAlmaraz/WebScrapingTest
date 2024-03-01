import datetime

months = [
    "ENERO",
    "FEBRERO",
    "MARZO",
    "ABRIL",
    "MAYO",
    "JUNIO",
    "JULIO",
    "AGOSTO",
    "SEPTIEMBRE",
    "OCTUBRE",
    "NOVIEMBRE",
    "DICIEMBRE",
]


class Processing:
    @staticmethod
    def split_dates(reference_date):
        date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        return {"year": year, "month": month, "day": day}

    @staticmethod
    def number_to_month(month):
        return months[month - 1]

    @staticmethod
    def clean_list(list):
        return [
            element
            for element in list
            if element.strip() and any(month in element.upper() for month in months)
        ]

    @staticmethod
    def find_mounth(newstellers, month):
        index_reference_month = -1
        for newsteller in newstellers:
            if month in newsteller:
                index_reference_month = months.index(month)
                break

        if index_reference_month != -1:
            return months[index_reference_month + 1 :]
        else:
            return None
