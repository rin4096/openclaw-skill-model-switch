import json
import os
import sys

# Path to the config file
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(1)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_models(config):
    models = []
    seen_ids = set()

    # Priority 1: agents.defaults.models (The Official Catalog)
    catalog = config.get('agents', {}).get('defaults', {}).get('models', {})
    for full_id, data in catalog.items():
        parts = full_id.split('/')
        provider = parts[0] if len(parts) > 1 else "unknown"
        short_id = parts[1] if len(parts) > 1 else full_id
        
        models.append({
            "full_id": full_id,
            "short_id": short_id,
            "provider": provider,
            "alias": data.get('alias', ""),
            "description": data.get('description', ""),
            "tags": data.get('tags', []),
            "source": "catalog"
        })
        seen_ids.add(full_id)

    # Priority 2: models.providers (Raw providers)
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
                    "alias": "",
                    "description": "",
                    "tags": [],
                    "source": "provider"
                })
                seen_ids.add(full_id)
            
    return models

def main():
    config = load_config()
    models = find_models(config)
    
    query = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if query:
        # Smart Search
        results = []
        for m in models:
            # Match ID, Provider, Alias, or Tags
            if (query in m['full_id'].lower() or 
                query in m['provider'].lower() or 
                (m['alias'] and query in m['alias'].lower()) or
                any(query in t.lower() for t in m['tags'])):
                results.append(m)

        if len(results) == 1:
            print(results[0]['full_id'])
        elif len(results) > 1:
            # Exact tie-breaking
            for r in results:
                if r['short_id'].lower() == query or (r['alias'] and r['alias'].lower() == query):
                    print(r['full_id'])
                    return
            print(json.dumps(results))
        else:
            sys.exit(1)
    else:
        # Full List Mode
        print(json.dumps(models, indent=2))

if __name__ == "__main__":
    main()
