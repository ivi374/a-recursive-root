"""
Role Loader - Loads and manages role definitions

Loads role definitions from YAML and provides utilities for
role management and validation.
"""

from typing import Dict, List, Optional
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)


class RoleDefinition:
    """Represents a role definition"""

    def __init__(self, role_id: str, data: Dict):
        self.role_id = role_id
        self.name = data.get("name", role_id)
        self.description = data.get("description", "")
        self.capabilities = data.get("capabilities", [])
        self.responsibilities = data.get("responsibilities", [])
        self.dependencies = data.get("dependencies", [])
        self.skills_required = data.get("skills_required", [])
        self.output_artifacts = data.get("output_artifacts", [])

    def has_capability(self, capability: str) -> bool:
        """Check if role has a specific capability"""
        return capability in self.capabilities

    def has_all_capabilities(self, capabilities: List[str]) -> bool:
        """Check if role has all specified capabilities"""
        return all(cap in self.capabilities for cap in capabilities)

    def has_any_capability(self, capabilities: List[str]) -> bool:
        """Check if role has any of the specified capabilities"""
        return any(cap in self.capabilities for cap in capabilities)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "role_id": self.role_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "responsibilities": self.responsibilities,
            "dependencies": self.dependencies,
            "skills_required": self.skills_required,
            "output_artifacts": self.output_artifacts,
        }

    def __repr__(self) -> str:
        return f"RoleDefinition({self.role_id}: {self.name})"


class RoleLoader:
    """
    Loads and manages role definitions

    Reads role definitions from YAML files and provides
    utilities for querying and managing roles.
    """

    def __init__(self, definitions_path: Optional[Path] = None):
        self.definitions_path = definitions_path or Path(__file__).parent / "role_definitions.yaml"
        self.roles: Dict[str, RoleDefinition] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_definitions()

    def _load_definitions(self):
        """Load role definitions from YAML file"""
        try:
            with open(self.definitions_path, "r") as f:
                data = yaml.safe_load(f)

            # Load roles
            roles_data = data.get("roles", {})
            for role_id, role_data in roles_data.items():
                self.roles[role_id] = RoleDefinition(role_id, role_data)

            # Load categories
            self.categories = data.get("categories", {})

            logger.info(
                f"Loaded {len(self.roles)} role definitions "
                f"in {len(self.categories)} categories"
            )

        except FileNotFoundError:
            logger.error(f"Role definitions file not found: {self.definitions_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing role definitions: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading roles: {e}")

    def get_role(self, role_id: str) -> Optional[RoleDefinition]:
        """Get a specific role definition"""
        return self.roles.get(role_id)

    def get_all_roles(self) -> List[RoleDefinition]:
        """Get all role definitions"""
        return list(self.roles.values())

    def get_roles_by_category(self, category: str) -> List[RoleDefinition]:
        """Get all roles in a category"""
        role_ids = self.categories.get(category, [])
        return [self.roles[rid] for rid in role_ids if rid in self.roles]

    def get_roles_with_capability(self, capability: str) -> List[RoleDefinition]:
        """Get all roles with a specific capability"""
        return [
            role for role in self.roles.values()
            if role.has_capability(capability)
        ]

    def get_roles_with_all_capabilities(
        self,
        capabilities: List[str]
    ) -> List[RoleDefinition]:
        """Get all roles with all specified capabilities"""
        return [
            role for role in self.roles.values()
            if role.has_all_capabilities(capabilities)
        ]

    def get_roles_with_any_capability(
        self,
        capabilities: List[str]
    ) -> List[RoleDefinition]:
        """Get all roles with any of the specified capabilities"""
        return [
            role for role in self.roles.values()
            if role.has_any_capability(capabilities)
        ]

    def search_roles(self, query: str) -> List[RoleDefinition]:
        """Search roles by name or description"""
        query_lower = query.lower()
        results = []

        for role in self.roles.values():
            if (
                query_lower in role.name.lower()
                or query_lower in role.description.lower()
                or query_lower in role.role_id.lower()
            ):
                results.append(role)

        return results

    def validate_role_dependencies(self, role_id: str) -> bool:
        """Validate that a role's dependencies exist"""
        role = self.get_role(role_id)
        if not role:
            return False

        for dep in role.dependencies:
            if dep not in self.roles:
                logger.warning(
                    f"Role {role_id} depends on non-existent role: {dep}"
                )
                return False

        return True

    def get_role_dependency_tree(self, role_id: str) -> List[str]:
        """Get full dependency tree for a role"""
        role = self.get_role(role_id)
        if not role:
            return []

        dependencies = []
        to_process = role.dependencies.copy()

        while to_process:
            dep_id = to_process.pop(0)
            if dep_id not in dependencies:
                dependencies.append(dep_id)
                dep_role = self.get_role(dep_id)
                if dep_role:
                    to_process.extend(dep_role.dependencies)

        return dependencies

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.categories.keys())

    def reload(self):
        """Reload role definitions from file"""
        self.roles.clear()
        self.categories.clear()
        self._load_definitions()

    def __len__(self) -> int:
        return len(self.roles)

    def __contains__(self, role_id: str) -> bool:
        return role_id in self.roles

    def __iter__(self):
        return iter(self.roles.values())


# Global role loader instance
_role_loader: Optional[RoleLoader] = None


def get_role_loader() -> RoleLoader:
    """Get global role loader instance"""
    global _role_loader
    if _role_loader is None:
        _role_loader = RoleLoader()
    return _role_loader


def get_role(role_id: str) -> Optional[RoleDefinition]:
    """Convenience function to get a role"""
    return get_role_loader().get_role(role_id)


def get_all_roles() -> List[RoleDefinition]:
    """Convenience function to get all roles"""
    return get_role_loader().get_all_roles()
