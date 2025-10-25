"""
Result Aggregator - Combines outputs from multiple agents

Aggregates, synthesizes, and validates results from multiple agents
working on decomposed tasks within an assembly.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AggregationStrategy(Enum):
    """Strategies for aggregating results"""
    MERGE = "merge"  # Merge all outputs
    VOTE = "vote"  # Use majority voting
    CONSENSUS = "consensus"  # Require consensus
    WEIGHTED = "weighted"  # Weighted combination
    BEST = "best"  # Select best result
    SEQUENTIAL = "sequential"  # Sequential pipeline


@dataclass
class AgentOutput:
    """Output from a single agent"""
    agent_id: str
    role_name: str
    output_data: Dict[str, Any]
    confidence: float
    metadata: Dict[str, Any]
    timestamp: str

    def validate(self) -> bool:
        """Validate agent output"""
        if not self.output_data:
            return False
        if self.confidence < 0 or self.confidence > 1:
            return False
        return True


@dataclass
class AggregatedResult:
    """Aggregated result from multiple agents"""
    outputs: Dict[str, Any]
    contributing_agents: List[str]
    confidence: float
    strategy_used: AggregationStrategy
    conflicts: List[Dict[str, Any]]
    metadata: Dict[str, Any]


@dataclass
class ValidationResult:
    """Result of output validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    quality_score: float


class ResultAggregator:
    """
    Aggregates results from multiple agents

    Provides various strategies for combining agent outputs,
    resolving conflicts, and validating final results.
    """

    def __init__(self):
        self.aggregation_strategies = {
            AggregationStrategy.MERGE: self._merge_strategy,
            AggregationStrategy.VOTE: self._vote_strategy,
            AggregationStrategy.CONSENSUS: self._consensus_strategy,
            AggregationStrategy.WEIGHTED: self._weighted_strategy,
            AggregationStrategy.BEST: self._best_strategy,
            AggregationStrategy.SEQUENTIAL: self._sequential_strategy,
        }

    async def aggregate(
        self,
        agent_outputs: List[AgentOutput],
        strategy: AggregationStrategy = AggregationStrategy.MERGE,
        config: Optional[Dict[str, Any]] = None
    ) -> AggregatedResult:
        """
        Aggregate outputs from multiple agents

        Args:
            agent_outputs: List of outputs from agents
            strategy: Aggregation strategy to use
            config: Optional configuration for aggregation

        Returns:
            AggregatedResult with combined outputs
        """
        logger.info(
            f"Aggregating {len(agent_outputs)} outputs "
            f"using strategy: {strategy.value}"
        )

        # Validate inputs
        valid_outputs = [out for out in agent_outputs if out.validate()]
        if len(valid_outputs) < len(agent_outputs):
            logger.warning(
                f"Filtered out {len(agent_outputs) - len(valid_outputs)} "
                f"invalid outputs"
            )

        if not valid_outputs:
            logger.error("No valid outputs to aggregate")
            return self._empty_result(strategy)

        # Select and execute strategy
        strategy_func = self.aggregation_strategies.get(strategy)
        if not strategy_func:
            logger.warning(f"Unknown strategy {strategy}, using MERGE")
            strategy_func = self._merge_strategy

        config = config or {}
        result = await strategy_func(valid_outputs, config)

        logger.info(
            f"Aggregation complete. "
            f"Confidence: {result.confidence:.2f}, "
            f"Conflicts: {len(result.conflicts)}"
        )

        return result

    async def validate_result(
        self,
        result: AggregatedResult,
        requirements: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate aggregated result against requirements

        Args:
            result: Aggregated result to validate
            requirements: Validation requirements

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []
        quality_score = result.confidence

        # Check required outputs
        required_keys = requirements.get("required_outputs", [])
        for key in required_keys:
            if key not in result.outputs:
                errors.append(f"Missing required output: {key}")

        # Check conflicts
        if result.conflicts and len(result.conflicts) > 0:
            conflict_threshold = requirements.get("max_conflicts", 3)
            if len(result.conflicts) > conflict_threshold:
                errors.append(
                    f"Too many conflicts: {len(result.conflicts)} "
                    f"(max: {conflict_threshold})"
                )
            else:
                warnings.append(f"Found {len(result.conflicts)} conflicts")

        # Check confidence threshold
        min_confidence = requirements.get("min_confidence", 0.7)
        if result.confidence < min_confidence:
            errors.append(
                f"Confidence {result.confidence:.2f} "
                f"below threshold {min_confidence}"
            )

        # Adjust quality score based on issues
        quality_score -= len(errors) * 0.1
        quality_score -= len(warnings) * 0.05
        quality_score = max(0.0, min(1.0, quality_score))

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            quality_score=quality_score
        )

    async def resolve_conflicts(
        self,
        conflicts: List[Dict[str, Any]],
        strategy: str = "majority"
    ) -> Dict[str, Any]:
        """
        Resolve conflicts between agent outputs

        Args:
            conflicts: List of conflicting outputs
            strategy: Resolution strategy (majority, weighted, manual)

        Returns:
            Resolved output
        """
        if not conflicts:
            return {}

        if strategy == "majority":
            return self._resolve_by_majority(conflicts)
        elif strategy == "weighted":
            return self._resolve_by_weight(conflicts)
        elif strategy == "confidence":
            return self._resolve_by_confidence(conflicts)
        else:
            logger.warning(f"Unknown resolution strategy: {strategy}")
            return conflicts[0] if conflicts else {}

    # Aggregation Strategy Implementations

    async def _merge_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Merge all outputs into single result"""
        merged = {}
        conflicts = []

        for output in outputs:
            for key, value in output.output_data.items():
                if key in merged and merged[key] != value:
                    # Conflict detected
                    conflicts.append({
                        "key": key,
                        "values": [merged[key], value],
                        "agents": [
                            next(
                                o.agent_id for o in outputs
                                if key in o.output_data and o.output_data[key] == merged[key]
                            ),
                            output.agent_id
                        ]
                    })
                merged[key] = value

        avg_confidence = sum(o.confidence for o in outputs) / len(outputs)

        return AggregatedResult(
            outputs=merged,
            contributing_agents=[o.agent_id for o in outputs],
            confidence=avg_confidence,
            strategy_used=AggregationStrategy.MERGE,
            conflicts=conflicts,
            metadata={"num_outputs": len(outputs)}
        )

    async def _vote_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Use majority voting for each output key"""
        votes: Dict[str, Dict[Any, int]] = {}
        all_keys = set()

        # Collect votes
        for output in outputs:
            all_keys.update(output.output_data.keys())
            for key, value in output.output_data.items():
                if key not in votes:
                    votes[key] = {}
                value_str = str(value)
                votes[key][value_str] = votes[key].get(value_str, 0) + 1

        # Determine winners
        result = {}
        conflicts = []
        for key in all_keys:
            if key in votes:
                sorted_votes = sorted(
                    votes[key].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                if len(sorted_votes) > 1 and sorted_votes[0][1] == sorted_votes[1][1]:
                    # Tie - conflict
                    conflicts.append({
                        "key": key,
                        "values": [v[0] for v in sorted_votes[:2]],
                        "votes": [v[1] for v in sorted_votes[:2]]
                    })
                result[key] = sorted_votes[0][0]

        # Calculate confidence based on vote strength
        total_votes = sum(sum(v.values()) for v in votes.values())
        winning_votes = sum(max(v.values()) for v in votes.values())
        confidence = winning_votes / total_votes if total_votes > 0 else 0.0

        return AggregatedResult(
            outputs=result,
            contributing_agents=[o.agent_id for o in outputs],
            confidence=confidence,
            strategy_used=AggregationStrategy.VOTE,
            conflicts=conflicts,
            metadata={"total_votes": total_votes}
        )

    async def _consensus_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Require consensus (all agents agree)"""
        if not outputs:
            return self._empty_result(AggregationStrategy.CONSENSUS)

        # Use first output as baseline
        consensus = outputs[0].output_data.copy()
        conflicts = []

        # Check all outputs match
        for output in outputs[1:]:
            for key, value in output.output_data.items():
                if key in consensus:
                    if consensus[key] != value:
                        conflicts.append({
                            "key": key,
                            "values": [consensus[key], value],
                            "agents": [outputs[0].agent_id, output.agent_id]
                        })
                        # Remove from consensus if disagreement
                        del consensus[key]

        # Confidence is 1.0 if perfect consensus, 0.0 if no agreement
        all_keys = set()
        for output in outputs:
            all_keys.update(output.output_data.keys())

        confidence = len(consensus) / len(all_keys) if all_keys else 0.0

        return AggregatedResult(
            outputs=consensus,
            contributing_agents=[o.agent_id for o in outputs],
            confidence=confidence,
            strategy_used=AggregationStrategy.CONSENSUS,
            conflicts=conflicts,
            metadata={"consensus_keys": len(consensus)}
        )

    async def _weighted_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Weight outputs by agent confidence"""
        weighted = {}
        weights: Dict[str, List[tuple]] = {}  # key -> [(value, weight)]

        for output in outputs:
            for key, value in output.output_data.items():
                if key not in weights:
                    weights[key] = []
                weights[key].append((value, output.confidence))

        # Select highest weighted value for each key
        for key, value_weights in weights.items():
            weighted[key] = max(value_weights, key=lambda x: x[1])[0]

        # Average confidence weighted by contributions
        total_weight = sum(o.confidence for o in outputs)
        confidence = total_weight / len(outputs) if outputs else 0.0

        return AggregatedResult(
            outputs=weighted,
            contributing_agents=[o.agent_id for o in outputs],
            confidence=confidence,
            strategy_used=AggregationStrategy.WEIGHTED,
            conflicts=[],
            metadata={"total_weight": total_weight}
        )

    async def _best_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Select best output based on confidence"""
        if not outputs:
            return self._empty_result(AggregationStrategy.BEST)

        best = max(outputs, key=lambda o: o.confidence)

        return AggregatedResult(
            outputs=best.output_data,
            contributing_agents=[best.agent_id],
            confidence=best.confidence,
            strategy_used=AggregationStrategy.BEST,
            conflicts=[],
            metadata={"selected_agent": best.agent_id}
        )

    async def _sequential_strategy(
        self,
        outputs: List[AgentOutput],
        config: Dict[str, Any]
    ) -> AggregatedResult:
        """Process outputs sequentially (pipeline)"""
        result = {}

        # Process in order, allowing later outputs to override
        for output in outputs:
            result.update(output.output_data)

        avg_confidence = sum(o.confidence for o in outputs) / len(outputs)

        return AggregatedResult(
            outputs=result,
            contributing_agents=[o.agent_id for o in outputs],
            confidence=avg_confidence,
            strategy_used=AggregationStrategy.SEQUENTIAL,
            conflicts=[],
            metadata={"pipeline_length": len(outputs)}
        )

    # Conflict Resolution Helpers

    def _resolve_by_majority(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Resolve by majority rule"""
        # Simplified - just take first value
        return {c["key"]: c["values"][0] for c in conflicts}

    def _resolve_by_weight(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Resolve by weighted voting"""
        # Simplified - just take first value
        return {c["key"]: c["values"][0] for c in conflicts}

    def _resolve_by_confidence(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Resolve by agent confidence"""
        # Simplified - just take first value
        return {c["key"]: c["values"][0] for c in conflicts}

    def _empty_result(self, strategy: AggregationStrategy) -> AggregatedResult:
        """Create empty result"""
        return AggregatedResult(
            outputs={},
            contributing_agents=[],
            confidence=0.0,
            strategy_used=strategy,
            conflicts=[],
            metadata={}
        )
