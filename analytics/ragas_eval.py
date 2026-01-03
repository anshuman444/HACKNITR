from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

def run_ragas_evaluation(question, answer, context):
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [[context]]
    }
    ds = Dataset.from_dict(data)
    return evaluate(ds, metrics=[faithfulness, answer_relevancy])
 