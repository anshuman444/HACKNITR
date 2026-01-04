import pathway as pw

def aggregate_survey_data(surveys):
    metrics = surveys.groupby(pw.this.survey_title, pw.this.location, pw.this.department).reduce(
        survey_title=pw.this.survey_title,
        location=pw.this.location,
        department=pw.this.department,
        total_surveyed=pw.reducers.count(),
        observed_result=pw.reducers.count(pw.this.service_quality),
        avg_quality=pw.reducers.avg(pw.this.service_quality),
        common_comments=pw.reducers.tuple(pw.this.comments)
    )
    return metrics
