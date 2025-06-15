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
   - Path: /success/yyyy/MM/dd/
   - Path: /failed/yyyy/MM/dd/
   - Path: /items/yyyy/MM/dd/
