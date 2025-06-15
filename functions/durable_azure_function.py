# Orchestrator Function
def orchestrator_function(context):
    record = context.get_input()
    
    # Step 1: Fraud detection
    is_fraudulent = yield context.call_activity("FraudCheck", record)
    if is_fraudulent:
        yield context.call_activity("LogFraud", record)
        return "Request flagged"

    # Step 2: Add timestamp & clean data
    enriched_record = yield context.call_activity("EnrichRecord", record)

    # Step 3: Store in Cosmos DB
    yield context.call_activity("StoreToCosmosDB", enriched_record)
    
    return "Stored"

# Activity Function: FraudCheck
def FraudCheck(record):
    user_id = record["userId"]
    # Check from a Redis store or CosmosDB how many attempts in last X mins
    return check_request_frequency(user_id) > 3

# Activity Function: EnrichRecord
def EnrichRecord(record):
    from datetime import datetime
    record["_ingestionTime"] = datetime.utcnow().isoformat()
    record["ttl"] = 8640000  # 100 days = 100 * 24 * 60 * 60
    return record

# Activity Function: StoreToCosmosDB
def StoreToCosmosDB(record):
    cosmos_client.upsert_document("BillingDB", "Transactions", record)
