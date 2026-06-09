import os
import sys
import shutil
import pytest
from unittest.mock import MagicMock, patch

# Ensure projects directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from src.utils.yaml_parser import get_yaml_content, get_template_blocks, get_registry_list
from src.utils.state import get_metadata, set_metadata, set_env_var, save_env_vars
from src.modules.preflight import is_admin
from src.modules.directories import setup_directories

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
    services_path = os.path.join(TEST_PROJECT_ROOT, "resources", "services.yml")
    template_path = os.path.join(TEST_PROJECT_ROOT, "resources", "templates.yml")
    
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

def test_timezone_detection():
    from src.modules.env_wizard import detect_timezone, select_timezone_interactive
    
    # 1. Test detect_timezone returns a string (not None or "None")
    tz = detect_timezone()
    assert tz is not None
    assert tz != "None"
    
    # 2. Test select_timezone_interactive behaves correctly in headless mode
    interactive_tz = select_timezone_interactive(tz)
    assert interactive_tz is not None
    assert interactive_tz != "None"
    
    # 3. Test that None/"None" input fallback logic resolves to a valid timezone/UTC
    fallback_tz = select_timezone_interactive("None")
    assert fallback_tz is not None
    assert fallback_tz != "None"

def test_compose_build_integration():
    from src.modules.compose_build import build_compose_stacks
    
    # 1. Setup metadata
    set_metadata({
        "selected_services": ["sonarr", "radarr", "homepage"],
        "tier": "1"
    })
    
    # 2. Setup master .env
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    save_env_vars({
        "PUID": "1000",
        "PGID": "1000",
        "TZ": "UTC",
        "DOCKERDIR": TEST_DEPLOY_DIR,
        "DRIVEPOOL": os.path.join(TEST_DEPLOY_DIR, "media"),
        "USERDIR": TEST_DEPLOY_DIR,
        "HTTP_USERNAME": "admin",
        "HTTP_PASSWORD": "password"
    }, file_path=env_file)
    
    # 3. Run build
    assert build_compose_stacks() is True
    
    # 4. Verify output
    stack_dir = os.path.join(TEST_DEPLOY_DIR, "stacks", "media-pvr")
    assert os.path.exists(stack_dir)
    assert os.path.exists(os.path.join(stack_dir, "docker-compose.yml"))
    assert os.path.exists(os.path.join(stack_dir, ".env"))
    
    with open(os.path.join(stack_dir, "docker-compose.yml"), "r") as f:
        content = f.read()
    assert "sonarr" in content
    assert "radarr" in content
    
    with open(os.path.join(stack_dir, ".env"), "r") as f:
        env_content = f.read()
    assert "PUID=1000" in env_content
    # HTTP_PASSWORD should be filtered out from PVR stack as it's not used in its compose
    assert "HTTP_PASSWORD" not in env_content

    # 5. Verify Homepage configuration files
    hp_config_dir = os.path.join(TEST_DEPLOY_DIR, "appdata", "homepage", "config")
    assert os.path.exists(os.path.join(hp_config_dir, "bookmarks.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "docker.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "widgets.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "settings.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "services.yaml"))

@patch("src.modules.auto_configure.wait_for_service")
@patch("requests.Session.request")
def test_auto_stitch_integration(mock_request, mock_wait):
    from src.modules.auto_configure import auto_stitch_services
    
    mock_wait.return_value = True
    
    # Mock API responses
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_request.return_value = mock_response
    
    # Setup files
    set_metadata({"selected_services": ["sonarr", "prowlarr"]})
    deploy_dir = TEST_DEPLOY_DIR
    
    # Mock sonarr config
    sonarr_cfg_path = os.path.join(deploy_dir, "appdata", "sonarr", "config", "config.xml")
    os.makedirs(os.path.dirname(sonarr_cfg_path), exist_ok=True)
    with open(sonarr_cfg_path, "w") as f:
        f.write("<Config><ApiKey>testkey</ApiKey></Config>")
        
    # Mock prowlarr config
    prowl_cfg_path = os.path.join(deploy_dir, "appdata", "prowlarr", "config", "config.xml")
    os.makedirs(os.path.dirname(prowl_cfg_path), exist_ok=True)
    with open(prowl_cfg_path, "w") as f:
        f.write("<Config><ApiKey>prowlkey</ApiKey></Config>")
        
    env_file = os.path.join(deploy_dir, ".env")
    save_env_vars({"HTTP_PASSWORD": "testpassword"}, file_path=env_file)
    
    # Run stitching
    assert auto_stitch_services() is True
    
    # Verify mock calls (should have attempted to auth sonarr and link prowlarr)
    assert mock_request.called
    
    # Verify metadata update
    meta = get_metadata()
    assert "auto_config_results" in meta
    assert len(meta["auto_config_results"]) > 0

@patch("src.modules.deploy_start.invoke_external_command")
@patch("src.modules.deploy_start.subprocess.run")
@patch("src.modules.deploy_start.test_container_conflict")
def test_deploy_stacks_success(mock_conflict, mock_run, mock_invoke):
    from src.modules.deploy_start import deploy_stacks
    
    # Mock subprocess run to succeed
    mock_run.return_value = MagicMock(returncode=0, stdout="Success")
    mock_invoke.return_value = None
    
    # Setup deployment directory and files
    set_metadata({
        "generated_stacks": [
            {"Name": "core"},
            {"Name": "media-server"}
        ]
    })
    
    stacks_dir = os.path.join(TEST_DEPLOY_DIR, "stacks")
    os.makedirs(os.path.join(stacks_dir, "core"), exist_ok=True)
    os.makedirs(os.path.join(stacks_dir, "media-server"), exist_ok=True)
    
    # Execute deploy
    assert deploy_stacks() is True
    assert mock_run.called

@patch("src.modules.deploy_start.invoke_external_command")
@patch("src.modules.deploy_start.subprocess.run")
@patch("src.modules.deploy_start.test_container_conflict")
def test_deploy_stacks_pull_failure(mock_conflict, mock_run, mock_invoke):
    from src.modules.deploy_start import deploy_stacks
    mock_invoke.return_value = None
    
    # Mock subprocess run to fail on pull
    def run_side_effect(args, **kwargs):
        if "pull" in args:
            raise subprocess.CalledProcessError(1, args)
        return MagicMock(returncode=0, stdout="Success")
        
    mock_run.side_effect = run_side_effect
    
    set_metadata({
        "generated_stacks": [
            {"Name": "core"},
            {"Name": "media-server"}
        ]
    })
    
    stacks_dir = os.path.join(TEST_DEPLOY_DIR, "stacks")
    os.makedirs(os.path.join(stacks_dir, "core"), exist_ok=True)
    os.makedirs(os.path.join(stacks_dir, "media-server"), exist_ok=True)
    
    # Under headless mode, pull failures must raise RuntimeError
    import subprocess
    with pytest.raises(RuntimeError):
        deploy_stacks()

@patch("src.utils.uninstall.subprocess.run")
@patch("questionary.confirm")
def test_uninstall_workflow(mock_confirm, mock_run):
    from src.utils.uninstall import main as uninstall_main
    
    # Setup environment
    os.environ["DEPLOY_DIR"] = TEST_DEPLOY_DIR
    
    # Write mock files to satisfy the validation checks in uninstall
    os.makedirs(os.path.join(TEST_DEPLOY_DIR, "stacks"), exist_ok=True)
    with open(os.path.join(TEST_DEPLOY_DIR, ".metadata.json"), "w") as f:
        f.write("{}")
    with open(os.path.join(TEST_DEPLOY_DIR, ".env"), "w") as f:
        f.write("HTTP_PASSWORD=test")
        
    # Mock user input: confirmation to proceed and deletion of volumes
    mock_confirm.return_value = MagicMock(ask=lambda: True)
    mock_run.return_value = MagicMock(returncode=0)
    
    # Run uninstall main
    try:
        uninstall_main()
    except SystemExit as e:
        assert e.code == 0
        
    # Verify cleanup occurred
    assert not os.path.exists(os.path.join(TEST_DEPLOY_DIR, "stacks"))
    assert not os.path.exists(os.path.join(TEST_DEPLOY_DIR, ".metadata.json"))

def test_ast_and_syntax_validation():
    """
    Ensure all Python source files in the project are syntactically valid by parsing them with built-in ast.
    """
    import ast
    project_root = TEST_PROJECT_ROOT
    python_files = []
    
    # Traverse directories to find python files
    for root, _, files in os.walk(project_root):
        if ".venv" in root or ".pytest_cache" in root or "build" in root or "dist" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
                
    assert len(python_files) > 0, "No Python source files found to validate."
    
    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source, filename=py_file)
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")

def test_yaml_integrity_and_schema():
    """
    Ensure templates.yml and services.yml are well-formed and meet basic structure rules.
    """
    services_path = os.path.join(TEST_PROJECT_ROOT, "resources", "services.yml")
    template_path = os.path.join(TEST_PROJECT_ROOT, "resources", "templates.yml")
    
    # Verify both exist
    assert os.path.exists(services_path), "services.yml is missing"
    assert os.path.exists(template_path), "templates.yml is missing"
    
    # Check services.yml structure
    services_data = get_yaml_content(services_path)
    assert isinstance(services_data, dict), "services.yml must parse to a dict"
    
    # Must have categories/tiers
    required_keys = ["MINIMAL", "MANAGEMENT", "NETWORKING", "DATABASE", "REMOTE", "TOOLS", "GAMES", "STACK_GROUPS"]
    for rk in required_keys:
        assert rk in services_data, f"Required category/section '{rk}' missing in services.yml"
        
    # Check templates.yml structure
    templates_data = get_template_blocks(template_path)
    assert isinstance(templates_data, dict), "templates.yml must parse to a dictionary"
    assert "header" in templates_data, "templates.yml must have a 'header' block defined"
    
    # Verify that all selected services in services.yml actually have templates in templates.yml
    registry_list = get_registry_list(services_data)
    for svc in registry_list:
        if svc.key != "divider":
            assert svc.key in templates_data, f"Service '{svc.key}' is defined in services.yml but has no template in templates.yml"

def test_strict_path_normalization_invariant():
    """
    Verify path normalization ensures forward slashes exclusively on Windows or other OS.
    """
    # Windows paths with backslashes
    assert resolve_path_slash("C:\\docker\\stacks") == "C:/docker/stacks"
    assert resolve_path_slash("appdata\\sonarr\\config") == "appdata/sonarr/config"
    assert resolve_path_slash("\\\\network-share\\share") == "//network-share/share"
    # Empty and invalid cases
    assert resolve_path_slash("") == ""
    assert resolve_path_slash(None) is None
    
    # Windows drives
    assert resolve_path_slash("D:") == "D:/"
    assert resolve_path_slash("z:") == "z:/"



