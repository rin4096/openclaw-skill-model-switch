import json
import os
import sys

# Path to the config file (User's forbidden zone - read only!)
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_models(config):
    models = []
    
    # 1. Check Standard 'models.providers'
    providers = config.get('models', {}).get('providers', {})
    for provider_name, provider_data in providers.items():
        for model in provider_data.get('models', []):
            model_id = model.get('id')
            full_id = f"{provider_name}/{model_id}"
            
            alias = ""
            if "flash" in model_id.lower(): alias = "flash"
            elif "pro" in model_id.lower(): alias = "pro"
                
            models.append({
                "full_id": full_id,
                "short_id": model_id,
                "provider": provider_name,
                "alias": alias
            })

    # 2. Check 'agents.defaults.models' (Catalog)
    catalog = config.get('agents', {}).get('defaults', {}).get('models', {})
    for full_id, data in catalog.items():
        # Avoid duplicates if already found
        if any(m['full_id'] == full_id for m in models):
            continue
            
        parts = full_id.split('/')
        provider = parts[0] if len(parts) > 1 else "unknown"
        short_id = parts[1] if len(parts) > 1 else full_id
        
        # Use configured alias, or guess
        alias = data.get('alias', "")
        if not alias:
            if "flash" in short_id.lower(): alias = "flash"
            elif "pro" in short_id.lower(): alias = "pro"

        models.append({
            "full_id": full_id,
            "short_id": short_id,
            "provider": provider,
            "alias": alias
        })
            
    return models

def main():
    config = load_config()
    models = find_models(config)
    
    query = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if query:
        # Search mode
        matches = []
        for m in models:
            # Check for substring match in full_id (e.g. "claude" in "anthropic/claude-3-opus")
            if query in m['full_id'].lower():
                matches.append(m['full_id'])
            # Check for provider match (e.g. "openai")
            elif query in m['provider'].lower():
                matches.append(m['full_id'])
            # Check for alias match
            elif m['alias'] == query:
                 matches.append(m['full_id'])

        # Deduplicate matches
        matches = sorted(list(set(matches)))

        if len(matches) == 1:
            print(matches[0])
        elif len(matches) > 1:
            # If exact match exists in the list, prefer it
            for match in matches:
                if match.lower() == query or match.split('/')[-1].lower() == query:
                    print(match)
                    return
            # Otherwise return all matches for the Agent to decide
            print("MULTIPLE_MATCHES:")
            for match in matches:
                print(match)
        else:
            print(f"Error: No model found matching '{query}'")
            sys.exit(1)
    else:
        # List mode
        print(json.dumps(models, indent=2))

if __name__ == "__main__":
    main()
