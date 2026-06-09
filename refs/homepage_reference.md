# Homepage Configuration & Layout Reference

This document serves as a reference for configuring the Homepage dashboard (`gethomepage.dev`), specifically focusing on layout management, grouping, and ordering.

## Core Concepts

Homepage uses YAML files located in its `config` directory to define its behavior. The two primary files relevant to layout are:
- `services.yaml`: Defines the actual services, their URLs, and widget configurations.
- `settings.yaml`: Controls the global application settings and the visual layout (rows, columns, ordering) of the groups defined in `services.yaml` and `bookmarks.yaml`.

## Layout Configuration (`settings.yaml`)

By default, Homepage arranges groups vertically in columns. To force groups into horizontal rows and control their exact order, you must use the `layout` block in `settings.yaml`.

### 1. Forcing Horizontal Rows

To make a group render as a horizontal row, you map the group's exact name (as defined in `services.yaml`) under the `layout` block and assign it `style: row`. You can also specify the maximum number of `columns` (widgets per row) before wrapping.

```yaml
# settings.yaml
layout:
  "Media Server":
    style: row
    columns: 4
```

### 2. Group Ordering

The order of groups rendered on the Homepage is strictly determined by their top-to-bottom order within the `layout` block in `settings.yaml`. 

*Note: Any group defined in `services.yaml` but missing from the `layout` block will be automatically appended to the bottom of the page in a default vertical column.*

**Example:**
```yaml
# settings.yaml
layout:
  - "Media Server":
      style: row
      columns: 4
  - "Media PVR":
      style: row
      columns: 4
  - "Downloaders":
      style: row
      columns: 4
  - "Maintenance":
      style: row
      columns: 4
```

### 3. Global Layout Settings

To ensure the rows utilize the full width of modern monitors (preventing widgets from squishing together in the center), you should enable the `fullWidth` property globally.

```yaml
# settings.yaml (top level)
title: "Home Server Dashboard"
favicon: "https://homepage.dev/favicon.ico"
theme: dark
fullWidth: true  # Make rows span the whole screen
```

## Strategy for DockerSetup

When dynamically generating the Homepage configuration in `compose_build.py`:

1.  **Generate `services.yaml`**: This file will map the selected apps to their respective stack groups (e.g., `media-server`, `media-pvr`).
2.  **Generate `settings.yaml`**: We must also dynamically write a `settings.yaml` to the Homepage config directory that explicitly defines the `layout` block. We will iterate through the configured stacks in the required order (`media-server`, `media-pvr`, `downloaders`, `maintenance`, plus any others) and assign `style: row`.

## Additional Configurations

### Services (`services.yaml`)
Services are the core clickable items on the dashboard, mapped to containers and URLs.
- **Structure:** Defined as a list of groups containing a list of service objects. Nesting is supported.
- **Key Attributes:** `icon`, `href`, `description`, `ping` (for health checks).
- **Service Widgets:** Live data from third-party APIs (like Sonarr or Plex) can be attached directly to a service definition via the `widget` property.

### Information Widgets (`widgets.yaml`)
Global widgets that display at the top of the dashboard for system-level or generic data.
- **Display Order:** Rendered in the exact order they are listed in the file. Some widgets (like weather or time) align to the right by default.
- **Examples:** Logo, Search, Weather, Resources (CPU/RAM), GitHub statistics, Date/Time.

### Docker Integration (`docker.yaml`)
Allows Homepage to query Docker directly to display container states and resource usage.
- **Connection Methods:** Can use `/var/run/docker.sock` directly (if root), a TCP API, or a secure proxy (`docker-socket-proxy`).
- **Mapping:** Use `server` and `container` attributes in `services.yaml` to link a dashboard item to its corresponding live container data.
- **Auto-Discovery:** By applying `homepage.*` labels to your Docker containers, Homepage can automatically populate them on the dashboard without manual entries in `services.yaml`.

### Bookmarks (`bookmarks.yaml`)
Smaller, simplified links that exist separately from Services.
- **Limitations:** Cannot host Service Widgets or ping monitors.
- **Structure:** Configured similarly to services (groups of links), but optimized for simple URL redirection. Often used for external sites or static reference material.

---
*Reference generated from gethomepage.dev documentation.*