provider "azurerm" {
  features {}
}

# --- FinOps Showback Foundation (Institutional Hub) ---

resource "azurerm_resource_group" "fst" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Billing Analytics Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "fst" {
  name                   = "psql-${var.project_name}-billing-${var.environment}"
  resource_group_name    = azurerm_resource_group.fst.name
  location               = azurerm_resource_group.fst.location
  version                = "13"
  administrator_login    = "fstadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Multi-Cloud Billing Lake (Storage Account) ---

resource "azurerm_storage_account" "billing_lake" {
  name                     = "stfstbillinglake${var.environment}"
  resource_group_name      = azurerm_resource_group.fst.name
  location                 = azurerm_resource_group.fst.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Environment = var.environment
    CostCenter  = "Finance-Shared"
  }
}

# --- Monitoring & Observability (Log Analytics) ---

resource "azurerm_log_analytics_workspace" "fst" {
  name                = "log-${var.project_name}-analytics-${var.environment}"
  location            = azurerm_resource_group.fst.location
  resource_group_name = azurerm_resource_group.fst.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# --- Container Apps Environment (Runtime) ---

resource "azurerm_container_app_environment" "fst" {
  name                       = "cae-${var.project_name}-${var.environment}"
  location                   = azurerm_resource_group.fst.location
  resource_group_name        = azurerm_resource_group.fst.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.fst.id
}
