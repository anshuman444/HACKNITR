import pathway as pw
from governanceflow.ingestion.survey_ingestor import build_survey_ingestion_pipeline
from governanceflow.extraction.context_engine import infer_survey_context
from governanceflow.discovery.policy_discoverer import discover_policies
from governanceflow.discovery.policy_parser import parse_policies
from governanceflow.analytics.ground_reality_aggregator import aggregate_survey_data
from governanceflow.analytics.comparison_engine import compare_reality_vs_policy
from governanceflow.agents.super_agent import SuperAgent

def run_governance_flow():
    raw_surveys = build_survey_ingestion_pipeline()
    context = infer_survey_context(raw_surveys)
    discovered_policies = discover_policies(context)
    parsed_policies = parse_policies(discovered_policies)
    ground_reality = aggregate_survey_data(raw_surveys)
    
    comparisons = compare_reality_vs_policy(ground_reality, parsed_policies)
    agent = SuperAgent()
    
    final_output = comparisons.select(
        *pw.this,
        final_report=pw.apply(
            agent.generate_formal_report,
            pw.this.survey_title,
            pw.this.observed_result,
            pw.this.policy_targets,
            pw.this.compliance_stats,
            pw.this.common_comments
        )
    )
    
    pw.io.json.write(final_output, "governanceflow/data/intelligence_reports.json")
    pw.run()

if __name__ == "__main__":
    run_governance_flow()
