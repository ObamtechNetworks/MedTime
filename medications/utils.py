from datetime import timedelta
from django.utils import timezone

def priority_lead_time_check(medication):
    """
    Check and enforce the priority lead time for a priority medication.
    
    Args:
        medication (Medication): The medication instance to check.
        
    Returns:
        lead_time_passed (bool): True if the priority lead time has passed or if not applicable.
        next_allowed_time (datetime): The next time the user can take non-priority medications.
    """
    # Check if the medication is a priority
    if medication.priority_flag:
        if medication.last_intake_time:
            # Calculate the next available time to take other medications
            next_allowed_time = medication.last_intake_time + timedelta(minutes=medication.priority_lead_time)
            
            # Check if the current time has passed the priority lead time
            if timezone.now() >= next_allowed_time:
                return True, None  # Lead time has passed
            else:
                return False, next_allowed_time  # Lead time not yet passed, return the next allowed time
        else:
            # If last_intake_time is not set, priority lead time is irrelevant
            return False, None
    return True, None  # No priority lead time to enforce


def take_medication(medication):
    # Check if priority lead time is satisfied
    can_take, next_time = priority_lead_time_check(medication)
    
    if can_take:
        medication.take_dose()
        return "Dose taken successfully."
    else:
        return f"Cannot take medication yet. You can take it at {next_time}."