import time
from core.classifier import classify
from core.router import route_problem
from core.database import insert_problem, update_problem_status, get_problem
import uuid

def run_tests():
    test_cases = [
        {"desc": "The fan in Room 204 is broken", "expected_cat": "Infrastructure/Maintenance", "expected_dept": "Campus Maintenance Cell"},
        {"desc": "A senior is threatening juniors in hostel", "expected_cat": "Anti-Ragging & Safety", "expected_dept": "Student Affairs / Security Office"},
        {"desc": "Dal is undercooked in today's lunch", "expected_cat": "Mess & Food Quality", "expected_dept": "Mess Committee / Warden"},
        {"desc": "My attendance is wrongly marked", "expected_cat": "Academic Issues", "expected_dept": "Academic Office / HOD"},
        {"desc": "Toilet on 2nd floor has no water", "expected_cat": "Bathroom & Hygiene", "expected_dept": "Housekeeping Department"},
        {"desc": "I have a general suggestion", "expected_cat": "Other", "expected_dept": "General Administration"},
    ]
    
    correct = 0
    results = []
    
    print("Testing flows...")
    for t in test_cases:
        t_id = str(uuid.uuid4())[:8].upper()
        # Mock submit
        insert_problem(t_id, t["desc"], None)
        
        # Test classifier
        result = classify(t["desc"])
        category = result["category"]
        confidence = result["confidence"]
        
        # Test router
        department = route_problem(t_id, category, confidence)
        
        # Verify
        prob = get_problem(t_id)
        
        is_correct = category == t["expected_cat"]
        if is_correct:
            correct += 1
            
        results.append({
            "id": t_id,
            "desc": t["desc"],
            "category": category,
            "expected_cat": t["expected_cat"],
            "dept": department,
            "status": prob["status"],
            "correct": is_correct
        })
        time.sleep(1) # ratelimit
        
    print(f"\nAccuracy: {correct}/{len(test_cases)}")
    
    with open("TESTING.md", "w", encoding="utf-8") as f:
        f.write("# Testing Results\n\n")
        f.write(f"**Accuracy:** {correct}/{len(test_cases)}\n\n")
        f.write("## Test Cases\n\n")
        
        for r in results:
            f.write(f"### {r['desc']}\n")
            f.write(f"- ID: `{r['id']}`\n")
            f.write(f"- Assigned Category: **{r['category']}** (Expected: {r['expected_cat']})\n")
            f.write(f"- Assigned Department: **{r['dept']}**\n")
            f.write(f"- Initial Status: **{r['status']}**\n")
            f.write(f"- Result: {'✅ PASS' if r['correct'] else '❌ FAIL'}\n\n")

if __name__ == "__main__":
    run_tests()
