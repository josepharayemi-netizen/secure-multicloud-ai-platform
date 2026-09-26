resource "random_string" "suffix" {length = 6; special = false; upper = false}
locals {
  name = "secure-ai-${var.environment}"
  tags = {Project = "secure-multicloud-ai-platform", Environment = var.environment, ManagedBy = "Terraform"}
}
resource "azurerm_resource_group" "main" {
  name = "rg-${local.name}-${random_string.suffix.result}"
  location = var.location
  tags = local.tags
}
resource "azurerm_log_analytics_workspace" "main" {
  name = "log-${local.name}-${random_string.suffix.result}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku = "PerGB2018"
  retention_in_days = 30
}
resource "azurerm_container_registry" "main" {
  name = "acrsecureai${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  sku = "Premium"
  admin_enabled = false
}
resource "azurerm_kubernetes_cluster" "main" {
  name = "aks-${local.name}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix = local.name
  private_cluster_enabled = true
  oidc_issuer_enabled = true
  workload_identity_enabled = true
  default_node_pool {
    name = "platform"
    vm_size = "Standard_D4s_v5"
    node_count = 2
    auto_scaling_enabled = true
    min_count = 2
    max_count = 5
  }
  identity {type = "SystemAssigned"}
  oms_agent {log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id}
  network_profile {network_plugin = "azure"; network_policy = "azure"}
  tags = local.tags
}
resource "azurerm_key_vault" "main" {
  name = "kv-ai-${random_string.suffix.result}"
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id = azurerm_kubernetes_cluster.main.identity[0].tenant_id
  sku_name = "standard"
  enable_rbac_authorization = true
  purge_protection_enabled = true
}
resource "azurerm_storage_account" "artifacts" {
  name = "staai${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  account_tier = "Standard"
  account_replication_type = "ZRS"
  min_tls_version = "TLS1_2"
  public_network_access_enabled = false
  tags = local.tags
}
