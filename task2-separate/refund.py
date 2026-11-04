"""Task 2: train delay refund (simplified rules, just for practice).

The rules (this is the specification):
  * delay of at least  60 minutes -> 25 % of the ticket price back
  * delay of at least 120 minutes -> 50 % of the ticket price back
  * a refund below 4.00 euro is not paid out -> 0.0
"""


def refund(ticket_price, delay_minutes):
    """Return the refund in euro for a delayed train."""
    if delay_minutes > 60:
        amount = ticket_price * 0.25
    elif delay_minutes >= 120:
        amount = ticket_price * 0.50
    else:
        amount = 0.0

    if amount < 4:
        return 0.0
    return round(amount, 2)
