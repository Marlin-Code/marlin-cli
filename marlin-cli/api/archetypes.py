ARCHETYPE_MAP = {
  "react-js": {
    "creator": "Marlin",
    "description": "desc",
    "documentation_url": "https://marlincode.notion.site/Jumpstart-Your-Frontend-3788900c2f2843a29da725fbbb3d6aa1",
    "repository": {
      "owner": "Marlin-Code",
      "repo_name": "react_frontend_module",
      "version": "1.0.0"
    }
  },
  "serverless-api": {
    "creator": "Marlin",
    "description": "desc",
    "documentation_url": "https://marlincode.notion.site/Jumpstart-Your-API-3f51845ff96d46c78ceefef89a5b71c8",
    "repository": {
      "owner": "Marlin-Code",
      "repo_name": "serverless-api",
      "version": "1.0.0"
    }
  }
}

def get_archetype(archetype_name):
  return ARCHETYPE_MAP.get(archetype_name)