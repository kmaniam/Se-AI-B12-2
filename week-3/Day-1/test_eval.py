
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import OllamaModel
from deepeval.evaluate.configs import CacheConfig

# Configure the local Ollama model as the evaluation judge
judge_model = OllamaModel(
    model="qwen2.5:3b",
    base_url="http://localhost:11434",
    temperature=0,
)

# Question and sample answer
question = "What is Oracle Data Guard?"

actual_answer = (
    "Oracle Data Guard is an Oracle Database technology "
    "that provides high availability, data protection, "
    "and disaster recovery by maintaining standby databases "
    "for a primary database. It supports switchover and "
    "failover when database roles need to change."
)

# Create the evaluation test case
test_case = LLMTestCase(
    input=question,
    actual_output=actual_answer,
)

# Configure the evaluation metric
relevancy = AnswerRelevancyMetric(
    threshold=0.7,
    model=judge_model,
    include_reason=True,
)

# Run evaluation
evaluate(
    test_cases=[test_case],
    metrics=[relevancy],
    cache_config=CacheConfig(write_cache=False),
)
