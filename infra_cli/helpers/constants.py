ErrorMessages = {
    "no_infra_file": "Failed to load infra.yaml, make sure it exists in the current directory",
    "no_provider": "No provider found for resource: {}",
    "duplicate_resource_id": "Duplicate resource id found: {}",
    "no_resources": "No resources found in infra.yaml",
    "no_config": "No config.yaml found for resource: {}, make sure it exists in infra/providers/{}/config.yaml",
    "no_provider_class": "No provider class found for resource: {}, make sure it exists in infra/providers/{}",
    "provider_config_validation_failed": "Failed to validate config.yaml for provider: {}",
    "provider_not_installed": "Provider: {} is not installed, install it using `infra provider install {}`",
}

InfoMessages = {
    "resource_not_created_yet": "Resource with id {} is not created yet",
    "destroyed_resource": "Destroyed resource: {}",
    "created_resource": "Created resource: {}",
    "applied_changes": "Applied changes to resource: {}",
    "imported_provider": "Imported provider: {}",
    "already_in_state": "Resource with id {} is already in the desired state",
    "loaded_user_provider": "Loaded user created provider: {}",
    "provider_not_installed": "Provider: {} is not installed, attempting to install it",
}
