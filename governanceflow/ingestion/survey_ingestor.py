import pathway as pw
import json
import os

def build_survey_ingestion_pipeline(data_path="governanceflow/data"):
    """
    Watches a folder for survey files (CSV) and survey_metadata.json.
    """
    # 1. Ingest Survey Metadata (Title)
    metadata_path = os.path.join(data_path, "survey_metadata.json")
    
    try:
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                data = [json.load(f)]
        else:
            data = [{"survey_title": "Default Governance Survey"}]
    except:
        data = [{"survey_title": "Default Governance Survey"}]

    import pandas as pd
    metadata = pw.debug.table_from_pandas(
        pd.DataFrame(data),
        schema=MetadataSchema,
    )

    # 2. Ingest All Survey Responses (CSV)
    surveys = pw.io.csv.read(
        data_path,
        schema=SurveySchema,
        mode="streaming",
        autocommit_duration_ms=100
    )
    
    # 3. Join Metadata to Surveys using a constant key
    surveys_with_key = surveys.select(*pw.this, join_key=pw.apply(lambda _: 1, pw.this.comments))
    metadata_with_key = metadata.select(*pw.this, join_key=pw.apply(lambda _: 1, pw.this.survey_title))
    
    integrated_surveys = surveys_with_key.join(
        metadata_with_key,
        pw.left.join_key == pw.right.join_key
    ).select(
        *pw.left,
        survey_title=pw.right.survey_title
    )
    
    return integrated_surveys

class MetadataSchema(pw.Schema):
    survey_title: str

class SurveySchema(pw.Schema):
    timestamp: str
    location: str
    department: str
    respondent_id: str
    service_quality: int
    bribe_requested: str
    delay_days: int
    comments: str
