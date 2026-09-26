output "cluster_name" {value = azurerm_kubernetes_cluster.main.name}
output "registry_url" {value = azurerm_container_registry.main.login_server}
output "artifact_storage" {value = azurerm_storage_account.artifacts.name}
