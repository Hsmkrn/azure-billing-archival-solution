## ADF/ADB Data Flow Logic (Weekend Archival)

```text
[Cosmos Source]
   ↓
[Derived Column]
   - Add year, month, day from billingDate
   ↓
[Conditional Split]
   - status == 'SUCCESS' → success branch
   - status == 'FAILED' → failed branch
   ↓
[Flatten Items] (on item array)
   ↓
[Sink to ADLS]
   - SUCCESS Path: /success/yyyy/MM/dd/
   - FAILED Path: /failed/yyyy/MM/dd/
   - ITEMS  Path: /items/yyyy/MM/dd/
