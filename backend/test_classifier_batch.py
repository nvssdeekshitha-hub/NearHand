"""
Batch test script for NearHand's AI fallback classifier.
Run this from inside the backend/ folder with your venv/environment active:

    python test_classifier_batch.py

This checks multiple request types and languages in one go, so you can
spot any remaining gaps before the demo.
"""

from app.services.ai_service import analyze_text_request

test_cases = [
    # (description, input_text, expected_request_type, expected_urgency)
    ("Fall - Telugu script", "నాకు బాత్రూమ్‌లో కాలు జారి పడిపోయాను, లేవలేకపోతున్నాను", "FALL", "CRITICAL"),
    ("Fall - Romanized Telugu", "Nenu bathroom lo padipoyanu, levalekapothunnanu", "FALL", "CRITICAL"),
    ("Fall - English", "I fell down and I can't stand up", "FALL", "CRITICAL"),

    ("Medical/Heart attack - English", "I am having a heart attack", "MEDICAL_HELP", "CRITICAL"),
    ("Medical/Heart attack - Telugu script", "నాకు గుండెపోటు వస్తోంది, ఊపిరి పీల్చుకోలేకపోతున్నాను", "MEDICAL_HELP", "CRITICAL"),
    ("Medical/Heart attack - Romanized", "Naku gundepotu vasthondi, oopiri adadam ledu", "MEDICAL_HELP", "CRITICAL"),
    ("Medical - Chest pain English", "I have severe chest pain and difficulty breathing", "MEDICAL_HELP", "CRITICAL"),

    ("Medication - English", "I need my blood pressure medicine", "MEDICATION", None),
    ("Medication - forgot dose", "I forgot to take my evening medicine", "MEDICATION", None),

    ("General help - English", "Can someone help me with groceries", "GENERAL_HELP", "MEDIUM"),
    ("General help - vague", "I need help", "GENERAL_HELP", None),

    ("Companionship - English", "I feel very lonely today", "COMPANIONSHIP", "LOW"),
    ("Companionship - English variant", "I want someone to talk to", "COMPANIONSHIP", "LOW"),
    ("Companionship - Romanized Telugu", "Nenu ontariga feel avuthunnanu", "COMPANIONSHIP", "LOW"),
    ("Companionship - Telugu script", "నేను ఒంటరిగా ఫీల్ అవుతున్నాను", "COMPANIONSHIP", "LOW"),
]

print("=" * 90)
print(f"{'Test Case':<38} {'Expected':<15} {'Actual':<15} {'Urgency':<10} Result")
print("=" * 90)

pass_count = 0
fail_count = 0

for description, text, expected_type, expected_urgency in test_cases:
    result = analyze_text_request(text)

    # Handle both dict and pydantic-model style results
    actual_type = result.get("request_type") if isinstance(result, dict) else result.request_type
    actual_urgency = result.get("urgency") if isinstance(result, dict) else result.urgency

    type_ok = (actual_type == expected_type)
    urgency_ok = (expected_urgency is None) or (actual_urgency == expected_urgency)
    passed = type_ok and urgency_ok

    status = "PASS" if passed else "FAIL"
    if passed:
        pass_count += 1
    else:
        fail_count += 1

    print(f"{description:<38} {expected_type:<15} {actual_type:<15} {actual_urgency:<10} {status}")

print("=" * 90)
print(f"Total: {len(test_cases)}  |  Passed: {pass_count}  |  Failed: {fail_count}")
print("=" * 90)

if fail_count > 0:
    print("\nSome cases failed — review the classifier's keyword list for the failing categories above.")
else:
    print("\nAll classifier test cases passed.")
