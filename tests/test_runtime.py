import os
import sys
import shutil
import pytest

# Ensure projects directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from utils.yaml_parser import get_yaml_content, get_template_blocks, get_registry_list
from utils.state import get_metadata, set_metadata, set_env_var, save_env_vars
from modules.preflight import is_admin
from modules.directories import setup_directories

# Temporary test directories
TEST_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DEPLOY_DIR = os.path.join(TEST_PROJECT_ROOT, "testing_sandbox")

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setenv("TEST_MODE", "true")
    monkeypatch.setenv("DS_HEADLESS", "true")
    monkeypatch.setenv("DEPLOY_DIR", TEST_DEPLOY_DIR)
    
    os.makedirs(TEST_DEPLOY_DIR, exist_ok=True)
    yield
    # Cleanup
    if os.path.exists(TEST_DEPLOY_DIR):
        shutil.rmtree(TEST_DEPLOY_DIR, ignore_errors=True)

def test_path_resolution():
    assert resolve_path_slash("C:\\test\\path") == "C:/test/path"
    assert resolve_path_slash("D:") == "D:/"

def test_yaml_parsers():
    services_path = os.path.join(TEST_PROJECT_ROOT, "services.yml")
    template_path = os.path.join(TEST_PROJECT_ROOT, "templates.yml")
    
    assert os.path.exists(services_path)
    assert os.path.exists(template_path)
    
    master_registry = get_yaml_content(services_path)
    assert "MINIMAL" in master_registry
    assert "STACK_GROUPS" in master_registry
    
    templates = get_template_blocks(template_path)
    assert "header" in templates
    assert "sonarr" in templates

def test_metadata_read_write():
    meta = get_metadata()
    assert isinstance(meta, dict)
    
    test_data = {"test_key": "test_value", "selected_services": ["sonarr", "radarr"]}
    set_metadata(test_data)
    
    new_meta = get_metadata()
    assert new_meta["test_key"] == "test_value"
    assert "sonarr" in new_meta["selected_services"]

def test_env_file_generation():
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    set_env_var("TEST_KEY", "TEST_VAL", file_path=env_file)
    assert os.path.exists(env_file)
    
    with open(env_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "TEST_KEY=TEST_VAL" in content
    
    # Save bulk env vars
    vars_dict = {"VAR1": "VAL1", "VAR2": "VAL2\nmulti"}
    save_env_vars(vars_dict, file_path=env_file)
    
    with open(env_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "VAR1=VAL1" in content
    assert 'VAR2="VAL2\nmulti"' in content

def test_directory_setup():
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    save_env_vars({
        "DOCKERDIR": TEST_DEPLOY_DIR,
        "DRIVEPOOL": os.path.join(TEST_DEPLOY_DIR, "media")
    }, file_path=env_file)
    
    set_metadata({"selected_services": ["sonarr", "radarr"]})
    
    setup_directories()
    
    # Check that directories were created
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "appdata/sonarr/config"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "appdata/radarr/config"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "stacks"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "media/downloads"))
