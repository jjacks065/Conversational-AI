# Nexus Cloud API – Consumer Interaction & Request Flow

# Overview

The **Nexus Cloud API** provides a unified and secure interface for both **internal** and **external** consumers to access Nexus capabilities.  
All consumer traffic is routed through standardized Azure components to ensure **security, observability, throttling, and governance**.

This page explains:

- Who the consumers are (internal vs external)
- How requests flow through Nexus Cloud infrastructure
- Environment-specific endpoints
- Key responsibilities of each component in the flow

## High-Level Architecture

**Request Flow**

## Consumers

### External Consumers

External consumers are systems or applications outside the organization boundary, such as:

- Databricks Jobs (Optarion Tenant)
- Sales Force Cloud

**Characteristics**

- Access Nexus Cloud APIs via public DNS endpoints
- Enforced through strict security controls (TLS, authentication, throttling)
- Governed by API contracts published in APIM
- All the API are secured via API Key

**Request Flow**

```
External Consumer (Public Endpoint)
        |
        v
      Akamai
        |
        v
      Firewall
        |
        v 
------BSC Tenant----------
Azure Application Gateway
        |
        v
Azure API Management (APIM)
        |
        v
Nexus Cloud API (Azure App Service)
```

**Public Endpoints**

| **Environment** | **Host Name** | **Base Path** |
| --- | --- | --- |
| DEV | `cloud-api-dev.blueshieldca.com` | `bnp-prdct-dev-v2` |
| QA | `cloud-api-dev.blueshieldca.com` | `bnp-prdct-qa-v2` |
| Stage | `cloud-api-dev.blueshieldca.com` | `bnp-prdct-stg-v2` |
| Prod | `cloud-api.blueshieldca.com` | `bnp-prdct-v2` |

### Internal Consumers

Internal consumers are applications hosted within the organization, such as:

- Member Protal
- Find a doctor
- Nexus Product lookup UI

**Characteristics**

- Must use the private connectivity
- Typically have higher trust levels but still enforced via APIM policies
- Benefit from centralized monitoring and logging
- All the API are secured via API Key

**Request Flow**

```
Internal Consumer (Private Endpoint)
        |
        v
Azure Application Gateway
        |
        v
Azure API Management (APIM)
        |
        v
Nexus Cloud API (Azure App Service)
```

**Private Endpoints**

| **Environment** | **Host Name** | **Base Path** |
| --- | --- | --- |
| DEV | `nexus-cloud-api-dev.bsc.bscal.com` | `bnp-prdct-dev-v2` |
| QA | `nexus-cloud-api-qa.bsc.bscal.com` | `bnp-prdct-qa-v2` |
| Stage | `nexus-cloud-api-stg.bsc.bscal.com` | `bnp-prdct-stg-v2` |
| Prod | `nexus-cloud-api.bsc.bscal.com` | `bnp-prdct-v2` |

## Security Considerations

- **TLS enforced** end-to-end
- **Authentication & authorization** handled at APIM 
- **WAF rules** enforced at Application Gateway
- **Rate limiting** to protect backend services
- **Centralized logging and monitoring** via APIM and App Service diagnostics

## Public Endpoint Access via cURL

| **Environment** | **Curl Command (Product Information)** | **Curl Command (Incremental Updates)** |
| --- | --- | --- |
| DEV | `curl --location 'https://cloud-api-dev.blueshieldca.com/bnp-prdct-dev-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xxx'` | `curl --location 'https://cloud-api-dev.blueshieldca.com/bnp-prdct-dev-v2/api/product-sync' \ --header 'accept: /' \ --header 'If-Modified-Since: 2025-01-01T18:00:00Z' \ --header 'Ocp-Apim-Subscription-Key: xxxx'` |
| QA | `  curl --location 'https://cloud-api-dev.blueshieldca.com/bnp-prdct-qa-v2/api/v2/PPDD/M0033822/20240101' \   --header 'Accept: application/json' \   --header 'Ocp-Apim-Subscription-Key: xxx'` | `curl --location 'https://cloud-api-qa.blueshieldca.com/bnp-prdct-qa-v2/api/product-sync' \ --header 'accept: /' \ --header 'If-Modified-Since: 2025-01-01T18:00:00Z' \ --header 'Ocp-Apim-Subscription-Key: xxxx'` |
| Stage | `curl --location 'https://cloud-api-dev.blueshieldca.com/bnp-prdct-stg-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xxx'` | `curl --location 'https://cloud-api-stg.blueshieldca.com/bnp-prdct-stg-v2/api/product-sync' \ --header 'accept: /' \ --header 'If-Modified-Since: 2025-01-01T18:00:00Z' \ --header 'Ocp-Apim-Subscription-Key: xxxx'` |
| Prod | `curl --location 'https://cloud-api.blueshieldca.com/bnp-prdct-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xxx'` | `curl --location 'https://cloud-api.blueshieldca.com/bnp-prdct-v2/api/product-sync' \ --header 'accept: /' \ --header 'If-Modified-Since: 2025-01-01T18:00:00Z' \ --header 'Ocp-Apim-Subscription-Key: xxxx'` |

## Private Endpoint Access via cURL

| **Environment** | **Curl Command** |
| --- | --- |
| DEV | `curl --location 'https://nexus-cloud-api-dev.bsc.bscal.com/bnp-prdct-dev-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xxx'` |
| QA | `  curl --location 'https://nexus-cloud-api-qa.bsc.bscal.com/bnp-prdct-qa-v2/api/v2/PPDD/M0033822/20240101' \   --header 'Accept: application/json' \   --header 'Ocp-Apim-Subscription-Key: xxx'` |
| Stage | `curl --location 'https://cnexus-cloud-api-stg.bsc.bscal.com/bnp-prdct-stg-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xx'` |
| Prod | `curl --location 'https://nexus-cloud-api.bsc.bscal.com/bnp-prdct-v2/api/v2/PPDD/M0033822/20240101' \ --header 'Accept: application/json' \ --header 'Ocp-Apim-Subscription-Key: xxx'` |
