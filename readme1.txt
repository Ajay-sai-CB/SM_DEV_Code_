# SynapseArch6DtSource Setup
# To set up a new external data source, follow these steps:

## -- ===========================================================================
## -- Create database template for Azure Synapse SQL Analytics on-demand Database
## -- ===========================================================================

```
## Create External Data Source


CREATE DATABASE SMSMBSFDASQLUAT
```

```sql
CREATE EXTERNAL DATA SOURCE SynapseArch6DtSource
WITH
  (  LOCATION = 'https://stsmbsfdadev.dfs.core.windows.net/archive6', -- Container names are case sensitive
    CREDENTIAL = [SynapseCred]
)
GO
```

# Create a View
## Create a view that extracts relevant information from the external data source:
```
-- Creating a view
SELECT
  TOP 100 
  result.filepath(1) as [Year_p],
  result.filepath(2) as [Month_p],
  result.filepath(3) as [Day_p],
  *
FROM
  OPENROWSET(
    BULK 'Object=Invoice/*/*/*/**',
    DATA_SOURCE = 'SynapseArch6DtSource',
    FORMAT = 'PARQUET'
  ) AS [result]
GO
```


```
[12/27/23 10:42 AM] Ajay Sai Goud   Pasham


CREATE VIEW Apex_logs

AS

SELECT

  result.filepath(1) as [AccountID_p],result.filepath(2) as [Year_p],result.filepath(3) as [Month_p],*

FROM

    OPENROWSET(

        BULK '*/Object=Apex_Logs/*/*/**',

        data_source = 'SynapseDtSource',

        FORMAT = 'PARQUET'

    ) AS [result]

GO
```


# Query the View

### Query the created view to retrieve specific data:

```
-- Querying the view
-- Retrieve the first 100 rows for the specified conditions
SELECT *
FROM Invoice
WHERE
  (Year_p >= 'Year=2023' AND Year_p <= 'Year=2025') AND
  (Month_p >= 'Month=01' AND Month_p <= 'Month=12') AND
  (AccountID_p = 'AccountId=0017X00001571soQAA')
LIMIT 100 OFFSET 0;
```


```
/****** Object:  View [dbo].[Invoice__c]    Script Date: 1/8/2024 9:05:29 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER VIEW [dbo].Apex_Log__c
AS
SELECT
  result.filepath(1) as [Year_p],result.filepath(2) as [Month_p],result.filepath(3) as [Day_p],*
FROM
    OPENROWSET(
        BULK 'Object=Apex_Log/*/*/*/**',
        data_source = 'SynapseArchDtSource',
        FORMAT = 'PARQUET'
    ) AS [result]

GO


```


```
CREATE EXTERNAL DATA SOURCE SynapseArchDtSource
WITH
  (  LOCATION = 'https://stsmbsfdadev.dfs.core.windows.net/archive', --container names are case sensitive
    CREDENTIAL =  [SynapseCred]
)
GO

-- This is auto-generated code
SELECT
    TOP 100 *
FROM
    OPENROWSET(
        BULK 'https://stsmbsfdadev.dfs.core.windows.net/archive6/Object=Invoice/Year=2014/Month=01/Day=01/Invoice_1704700505208-00001.parquet',
        FORMAT = 'PARQUET'
    ) AS [result]

```


```
 SET ANSI_WARNINGS OFF; 

SELECT *
FROM Service_Work_Order__c
WHERE
  --(Year_p >= 'Year=2003' AND Year_p <= 'Year=2025') AND
  --(Month_p >= 'Month=01' AND Month_p <= 'Month=12') AND
  (AccountId = '0013000001JsUuaAAF')
  ORDER BY AccountId
  OFFSET 0 ROWS FETCH NEXT 100 ROWS ONLY; 


-- Set ANSI_WARNINGS back ON for other queries 
SET ANSI_WARNINGS ON; 
```