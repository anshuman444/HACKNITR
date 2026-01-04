import pathway as pw
import json

def compare_reality_vs_policy(ground_reality, parsed_policies):
    comparison = ground_reality.join(
        parsed_policies,
        pw.left.survey_title == pw.right.survey_title
    ).select(
        pw.left.survey_title,
        pw.left.observed_result,
        pw.left.common_comments,
        pw.right.policy_targets,
        compliance_stats=pw.apply(calculate_compliance, pw.left.observed_result, pw.right.policy_targets)
    )
    return comparison

def calculate_compliance(observed, policy_json):
    try:
        policy = json.loads(policy_json)
        target = policy.get("target_metric", 1)
        comp = (observed / target) * 100
        return json.dumps({"compliance_percentage": comp, "gap_count": target - observed})
    except:
        return "{}"
