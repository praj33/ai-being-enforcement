from models.evaluator_result import EvaluatorResult

class SafetyRiskEvaluator:
    name = "safety_risk"

    def evaluate(self, input_data):
        if (
    "HIGH_RISK" in input_data.risk_flags
    or "SELF_HARM" in input_data.risk_flags
):
            return EvaluatorResult(
            name=self.name,
            triggered=True,
            action="BLOCK",
            code="SELF_HARM_RISK"
        )

        return EvaluatorResult(self.name, False, "EXECUTE", "")
