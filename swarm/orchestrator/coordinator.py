"""
Swarm Coordinator - Main orchestration logic for AI agent swarms

This module coordinates multiple AI agents working together as a swarm to accomplish
complex tasks through role-based collaboration and assembly execution.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    """Status of assembly execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionContext:
    """Context for assembly execution"""
    task_id: str
    input_data: Dict[str, Any]
    constraints: Dict[str, Any]
    timeout: Optional[timedelta] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Role:
    """Defines a role in the swarm"""
    name: str
    capabilities: List[str]
    responsibilities: List[str]
    dependencies: List[str]

    def can_fulfill(self, requirements: List[str]) -> bool:
        """Check if role can fulfill given requirements"""
        return all(req in self.capabilities for req in requirements)


@dataclass
class Agent:
    """Represents an AI agent in the swarm"""
    agent_id: str
    name: str
    capabilities: List[str]
    current_role: Optional[Role] = None
    status: str = "available"

    def assign_role(self, role: Role) -> bool:
        """Assign a role to this agent"""
        if self.can_perform_role(role):
            self.current_role = role
            self.status = "assigned"
            return True
        return False

    def can_perform_role(self, role: Role) -> bool:
        """Check if agent can perform the given role"""
        return all(cap in self.capabilities for cap in role.capabilities[:3])


@dataclass
class Workflow:
    """Defines workflow steps for assembly execution"""
    steps: List[Dict[str, Any]]
    parallel_execution: bool = False
    error_handling: str = "stop"  # stop, continue, retry


@dataclass
class SuccessCriteria:
    """Criteria for successful assembly completion"""
    required_outputs: List[str]
    quality_threshold: float = 0.8
    timeout: Optional[timedelta] = None
    validation_rules: List[str] = None

    def __post_init__(self):
        if self.validation_rules is None:
            self.validation_rules = []


@dataclass
class Assembly:
    """Defines a swarm assembly configuration"""
    name: str
    description: str
    roles: List[Role]
    workflow: Workflow
    success_criteria: SuccessCriteria
    version: str = "1.0.0"


@dataclass
class Contribution:
    """Represents an agent's contribution to assembly execution"""
    agent_id: str
    role_name: str
    outputs: Dict[str, Any]
    duration: timedelta
    quality_score: float = 0.0


@dataclass
class AssemblyResult:
    """Result of assembly execution"""
    assembly_name: str
    status: ExecutionStatus
    outputs: Dict[str, Any]
    agent_contributions: Dict[str, Contribution]
    duration: timedelta
    error_message: Optional[str] = None
    started_at: datetime = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.utcnow()


class RoleRequirements:
    """Requirements for role assignment"""
    def __init__(self, required_roles: List[str], min_capabilities: Dict[str, int]):
        self.required_roles = required_roles
        self.min_capabilities = min_capabilities


class SwarmCoordinator:
    """
    Main coordinator for swarm operations

    Manages agent assignment, assembly execution, and result aggregation.
    """

    def __init__(self):
        self.active_assemblies: Dict[str, Assembly] = {}
        self.available_agents: List[Agent] = []
        self.execution_history: List[AssemblyResult] = []

    async def execute_assembly(
        self,
        assembly: Assembly,
        context: ExecutionContext
    ) -> AssemblyResult:
        """
        Execute a swarm assembly

        Args:
            assembly: The assembly definition to execute
            context: Execution context with input data and constraints

        Returns:
            AssemblyResult with execution status and outputs
        """
        logger.info(f"Starting assembly execution: {assembly.name}")
        start_time = datetime.utcnow()

        try:
            # Register assembly as active
            self.active_assemblies[context.task_id] = assembly

            # Assign roles to agents
            role_assignments = await self._assign_roles(assembly.roles)
            if not role_assignments:
                raise ValueError("Failed to assign all required roles")

            logger.info(f"Assigned {len(role_assignments)} roles")

            # Execute workflow
            outputs = await self._execute_workflow(
                assembly.workflow,
                role_assignments,
                context
            )

            # Collect contributions
            contributions = await self._collect_contributions(role_assignments)

            # Validate results
            success = self._validate_results(outputs, assembly.success_criteria)

            duration = datetime.utcnow() - start_time

            result = AssemblyResult(
                assembly_name=assembly.name,
                status=ExecutionStatus.COMPLETED if success else ExecutionStatus.FAILED,
                outputs=outputs,
                agent_contributions=contributions,
                duration=duration,
                started_at=start_time,
                completed_at=datetime.utcnow()
            )

            self.execution_history.append(result)
            logger.info(f"Assembly {assembly.name} completed with status: {result.status}")

            return result

        except Exception as e:
            logger.error(f"Assembly execution failed: {str(e)}")
            duration = datetime.utcnow() - start_time

            return AssemblyResult(
                assembly_name=assembly.name,
                status=ExecutionStatus.FAILED,
                outputs={},
                agent_contributions={},
                duration=duration,
                error_message=str(e),
                started_at=start_time,
                completed_at=datetime.utcnow()
            )
        finally:
            # Clean up
            if context.task_id in self.active_assemblies:
                del self.active_assemblies[context.task_id]

    async def assign_roles(
        self,
        agents: List[Agent],
        requirements: RoleRequirements
    ) -> Dict[Agent, Role]:
        """
        Assign roles to available agents based on requirements

        Args:
            agents: List of available agents
            requirements: Role assignment requirements

        Returns:
            Dictionary mapping agents to assigned roles
        """
        assignments = {}

        # Sort agents by capability match
        for role_name in requirements.required_roles:
            best_agent = None
            best_score = 0

            for agent in agents:
                if agent in assignments:
                    continue

                score = self._calculate_role_fitness(agent, role_name)
                if score > best_score:
                    best_score = score
                    best_agent = agent

            if best_agent:
                # Create role and assign
                role = Role(
                    name=role_name,
                    capabilities=[],
                    responsibilities=[],
                    dependencies=[]
                )
                assignments[best_agent] = role

        return assignments

    async def _assign_roles(self, roles: List[Role]) -> Dict[str, Agent]:
        """Internal role assignment logic"""
        assignments = {}
        available = self.available_agents.copy()

        for role in roles:
            # Find best agent for this role
            best_agent = None
            best_score = 0

            for agent in available:
                if agent.can_perform_role(role):
                    score = len(set(agent.capabilities) & set(role.capabilities))
                    if score > best_score:
                        best_score = score
                        best_agent = agent

            if best_agent:
                best_agent.assign_role(role)
                assignments[role.name] = best_agent
                available.remove(best_agent)
            else:
                logger.warning(f"No suitable agent found for role: {role.name}")

        return assignments

    async def _execute_workflow(
        self,
        workflow: Workflow,
        role_assignments: Dict[str, Agent],
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Execute workflow steps"""
        outputs = {}

        if workflow.parallel_execution:
            # Execute steps in parallel
            tasks = [
                self._execute_step(step, role_assignments, context)
                for step in workflow.steps
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Step {i} failed: {result}")
                    if workflow.error_handling == "stop":
                        raise result
                else:
                    outputs.update(result)
        else:
            # Execute steps sequentially
            for step in workflow.steps:
                try:
                    result = await self._execute_step(step, role_assignments, context)
                    outputs.update(result)
                except Exception as e:
                    logger.error(f"Step failed: {e}")
                    if workflow.error_handling == "stop":
                        raise

        return outputs

    async def _execute_step(
        self,
        step: Dict[str, Any],
        role_assignments: Dict[str, Agent],
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Execute a single workflow step"""
        # Placeholder implementation
        # In real implementation, this would delegate to assigned agents
        role_name = step.get("role")
        action = step.get("action")

        logger.info(f"Executing step: {action} with role: {role_name}")

        # Simulate execution
        await asyncio.sleep(0.1)

        return {f"{role_name}_{action}": "completed"}

    async def _collect_contributions(
        self,
        role_assignments: Dict[str, Agent]
    ) -> Dict[str, Contribution]:
        """Collect contributions from all agents"""
        contributions = {}

        for role_name, agent in role_assignments.items():
            contribution = Contribution(
                agent_id=agent.agent_id,
                role_name=role_name,
                outputs={},
                duration=timedelta(seconds=1),
                quality_score=0.85
            )
            contributions[agent.agent_id] = contribution

        return contributions

    def _validate_results(
        self,
        outputs: Dict[str, Any],
        criteria: SuccessCriteria
    ) -> bool:
        """Validate execution results against success criteria"""
        # Check all required outputs are present
        for required in criteria.required_outputs:
            if required not in outputs:
                logger.warning(f"Missing required output: {required}")
                return False

        # Additional validation could be added here
        return True

    def _calculate_role_fitness(self, agent: Agent, role_name: str) -> float:
        """Calculate how well an agent fits a role"""
        # Placeholder implementation
        # In real implementation, would use more sophisticated matching
        return 0.5

    def register_agent(self, agent: Agent) -> None:
        """Register an agent as available for assignments"""
        if agent not in self.available_agents:
            self.available_agents.append(agent)
            logger.info(f"Registered agent: {agent.name}")

    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent from available pool"""
        self.available_agents = [
            a for a in self.available_agents
            if a.agent_id != agent_id
        ]
        logger.info(f"Unregistered agent: {agent_id}")

    def get_active_assemblies(self) -> List[str]:
        """Get list of currently active assemblies"""
        return list(self.active_assemblies.keys())

    def get_execution_history(self) -> List[AssemblyResult]:
        """Get history of assembly executions"""
        return self.execution_history.copy()
