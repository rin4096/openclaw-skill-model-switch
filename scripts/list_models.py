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
    # Dictionary to store models grouped by provider
    # Structure: { "provider_name": [ { model_info }, ... ] }
    grouped_models = {}
    
    # Also keep a flat list for search functionality
    flat_models = []
    seen_ids = set()

    def add_model(provider, full_id, short_id, alias="", description="", tags=None, source=""):
        if full_id in seen_ids:
            return
        
        model_info = {
            "full_id": full_id,
            "short_id": short_id,
            "provider": provider,
            "alias": alias,
            "description": description,
            "tags": tags or [],
            "source": source
        }
        
        # Add to groups
        if provider not in grouped_models:
            grouped_models[provider] = []
        grouped_models[provider].append(model_info)
        
        # Add to flat list
        flat_models.append(model_info)
        seen_ids.add(full_id)

    # Priority 1: agents.defaults.models (The Official Catalog)
    catalog = config.get('agents', {}).get('defaults', {}).get('models', {})
    for full_id, data in catalog.items():
        parts = full_id.split('/')
        provider = parts[0] if len(parts) > 1 else "unknown"
        short_id = parts[1] if len(parts) > 1 else full_id
        
        add_model(
            provider, full_id, short_id, 
            alias=data.get('alias', ""),
            description=data.get('description', ""),
            tags=data.get('tags', []),
            source="catalog"
        
        )

    # Priority 2: models.providers (Raw providers)
    providers = config.get('models', {}).get('providers', {})
    for provider_name, provider_data in providers.items():
        for model in provider_data.get('models', []):
            model_id = model.get('id')
            full_id = f"{provider_name}/{model_id}"
            
            add_model(
                provider_name, full_id, model_id,
                source="provider"
            )
            
    return grouped_models, flat_models

def main():
    config = load_config()
    grouped, flat = find_models(config)
    
    if len(sys.argv) > 1:
        query = sys.argv[1].lower()
        
        # Mode 1: Exact Provider Match (Menu Level 2)
        # If the argument matches a provider name exactly, return its models.
        if query in grouped:
            print(json.dumps(grouped[query]))
            return

        # Mode 2: Smart Search (Fallback)
        results = []
        for m in flat:
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
            # If nothing found, exit with error
            sys.exit(1)
    else:
        # Mode 0: List Providers (Menu Level 1)
        # Return a list of provider names for the top-level menu.
        print(json.dumps(list(grouped.keys())))

if __name__ == "__main__":
    main()
