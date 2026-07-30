"""
Callibr Engineering Knowledge Graph

Relie les checks, capabilities, ADR, AEB, packages, fichiers et classes.
Quand un check echoue, il fournit tout son contexte automatiquement.
"""

from dataclasses import dataclass, field


@dataclass
class KnowledgeNode:
    id: str
    kind: str  # "check", "capability", "adr", "aeb_volume", "package", "module", "class"
    label: str
    metadata: dict = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    source: str
    target: str
    relation: str  # "validates", "implements", "decides", "contains", "depends_on"


class KnowledgeGraph:
    def __init__(self):
        self.nodes: dict[str, KnowledgeNode] = {}
        self.edges: list[KnowledgeEdge] = []
        self._build_graph()

    def _build_graph(self):
        self._add_capabilities()
        self._add_adrs()
        self._add_aeb_volumes()
        self._add_packages()
        self._add_checks()
        self._add_edges()

    def _add_node(self, node: KnowledgeNode):
        self.nodes[node.id] = node

    def _add_edge(self, edge: KnowledgeEdge):
        self.edges.append(edge)

    def _add_capabilities(self):
        caps = [
            ("cap-simulation", "SIMULATION", "B02, B08, C01"),
            ("cap-crm", "CRM", "B07"),
            ("cap-evaluation", "EVALUATION", "B09"),
            ("cap-reporting", "REPORTING", "B10"),
            ("cap-identity", "IDENTITY", "C03, J01"),
            ("cap-iam", "IAM", "J01-J03"),
            ("cap-ai", "AI Runtime", "B03, E01-E06, H01-H15"),
            ("cap-scenario", "SCENARIO", "B05"),
            ("cap-session", "SESSION", "B02, B08"),
            ("cap-orchestration", "ORCHESTRATION", "C01, C02"),
            ("cap-procedure", "PROCEDURE", "B05, B06"),
            ("cap-persona", "PERSONA", "B04"),
            ("cap-rule", "RULE", "B06"),
            ("cap-analytics", "ANALYTICS", "B10, I11-I20"),
            ("cap-multi-tenant", "MULTI-TENANT", "C03"),
            ("cap-observability", "OBSERVABILITY", "K07, H10"),
            ("cap-domain-packs", "DOMAIN PACKS", "G00-G20"),
        ]
        for cap_id, label, volumes in caps:
            self._add_node(
                KnowledgeNode(
                    id=cap_id,
                    kind="capability",
                    label=label,
                    metadata={"aeb_volumes": volumes},
                )
            )

    def _add_adrs(self):
        adrs = [
            (
                "adr-0001",
                "ADR-0001 PostgreSQL",
                {"packages": ["packages/persistence"], "status": "accepted"},
            ),
            ("adr-0002", "ADR-0002 FastAPI", {"packages": ["apps/api"], "status": "accepted"}),
            ("adr-0003", "ADR-0003 Hexagonal", {"packages": ["*"], "status": "accepted"}),
            ("adr-0004", "ADR-0004 Monorepo", {"packages": ["*"], "status": "accepted"}),
            ("adr-0005", "ADR-0005 Vertical Slice", {"packages": ["*"], "status": "accepted"}),
            (
                "adr-0006",
                "ADR-0006 Pydantic",
                {"packages": ["packages/contracts"], "status": "accepted"},
            ),
            (
                "adr-0007",
                "ADR-0007 Alembic",
                {"packages": ["packages/persistence"], "status": "accepted"},
            ),
        ]
        for adr_id, label, meta in adrs:
            self._add_node(
                KnowledgeNode(
                    id=adr_id,
                    kind="adr",
                    label=label,
                    metadata=meta,
                )
            )

    def _add_aeb_volumes(self):
        volumes = [
            ("aeb-b02", "B02 — Simulation Operating Engine"),
            ("aeb-b03", "B03 — AI Runtime Architecture"),
            ("aeb-b04", "B04 — Customer Persona Engine"),
            ("aeb-b05", "B05 — Scenario & Procedure Engine"),
            ("aeb-b06", "B06 — Rule & Decision Engine"),
            ("aeb-b07", "B07 — CRM Runtime Engine"),
            ("aeb-b08", "B08 — Conversation Runtime Engine"),
            ("aeb-b09", "B09 — Evaluation & Quality Intelligence"),
            ("aeb-b10", "B10 — Analytics & Coaching Platform"),
            ("aeb-c01", "C01 — ATOS Kernel"),
            ("aeb-c02", "C02 — Event Bus & CQRS"),
            ("aeb-c03", "C03 — Multi-Tenant SaaS Architecture"),
            ("aeb-i02", "I02 — Tenant Isolation"),
        ]
        for vol_id, label in volumes:
            self._add_node(KnowledgeNode(id=vol_id, kind="aeb_volume", label=label))

    def _add_packages(self):
        pkgs = [
            ("pkg-kernel", "packages/kernel", ["callibr_kernel"]),
            ("pkg-contracts", "packages/contracts", ["callibr_contracts"]),
            ("pkg-persistence", "packages/persistence", ["callibr_persistence"]),
            ("pkg-telemetry", "packages/telemetry", ["callibr_telemetry"]),
            ("pkg-shared", "packages/shared", ["callibr_shared"]),
            ("pkg-identity", "platform/identity", ["callibr_identity"]),
            ("pkg-api", "apps/api", ["callibr_api"]),
            ("pkg-frontend", "apps/frontend", []),
            ("pkg-simulation", "engines/simulation", ["callibr_simulation"]),
            ("pkg-crm", "engines/crm", ["callibr_crm"]),
            ("pkg-evaluation", "engines/evaluation", ["callibr_evaluation"]),
            ("pkg-scenario", "engines/scenario", ["callibr_scenario"]),
        ]
        for pkg_id, path, modules in pkgs:
            self._add_node(
                KnowledgeNode(
                    id=pkg_id,
                    kind="package",
                    label=path,
                    metadata={"modules": modules},
                )
            )

    def _add_checks(self):
        checks = [
            ("chk-arch-layers", "Architecture Layer Validation", "architecture", "CRITIQUE"),
            ("chk-arch-contracts", "Contracts Independence", "architecture", "HAUTE"),
            ("chk-arch-kernel", "Kernel Independence", "architecture", "HAUTE"),
            ("chk-tenant-isolation", "Tenant Isolation", "securite", "CRITIQUE"),
            ("chk-secrets", "Hardcoded Secrets", "securite", "CRITIQUE"),
            ("chk-lint", "Code Quality (ruff)", "qualite", "MOYENNE"),
            ("chk-typage", "Type Safety (mypy)", "qualite", "MOYENNE"),
            ("chk-tests", "Test Coverage", "qualite", "HAUTE"),
            ("chk-todos", "TODO Left Behind", "dette", "BASSE"),
            ("chk-pass", "Incomplete Implementation", "dette", "MOYENNE"),
            ("chk-migrations", "Database Migrations", "infrastructure", "HAUTE"),
            ("chk-capabilities", "Capability Completeness", "fonctionnel", "HAUTE"),
        ]
        for chk_id, label, category, severity in checks:
            self._add_node(
                KnowledgeNode(
                    id=chk_id,
                    kind="check",
                    label=label,
                    metadata={"category": category, "severity": severity},
                )
            )

    def _add_edges(self):
        self._add_edge(KnowledgeEdge("chk-arch-layers", "cap-orchestration", "validates"))
        self._add_edge(KnowledgeEdge("chk-arch-layers", "adr-0003", "enforces"))
        self._add_edge(KnowledgeEdge("chk-arch-layers", "aeb-c01", "references"))
        self._add_edge(KnowledgeEdge("chk-arch-layers", "pkg-simulation", "validates"))
        self._add_edge(KnowledgeEdge("chk-arch-contracts", "pkg-contracts", "validates"))
        self._add_edge(KnowledgeEdge("chk-arch-contracts", "adr-0006", "enforces"))
        self._add_edge(KnowledgeEdge("chk-arch-kernel", "pkg-kernel", "validates"))
        self._add_edge(KnowledgeEdge("chk-arch-kernel", "aeb-c01", "references"))
        self._add_edge(KnowledgeEdge("chk-tenant-isolation", "cap-multi-tenant", "validates"))
        self._add_edge(KnowledgeEdge("chk-tenant-isolation", "adr-0001", "enforces"))
        self._add_edge(KnowledgeEdge("chk-tenant-isolation", "aeb-i02", "references"))
        self._add_edge(KnowledgeEdge("chk-tenant-isolation", "pkg-scenario", "inspects"))
        self._add_edge(KnowledgeEdge("chk-secrets", "cap-iam", "validates"))
        self._add_edge(KnowledgeEdge("chk-secrets", "aeb-c03", "references"))
        self._add_edge(KnowledgeEdge("chk-migrations", "adr-0007", "enforces"))
        self._add_edge(KnowledgeEdge("chk-migrations", "pkg-persistence", "validates"))
        self._add_edge(KnowledgeEdge("chk-capabilities", "cap-simulation", "validates"))
        self._add_edge(KnowledgeEdge("chk-capabilities", "cap-crm", "validates"))
        self._add_edge(KnowledgeEdge("chk-capabilities", "cap-evaluation", "validates"))
        self._add_edge(KnowledgeEdge("chk-capabilities", "cap-scenario", "validates"))

    def get_context(self, check_id: str) -> dict:
        result = {
            "check": None,
            "capabilities": [],
            "adrs": [],
            "aeb_volumes": [],
            "packages": [],
        }

        if check_id in self.nodes:
            result["check"] = self.nodes[check_id]

        for edge in self.edges:
            if edge.source == check_id:
                target = self.nodes.get(edge.target)
                if target:
                    if target.kind == "capability":
                        result["capabilities"].append(target)
                    elif target.kind == "adr":
                        result["adrs"].append(target)
                    elif target.kind == "aeb_volume":
                        result["aeb_volumes"].append(target)
                    elif target.kind == "package":
                        result["packages"].append(target)

        return result

    def get_check_for_file(self, filepath: str) -> list[str]:
        checks = []
        for edge in self.edges:
            if edge.relation == "inspects":
                target = self.nodes.get(edge.target)
                if target and target.kind == "package":
                    pkg_path = target.label
                    if pkg_path in filepath:
                        checks.append(edge.source)
        return checks


knowledge_graph = KnowledgeGraph()
