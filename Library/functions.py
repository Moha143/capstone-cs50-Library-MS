
from datetime import date, datetime
from sched import scheduler
from django.conf import settings

from Library import models as models
from django.db.models import Q

currentDate = date.today()
datetime_day = datetime.now()


def bookborrow():

    try:
        Borrow = models.Borrow.objects.filter(status="Borrow")
        for i in range(0, len(Borrow)):
            EndDate = Borrow[i].end_date
            if currentDate > EndDate:
                Borrow[i].status = "Not Returned"
                Borrow[i].is_fine = True
                Borrow[i].save()

    except Exception as error:
        pass


def Fine():
    try:

        Borrow = models.Borrow.objects.filter(status="Not Returned")

        for i in range(0, len(Borrow)):
            EndDate = Borrow[i].end_date
            Member = Borrow[i].Member
            if currentDate > EndDate:

                if models.Fine.objects.filter(borrow=Borrow[i].id).exists():
                    pass

                else:
                    fine = models.Fine(
                        borrow=Borrow[i], amount=3*float(Borrow[i].NBook), paid="0.0", Member=Member)
                    fine.save()

    except Exception as error:
        print(str(error))
