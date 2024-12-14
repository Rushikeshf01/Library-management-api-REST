from django.conf import settings

def calculate_fine(due_date, return_date):

    no_of_days = return_date - due_date
    no_of_days = no_of_days.days
    fine = no_of_days * settings.FINE_RATE
    message = f"Book returned Succefully and You have been fined {fine}rs for delaying in the return of the book for {no_of_days} days"

    return fine,message