from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class BaseApp:
    key: str = ""
    name: str = ""
    port: int = 0
    category: str = ""
    description: str = ""
    stack_group: str = ""
    recommendations: List[str] = []
    is_configurable: bool = True
    has_widget: bool = False
    config_model: Optional[type[BaseModel]] = None

    def get_compose_template(self) -> str:
        """Returns the Docker Compose YAML template string for this service."""
        return ""

    def run_stitching(self, keys: Dict[str, str], deploy_dir: str, rest_invoker) -> List[str]:
        """Runs custom stitching or setup actions. Returns a list of result strings."""
        return []
