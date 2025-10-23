# Component Architecture - AI Council System

**Version**: 0.1.0
**Last Updated**: October 23, 2025

## Overview

This document provides detailed specifications for each major component in the AI Council System.

## 1. AI Agent System

### Responsibilities
- Execute AI agent behaviors during debates
- Maintain agent personality and memory
- Interface with multiple LLM providers
- Vote on debate outcomes

### Component Structure

```
core/agents/
├── runtime/
│   ├── agent_executor.py      # Main agent execution loop
│   ├── llm_interface.py       # LLM provider abstraction
│   └── context_manager.py     # Context window management
├── memory/
│   ├── vector_store.py        # Vector database interface
│   ├── conversation_history.py # Chat history management
│   └── knowledge_base.py      # Agent knowledge retrieval
├── personality/
│   ├── traits.py              # Personality trait definitions
│   ├── behavior_templates.py  # Behavior pattern templates
│   └── role_definitions.py    # Agent role specifications
└── voting/
    ├── decision_logic.py      # Voting decision algorithms
    ├── consensus.py           # Consensus mechanisms
    └── vote_verification.py   # Vote integrity checks
```

### Key Interfaces

#### AgentExecutor
```python
class AgentExecutor:
    def __init__(self, agent_id: str, personality: Personality, llm_provider: LLMProvider):
        """Initialize agent with personality and LLM provider"""

    async def respond(self, context: DebateContext) -> AgentResponse:
        """Generate response to debate topic"""

    async def vote(self, options: List[VoteOption]) -> Vote:
        """Cast vote on debate outcome"""

    async def update_memory(self, interaction: Interaction) -> None:
        """Update agent memory with new interaction"""
```

#### LLMInterface
```python
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM"""

    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream response from LLM"""

class ClaudeProvider(LLMProvider):
    """Anthropic Claude implementation"""

class GPTProvider(LLMProvider):
    """OpenAI GPT implementation"""

class GrokProvider(LLMProvider):
    """xAI Grok implementation"""
```

### Data Models

```python
@dataclass
class Personality:
    name: str
    traits: Dict[str, float]  # e.g., {"aggression": 0.7, "logic": 0.9}
    role: AgentRole
    background: str
    speaking_style: str

@dataclass
class AgentResponse:
    agent_id: str
    content: str
    confidence: float
    reasoning: Optional[str]
    timestamp: datetime

@dataclass
class Vote:
    agent_id: str
    option: str
    weight: float
    signature: str  # Cryptographic signature
```

### Configuration

```yaml
# agents/config.yaml
agents:
  max_concurrent: 12
  response_timeout: 10s
  memory_ttl: 7d

llm_providers:
  claude:
    model: claude-3-5-sonnet-20250219
    temperature: 0.7
    max_tokens: 1000
  gpt:
    model: gpt-4-turbo
    temperature: 0.7
    max_tokens: 1000
```

## 2. Council Manager

### Responsibilities
- Form councils based on debate topics
- Manage debate lifecycle
- Moderate debate flow
- Tally votes and determine outcomes

### Component Structure

```
core/council/
├── formation/
│   ├── council_builder.py     # Council formation logic
│   ├── agent_selector.py      # Agent selection algorithms
│   └── rng_integration.py     # RNG for randomization
├── debate/
│   ├── session_manager.py     # Debate session lifecycle
│   ├── moderator.py           # Debate flow control
│   └── turn_scheduler.py      # Agent turn scheduling
├── voting/
│   ├── vote_collector.py      # Collect votes from agents
│   ├── tally_engine.py        # Vote counting logic
│   └── outcome_resolver.py    # Determine final outcome
└── state/
    ├── council_state.py       # Council state machine
    └── debate_history.py      # Historical debate records
```

### Key Interfaces

#### CouncilBuilder
```python
class CouncilBuilder:
    async def form_council(
        self,
        topic: DebateTopic,
        size: int = 5,
        diversity: float = 0.8
    ) -> Council:
        """Form a council for given topic"""

    async def select_agents(
        self,
        pool: List[Agent],
        criteria: SelectionCriteria
    ) -> List[Agent]:
        """Select agents based on criteria"""
```

#### SessionManager
```python
class SessionManager:
    async def start_debate(self, council: Council, topic: DebateTopic) -> Session:
        """Initialize debate session"""

    async def moderate_round(self, session: Session) -> RoundResult:
        """Execute one round of debate"""

    async def conclude_debate(self, session: Session) -> DebateOutcome:
        """Finalize debate and determine outcome"""
```

### Data Models

```python
@dataclass
class Council:
    id: str
    agents: List[Agent]
    topic: DebateTopic
    formation_timestamp: datetime
    rng_seed: str  # RNG seed used for formation

@dataclass
class DebateTopic:
    id: str
    title: str
    description: str
    category: str
    context: Dict[str, Any]
    source_event: Optional[Event]

@dataclass
class Session:
    id: str
    council: Council
    state: SessionState
    rounds: List[Round]
    start_time: datetime
    end_time: Optional[datetime]

@dataclass
class DebateOutcome:
    session_id: str
    winner: Optional[str]
    vote_distribution: Dict[str, int]
    consensus_level: float
    summary: str
```

### State Machine

```
FORMING → OPENING → DEBATING → VOTING → CONCLUDED → ARCHIVED
    ↓         ↓          ↓         ↓
  ERROR    ERROR      ERROR    ERROR
```

## 3. Swarm Orchestrator

### Responsibilities
- Coordinate development swarm agents
- Assign roles and tasks
- Track assembly execution
- Aggregate results

### Component Structure

```
swarm/
├── orchestrator/
│   ├── coordinator.py         # Main orchestration logic
│   ├── task_decomposer.py     # Break down complex tasks
│   └── result_aggregator.py   # Combine agent outputs
├── roles/
│   ├── role_definitions.yaml  # Available role types
│   ├── role_assigner.py       # Assign roles to agents
│   └── capabilities.py        # Role capability definitions
├── assemblies/
│   ├── assembly_loader.py     # Load assembly definitions
│   ├── assembly_executor.py   # Execute assemblies
│   └── templates/             # Assembly templates
└── monitoring/
    ├── progress_tracker.py    # Track task progress
    └── health_checker.py      # Monitor agent health
```

### Key Interfaces

#### SwarmCoordinator
```python
class SwarmCoordinator:
    async def execute_assembly(
        self,
        assembly: Assembly,
        context: ExecutionContext
    ) -> AssemblyResult:
        """Execute a swarm assembly"""

    async def assign_roles(
        self,
        agents: List[Agent],
        requirements: RoleRequirements
    ) -> Dict[Agent, Role]:
        """Assign roles to available agents"""
```

### Data Models

```python
@dataclass
class Assembly:
    name: str
    roles: List[Role]
    workflow: Workflow
    success_criteria: SuccessCriteria

@dataclass
class Role:
    name: str
    capabilities: List[str]
    responsibilities: List[str]
    dependencies: List[str]

@dataclass
class AssemblyResult:
    assembly_name: str
    status: ExecutionStatus
    outputs: Dict[str, Any]
    agent_contributions: Dict[str, Contribution]
    duration: timedelta
```

## 4. Event Ingestion System

### Responsibilities
- Ingest events from multiple sources
- Classify and rank events
- Extract debate topics
- Maintain event queue

### Component Structure

```
core/events/
├── ingestors/
│   ├── twitter_ingestor.py    # Twitter/X API integration
│   ├── news_ingestor.py       # News API integration
│   ├── rss_ingestor.py        # RSS feed processing
│   └── webhook_ingestor.py    # Generic webhook handler
├── processing/
│   ├── classifier.py          # Event classification
│   ├── ranker.py              # Event importance ranking
│   ├── deduplicator.py        # Remove duplicate events
│   └── enricher.py            # Add context to events
├── extraction/
│   ├── topic_extractor.py     # Extract debate topics
│   ├── entity_recognizer.py   # NER for entities
│   └── sentiment_analyzer.py  # Sentiment analysis
└── queue/
    ├── event_queue.py         # Priority queue management
    └── scheduler.py           # Schedule topic selection
```

### Key Interfaces

```python
class EventIngestor(ABC):
    @abstractmethod
    async def fetch_events(self, since: datetime) -> List[RawEvent]:
        """Fetch events from source"""

    async def process_event(self, raw_event: RawEvent) -> ProcessedEvent:
        """Process and normalize event"""

class TopicExtractor:
    async def extract_topics(
        self,
        events: List[ProcessedEvent],
        limit: int = 10
    ) -> List[DebateTopic]:
        """Extract potential debate topics from events"""
```

### Data Models

```python
@dataclass
class RawEvent:
    source: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class ProcessedEvent:
    id: str
    title: str
    description: str
    category: str
    importance_score: float
    sentiment: float
    entities: List[Entity]
    source: str
    timestamp: datetime
```

## 5. Streaming Engine

### Responsibilities
- Generate audio from debate text
- Create visual representations
- Compose final stream
- Distribute to platforms

### Component Structure

```
streaming/
├── audio/
│   ├── tts_engine.py          # Text-to-speech conversion
│   ├── voice_manager.py       # Manage agent voices
│   └── audio_mixer.py         # Mix multiple audio sources
├── visuals/
│   ├── scene_generator.py     # Generate visual scenes
│   ├── avatar_renderer.py     # Render agent avatars
│   └── overlay_composer.py    # Add overlays (votes, etc.)
├── broadcast/
│   ├── stream_composer.py     # Compose final stream
│   ├── encoder.py             # Video encoding (FFmpeg)
│   └── distributor.py         # Multi-platform distribution
└── obs/
    ├── obs_controller.py      # OBS WebSocket control
    └── scene_manager.py       # OBS scene management
```

### Key Interfaces

```python
class StreamComposer:
    async def compose_frame(
        self,
        debate_state: DebateState,
        audio: AudioBuffer,
        visuals: VisualFrame
    ) -> StreamFrame:
        """Compose single stream frame"""

    async def start_broadcast(
        self,
        session: Session,
        platforms: List[Platform]
    ) -> BroadcastHandle:
        """Start broadcasting session"""
```

## 6. Blockchain Interface

### Responsibilities
- Manage token operations
- Execute smart contracts
- Verify RNG commitments
- Handle wallet connections

### Component Structure

```
blockchain/
├── contracts/
│   ├── CouncilToken.sol       # ERC-20 token contract
│   ├── VotingManager.sol      # Vote recording contract
│   ├── RNGOracle.sol          # RNG verification contract
│   └── Treasury.sol           # Token treasury management
├── rng/
│   ├── chainlink_vrf.py       # Chainlink VRF integration
│   ├── pyth_entropy.py        # Pyth Entropy integration
│   └── verifier.py            # RNG verification logic
├── token/
│   ├── token_manager.py       # Token operations
│   ├── rewards.py             # Reward distribution
│   └── staking.py             # Token staking logic
└── wallet/
    ├── wallet_connector.py    # Wallet connection handling
    └── transaction_signer.py  # Transaction signing
```

### Smart Contract Interfaces

```solidity
// CouncilToken.sol
interface ICouncilToken {
    function mint(address to, uint256 amount) external;
    function burn(address from, uint256 amount) external;
    function stake(uint256 amount) external;
    function unstake(uint256 amount) external;
}

// VotingManager.sol
interface IVotingManager {
    function recordVote(
        bytes32 sessionId,
        address voter,
        uint8 option,
        bytes calldata signature
    ) external;

    function getResults(bytes32 sessionId)
        external
        view
        returns (uint256[] memory);
}

// RNGOracle.sol
interface IRNGOracle {
    function requestRandomness(uint256 seed)
        external
        returns (bytes32 requestId);

    function fulfillRandomness(
        bytes32 requestId,
        uint256 randomness
    ) external;
}
```

## 7. Web Application

### Responsibilities
- Display live streams
- User authentication
- Wallet integration
- Council interaction UI

### Component Structure

```
web/
├── frontend/
│   ├── app/                   # Next.js app router
│   ├── components/            # React components
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                   # Utility libraries
│   └── styles/                # Tailwind styles
├── backend/
│   ├── api/                   # API routes
│   ├── services/              # Business logic
│   ├── middleware/            # Express middleware
│   └── websocket/             # WebSocket handlers
└── api/
    ├── councils/              # Council API endpoints
    ├── streams/               # Streaming API endpoints
    └── auth/                  # Authentication endpoints
```

### Key React Components

```typescript
// StreamViewer.tsx
interface StreamViewerProps {
  sessionId: string;
  onVote?: (option: string) => void;
}

// CouncilCard.tsx
interface CouncilCardProps {
  council: Council;
  session: Session;
  isLive: boolean;
}

// VotingInterface.tsx
interface VotingInterfaceProps {
  options: VoteOption[];
  userTokenBalance: number;
  onSubmitVote: (option: string, amount: number) => Promise<void>;
}
```

## Component Communication

### API Patterns

1. **REST API**: Synchronous operations (CRUD)
2. **WebSocket**: Real-time updates (debate state, votes)
3. **Message Queue**: Asynchronous processing (event ingestion)
4. **gRPC**: Internal service communication (future)

### Event Bus

```python
class EventBus:
    """Central event bus for component communication"""

    async def publish(self, event: Event) -> None:
        """Publish event to subscribers"""

    async def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], Awaitable[None]]
    ) -> None:
        """Subscribe to event type"""
```

### Key Events

- `CouncilFormed`: New council created
- `DebateStarted`: Debate session started
- `AgentResponded`: Agent posted response
- `VoteCast`: Vote submitted
- `DebateConcluded`: Debate finished
- `TokensDistributed`: Rewards distributed

## Inter-Component Dependencies

```
Event Ingestor → Council Manager → AI Agents → Streaming Engine
                       ↓               ↓
                 Blockchain      ← Web App →  User
                       ↓
                 RNG Oracle
```

## Performance Considerations

### Agent System
- Connection pooling for LLM APIs
- Response caching for similar prompts
- Parallel agent execution

### Council Manager
- State persistence for recovery
- Optimistic locking for concurrent updates
- Database indexing on council_id, session_id

### Event Ingestion
- Rate limiting per source
- Batch processing
- Event deduplication with bloom filters

### Streaming
- Buffer management (2-5 second buffer)
- Adaptive bitrate streaming
- CDN edge caching

## Monitoring & Observability

Each component exposes:
- Health check endpoint (`/health`)
- Metrics endpoint (`/metrics`)
- Structured logging (JSON)
- Distributed tracing (OpenTelemetry)

---

**Related Documents**:
- [System Architecture](./system-architecture.md)
- [Data Flow Diagrams](./data-flows.md)
- [API Specifications](../api/README.md)
