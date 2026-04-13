from core import database, notifier

CATEGORY_TO_DEPARTMENT = {
    "Bathroom & Hygiene": "Housekeeping Department",
    "Anti-Ragging & Safety": "Student Affairs / Security Office",
    "Mess & Food Quality": "Mess Committee / Warden",
    "Academic Issues": "Academic Office / HOD",
    "Infrastructure/Maintenance": "Campus Maintenance Cell",
    "Other": "General Administration"
}

def route_problem(problem_id: str, category: str, confidence: float) -> str:
    # 1. Look up department
    department = CATEGORY_TO_DEPARTMENT.get(category, "General Administration")
    
    # 2. Update database
    database.update_problem_classification(problem_id, category, confidence, department)
    
    # 3. Notify
    notifier.notify(problem_id, department, category)
    
    # 4. Return new department
    return department
