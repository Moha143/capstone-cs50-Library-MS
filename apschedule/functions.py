
from datetime import date, datetime
from django.conf import settings

from Library import models as models
from django.db.models import Q

currentDate = date.today()
datetime_day = datetime.now()


def bookborrow():
    try:
        print("Bookborrow")
        Borrow = models.Borrow.objects.all()
        for i in range(0, len(Borrow)):
            EndDate = i[Borrow].endDate
            if currentDate > EndDate:
                fine = models.Fine(
                    borrow=i[Borrow].id, amount=3*int(i[Borrow].NBook)
                )

                fine.save()
    except Exception as error:
        pass
