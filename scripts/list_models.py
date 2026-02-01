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
    seen_ids = set()

    # 1. Check Standard 'models.providers'
    providers = config.get('models', {}).get('providers', {})
    for provider_name, provider_data in providers.items():
        for model in provider_data.get('models', []):
            model_id = model.get('id')
            full_id = f"{provider_name}/{model_id}"
            if full_id not in seen_ids:
                models.append({
                    "full_id": full_id,
                    "short_id": model_id,
                    "provider": provider_name,
                    "alias": "" # Let users use IDs directly
                })
                seen_ids.add(full_id)

    # 2. Check 'agents.defaults.models' (Catalog)
    catalog = config.get('agents', {}).get('defaults', {}).get('models', {})
    for full_id, data in catalog.items():
        if full_id in seen_ids:
            # Update alias if found in catalog
            for m in models:
                if m['full_id'] == full_id:
                    m['alias'] = data.get('alias', "")
            continue
            
        parts = full_id.split('/')
        provider = parts[0] if len(parts) > 1 else "unknown"
        short_id = parts[1] if len(parts) > 1 else full_id
        
        models.append({
            "full_id": full_id,
            "short_id": short_id,
            "provider": provider,
            "alias": data.get('alias', "")
        })
        seen_ids.add(full_id)
            
    return models

def main():
    config = load_config()
    models = find_models(config)
    
    query = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if query:
        # Search mode
        results = []
        for m in models:
            # Match against everything!
            if (query in m['full_id'].lower() or 
                query in m['provider'].lower() or 
                (m['alias'] and query in m['alias'].lower())):
                results.append(m)

        if len(results) == 1:
            # Single perfect match
            print(results[0]['full_id'])
        elif len(results) > 1:
            # Try to find an exact match for ID or Alias to break the tie
            for r in results:
                if r['short_id'].lower() == query or (r['alias'] and r['alias'].lower() == query):
                    print(r['full_id'])
                    return
            
            # Still multiple? Return as JSON list for the Agent
            print(json.dumps(results))
        else:
            print(f"Error: No model found matching '{query}'")
            sys.exit(1)
    else:
        # List mode
        print(json.dumps(models, indent=2))

if __name__ == "__main__":
    main()
