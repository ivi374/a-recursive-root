"""
Assembly Loader - Loads assembly definitions from YAML templates

Loads and validates assembly definitions that define swarm workflows
for specific tasks.
"""

from typing import Dict, List, Optional
from pathlib import Path
from datetime import timedelta
import yaml
import logging

logger = logging.getLogger(__name__)


class AssemblyDefinition:
    """Represents an assembly definition"""

    def __init__(self, data: Dict):
        self.name = data.get("name", "")
        self.version = data.get("version", "1.0.0")
        self.description = data.get("description", "")
        self.roles = data.get("roles", [])
        self.workflow = data.get("workflow", {})
        self.success_criteria = data.get("success_criteria", {})
        self.metadata = data.get("metadata", {})

    def validate(self) -> tuple[bool, List[str]]:
        """Validate assembly definition"""
        errors = []

        if not self.name:
            errors.append("Assembly must have a name")

        if not self.roles:
            errors.append("Assembly must define at least one role")

        if not self.workflow:
            errors.append("Assembly must define a workflow")

        if not self.success_criteria:
            errors.append("Assembly must define success criteria")

        # Validate workflow steps
        steps = self.workflow.get("steps", [])
        if not steps:
            errors.append("Workflow must have at least one step")

        # Check that all step roles are defined
        defined_roles = {role.get("name") for role in self.roles}
        for step in steps:
            step_role = step.get("role")
            if step_role not in defined_roles:
                errors.append(f"Step references undefined role: {step_role}")

        # Validate success criteria
        if "required_outputs" not in self.success_criteria:
            errors.append("Success criteria must define required_outputs")

        return len(errors) == 0, errors

    def get_role_names(self) -> List[str]:
        """Get list of role names in this assembly"""
        return [role.get("name") for role in self.roles]

    def get_estimated_duration(self) -> Optional[str]:
        """Get estimated duration from metadata"""
        return self.metadata.get("estimated_duration")

    def get_tags(self) -> List[str]:
        """Get tags from metadata"""
        return self.metadata.get("tags", [])

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "roles": self.roles,
            "workflow": self.workflow,
            "success_criteria": self.success_criteria,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"AssemblyDefinition({self.name} v{self.version})"


class AssemblyLoader:
    """
    Loads and manages assembly definitions

    Reads assembly definitions from YAML template files and
    provides utilities for querying and managing assemblies.
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent / "templates"
        self.assemblies: Dict[str, AssemblyDefinition] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all assembly templates from directory"""
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            return

        template_files = list(self.templates_dir.glob("*.yaml")) + \
                        list(self.templates_dir.glob("*.yml"))

        for template_file in template_files:
            try:
                self._load_template(template_file)
            except Exception as e:
                logger.error(f"Error loading template {template_file}: {e}")

        logger.info(f"Loaded {len(self.assemblies)} assembly templates")

    def _load_template(self, template_path: Path):
        """Load a single assembly template"""
        try:
            with open(template_path, "r") as f:
                data = yaml.safe_load(f)

            assembly = AssemblyDefinition(data)

            # Validate assembly
            is_valid, errors = assembly.validate()
            if not is_valid:
                logger.error(
                    f"Invalid assembly {assembly.name}: {', '.join(errors)}"
                )
                return

            self.assemblies[assembly.name] = assembly
            logger.debug(f"Loaded assembly: {assembly.name}")

        except yaml.YAMLError as e:
            logger.error(f"YAML error in {template_path}: {e}")
        except Exception as e:
            logger.error(f"Error loading {template_path}: {e}")

    def get_assembly(self, name: str) -> Optional[AssemblyDefinition]:
        """Get assembly definition by name"""
        return self.assemblies.get(name)

    def get_all_assemblies(self) -> List[AssemblyDefinition]:
        """Get all assembly definitions"""
        return list(self.assemblies.values())

    def get_assemblies_by_tag(self, tag: str) -> List[AssemblyDefinition]:
        """Get assemblies with specific tag"""
        return [
            assembly for assembly in self.assemblies.values()
            if tag in assembly.get_tags()
        ]

    def search_assemblies(self, query: str) -> List[AssemblyDefinition]:
        """Search assemblies by name or description"""
        query_lower = query.lower()
        results = []

        for assembly in self.assemblies.values():
            if (
                query_lower in assembly.name.lower()
                or query_lower in assembly.description.lower()
            ):
                results.append(assembly)

        return results

    def list_assembly_names(self) -> List[str]:
        """Get list of all assembly names"""
        return list(self.assemblies.keys())

    def reload(self):
        """Reload all assembly templates"""
        self.assemblies.clear()
        self._load_templates()

    def add_assembly(self, assembly: AssemblyDefinition) -> bool:
        """Add or update an assembly definition"""
        is_valid, errors = assembly.validate()
        if not is_valid:
            logger.error(f"Cannot add invalid assembly: {', '.join(errors)}")
            return False

        self.assemblies[assembly.name] = assembly
        logger.info(f"Added assembly: {assembly.name}")
        return True

    def remove_assembly(self, name: str) -> bool:
        """Remove an assembly definition"""
        if name in self.assemblies:
            del self.assemblies[name]
            logger.info(f"Removed assembly: {name}")
            return True
        return False

    def __len__(self) -> int:
        return len(self.assemblies)

    def __contains__(self, name: str) -> bool:
        return name in self.assemblies

    def __iter__(self):
        return iter(self.assemblies.values())


# Global assembly loader instance
_assembly_loader: Optional[AssemblyLoader] = None


def get_assembly_loader() -> AssemblyLoader:
    """Get global assembly loader instance"""
    global _assembly_loader
    if _assembly_loader is None:
        _assembly_loader = AssemblyLoader()
    return _assembly_loader


def get_assembly(name: str) -> Optional[AssemblyDefinition]:
    """Convenience function to get an assembly"""
    return get_assembly_loader().get_assembly(name)


def get_all_assemblies() -> List[AssemblyDefinition]:
    """Convenience function to get all assemblies"""
    return get_assembly_loader().get_all_assemblies()
