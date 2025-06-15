## Azure Billing Data Archival & Fraud Detection Solution – Summary

This solution is designed to manage **billing records** efficiently using a scalable, cost-optimized architecture built on **Azure**. It addresses:

- Timely archival of stale data
- Fraud detection logic
- TTL-based cleanup
- Category-wise structured storage in ADLS
- Scheduled weekend orchestration

---

## Components & Flow

### 1. **Cosmos DB (Source)**
- Stores active billing records for each user.
- Each record includes fields like `billingDate`, `status`, `items[]`, and `_ts` (timestamp).

### 2. **Azure Functions (Preprocessing Logic)**
Used for **lightweight compute before pipeline execution**, specifically:
- **Deriving Partition Columns**: Extracts `year`, `month`, `day` from `billingDate` to organize data in ADLS.
- **TTL Enforcement**: Sets a **Time-To-Live (TTL)** of `100 days` (90-day active + 10-day grace period).
- **Fraud Checks** (Optional enhancement): Functions can flag suspicious billing patterns (e.g., unusually high totals, frequent retries).

> *Example:* A record with `billingDate = 2025-02-28` will have TTL expire by `2025-06-07`.

---

### 3. **Azure Data Factory (ADF) or Azure Databricks (ADB notebook) Weekend Archival Pipeline**
- **Trigger**: Runs every **Saturday at 11:59 PM IST**.
- **Step 1**: Filters records older than **90 days** using `_ts`.
- **Step 2**: Splits records into 3 categories:
  - **Success** (status = 'SUCCESS')
  - **Failed** (status = 'FAILED')
  - **Items** (records with `items[]` array)
  - Archives each category into separate ADLS paths:
  - /success/yyyy/MM/dd/
  - /failed/yyyy/MM/dd/
  - /items/yyyy/MM/dd/

- - **Step 4**: Deletes the filtered archived records from Cosmos DB (optional but recommended for cost optimization).

---

### 4. **ADLS Gen2 (Data Lake Storage)**
- Final sink for long-term storage of:
- Cleaned billing data
- Failure logs
- Flattened item arrays (for analytics)

---

### Design Considerations

| Aspect                     | Design Choice & Reason                                                                 |
|---------------------------|-----------------------------------------------------------------------------------------|
| **TTL in Cosmos DB**      | 100 days total (90 active + 10 grace) for automatic cleanup and alerting.              |
| **Azure Functions**       | Used to precompute fields, apply fraud logic, or trigger ADF programmatically.         |
| **Weekend Scheduling**    | Ensures minimal load on weekdays and aligns with data retention policies.              |
| **Data Splitting Logic**  | Helps isolate successful vs failed vs item-level data for better downstream use.       |
| **JSON format in ADLS**   | Enables schema-on-read and easier querying from Azure Synapse or Databricks.          |
| **Parameterization**      | Threshold date is dynamically calculated using UTC `-90 days`.                         |
| **Retry Policies**        | Activities have retry attempts and timeout policies for robustness.                    |

---

### Example Scenario

Let's say a user had this record in Cosmos DB:

```json
{
"id": "TXN_20250228_001",
"billingDate": "2025-02-28",
"status": "SUCCESS",
"items": [
  {"itemId": "I001", "amount": 1200},
  {"itemId": "I002", "amount": 300}
],
"_ts": 1748732400
}

```
What Happens on Weekend:
It’s now June 15, 2025 → the record is older than 90 days.

status is "SUCCESS" → goes to /success/2025/02/28/

items array is not empty → flattened and written to /items/2025/02/28/

If TTL is reached, the record is auto-deleted, else deletion is handled by pipeline if active (for deletion also from Cosmos DB we have specified TTL to 100 days so that auto-deletion doesn't cause any issue and even if adhoc run is made for pipeline that also fulfills our need).

## This approach ensures:

- Minimal operational cost (via TTL and weekend scheduling)

- Granular data categorization for analytics

- Seamless archival with option to trigger fraud logic

- Flexibility to integrate with Synapse, Power BI, or downstream alerts


