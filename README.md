# azure-billing-archival-solution
Cost-optimized Azure billing records management with Cosmos DB, ADLS, ADF, and Azure Functions

This repository contains all components for the Azure-based billing records archival and fraud detection pipeline.

#### Folder Layout

```text
azure-billing-archival-solution/
├── README.md                               # Project overview and setup
├── json_struct/
│   └── sample_billing_record.json         # Sample Cosmos DB input record
├── functions/
│   └── durable_azure_function.py           # Sample Azure function being called when API makes call
├── architectue_flow/
│   └── architecture.png                 # Visual diagram of architecture
│   └── intro.md                         # Complete architecture and design explanation
│   ├── flow_for_exporting_old_data.md   # Flow being followed for uploading old data to ADLS
├── adb_notebook_code/
│   ├── export_adls.py                 
├── ADF_Pipeline_pseudo_code/
│   └── cosmostoadls.json            # Main ADF pipeline definition
│   └── schedule.json                # Scheduled trigger for weekend archival
