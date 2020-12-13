# SOS DATA
## Where the data in CD241120.txt strays from the meta data outlined in corp-bulkorder-layout fixed.doc
- All Record Layout 11 entries having length of 562 (already noted in previous email)
- Record Layout 12 entries also seem to have an "EDIT" ACTION only (ADD,UPDATE,DELETE are in the revised corp-bulkorder-layout document you sent over)
- Record Layout 12 entries can be of length 560,260,or 252 depending on their ACTION and CURRENT_VALUE fields, specifically: 
     - "EDIT" actions where CURRENT_VALUE and AUDIT_COMMENT fields are blank (spaces) are width 260
     - 6 "EDIT" actions where "Vendor Error - Entity name included with individual name - Removed entity name." proceeds the ACTION field are width 260
     - 1 "EDIT" action where "Updated PIR - Filing# 800345627 Doc# 330904380001 " proceeds the ACTION field is width 260
     - "ADD" actions that are missing data for TABLE_ID and FIELD_ID (presumably as the Entries up to and including the ACTION field are width 20 and not 28 as specified in the corp-bulkorder-layout document you sent over)  and have no data for CURRENT_VALUE and AUDIT_COMMENT are width 252 
