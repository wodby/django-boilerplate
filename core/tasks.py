from celery import shared_task


@shared_task
def add(left, right):
    """Return the sum of two values as a minimal background-task example."""
    return left + right
