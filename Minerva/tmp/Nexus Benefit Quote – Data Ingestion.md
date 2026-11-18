# Nexus Benefit Quote – Data Ingestion

## Overview

We perform **data ingestion into Databricks Delta Tables** as part of the Nexus Benefit Quote process. The ingestion leverages the **Nexus Cloud API**, which serves as the primary interface for extracting plan & benefit data from Cosmos Database.

The ingestion supports two modes:

- **Full Refresh**  
Used during the very first load or when a complete rebuild is required. This process ingests the entire dataset into Databricks Delta tables.
- **Incremental Refresh**  
Used for ongoing updates. This process ingests only the changes available from a given date, ensuring efficient and timely updates without reloading all data.

Both approaches leverage Databricks Delta’s capabilities for ACID transactions, schema enforcement, and efficient upserts.

## **Ingestion Strategies**

### **Full Refresh**

- **When used:** First-time load or complete rebuild.
- **Steps:**
    - Drop existing Delta table (if any).
    - Load entire dataset from source.
    - Validate schema and data integrity.
- **Considerations:**
    - High resource usage.
    - Longer runtime.
- **Notes: **
    - The Nexus Team supplies a CSV file containing one or more composite keys made up of FacetsProductId and EffectiveDate. 
    - The composite key, consisting of *FacetsProductId* and *EffectiveDate*, uniquely identifies a product.
    - Databricks processes each item and retrieves its complete product details via the [Fetch Product Details API](https://blueshieldca.atlassian.net/wiki/spaces/SOOP/pages/1711800500/Nexus+Benefit+Quote+Data+Ingestion#API-Details).

### **Incremental Refresh**

- **When used:** Daily or periodic updates.
- **Steps:**
    - Identify changes since `last_refresh_date`.
    - Apply upserts (MERGE INTO Delta table).
- **Considerations:**
    - Requires reliable change tracking (CDC or timestamp).
    - Faster and resource-efficient.
- **Notes**
    - Returns a list of products that have been updated or added after the specified `last_refresh_date`. Full product details can be retrieved using the [Fetch Product Details API](https://blueshieldca.atlassian.net/wiki/spaces/SOOP/pages/1711800500/Nexus+Benefit+Quote+Data+Ingestion#API-Details) 

## **API Details**

### End Points

#### Full Refresh/Fetch Product Details Example: 

Processes all products listed in the CSV file, retrieves their details, and upserts them into the Databricks Delta Table. .

```
curl --location 'https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/api/v2/PPDD/M0037048/20250101' \
--header 'Accept: application/json' 
```

#### Incremental Refresh Example: ￼

```
curl --location 'https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/api/product-sync' \
--header 'accept: */*' \
--header 'If-Modified-Since: 2025-12-04T18:00:00Z'
```

#### **Headers**

- `If-Modified-Since` for incremental refresh.

## Environments

| **Nexus Cloud Environment** | **Fetch Product Details** | **Product Sync** |
| --- | --- | --- |
| Dev | `https://app-prdsrch-npn-to-bncp-cus-052.azurewebsites.net/api/v2/PPDD/:facetsProductId/:effectiveDate` | `https://app-prdsrch-npn-to-bncp-cus-052.azurewebsites.net/api/product-sync` |
| QA | `https://app-prdsrch-npn-to-bncp-cus-252.azurewebsites.net/api/v2/PPDD/:facetsProductId/:effectiveDate` | `https://app-prdsrch-npn-to-bncp-cus-252.azurewebsites.net/api/product-sync` |
| Stage | `https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/api/v2/PPDD/:facetsProductId/:effectiveDate` | `https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/api/product-sync` |
| Prod | `https://app-prdsrch-pp-to-bncp-cus-952.azurewebsites.net/api/v2/PPDD/:facetsProductId/:effectiveDate` | `https://app-prdsrch-pp-to-bncp-cus-952.azurewebsites.net/api/product-sync` |

### Swagger Spec: ￼

The Swagger (OpenAPI) specification — provides a complete, machine‑readable description of an API, including endpoints, request/response formats, authentication, error codes, and metadata.

| **Nexus Cloud Environment** |  |
| --- | --- |
| Dev | [https://app-prdsrch-npn-to-bncp-cus-052.azurewebsites.net/swagger/index.html](https://app-prdsrch-npn-to-bncp-cus-252.azurewebsites.net/swagger/index.html) |
| QA | <https://app-prdsrch-npn-to-bncp-cus-252.azurewebsites.net/swagger/index.html> |
| Stage | <https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/swagger/index.html> |
| Prod | [app-prdsrch-pp-to-bncp-cus-952.azurewebsites.net/swagger/v2/swagger.json](https://app-prdsrch-pp-to-bncp-cus-952.azurewebsites.net/swagger/v2/swagger.json) |
