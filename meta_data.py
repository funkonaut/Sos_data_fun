"""
The module to define meta data constants as specified by corp-bulkorder-layout.doc
"""

import pandas as pd


############META DATA CONSTANTS################
df_meta = pd.read_csv("sos_meta_data.csv",dtype=object)
#Layout columns to link
cols_2 = [("status_id","status_description"),("corp_type_id","corp_type"),("nonprofit_subtype_id","description_n")]
cols_9 = [("name_status_id","status"),("name_type_id","name_description")]
cols_10 = [("capacity_id","corp_type_id_description")]
COLS = [None, cols_2, None, None, None, None, None, None, cols_9, cols_10, None, None, None]
MD_TABLE_NAMES = [None, "md_master", None, None, None, None, None, None, "md_charter_names", "md_associated_entity", None, None, None]

#Each record has a length of 560 characters and all the fields contained within are fixed-width strings.  Data Type ‘N’ (Numeric) is right justified zero filled on the left.  Data Type ‘C’ (Character) is left justified and space filled on the right, even if the value happens to be a number. Data Type 'D' (Date) is a subset of data type 'N' and is not specified in the layout document but infered from the table columns names (ends with _date)
#Record layout code 01 Delete All Command Record
delete_rec_w = [0,2,10,6,542]
delete_rec_dt = ["N","N","C","C"]
delete_rec_names = ["layout_code","filing_num","value_DELETE","filler"]
#Record layout code 02 Master Record
master_rec_w = [0,2,10,2,2,150,2,8,8,8,8,8,11,150,16,4,64,8,16,3,2,8,70]
#master_rec_dt = ["N","N","N","N","C","N","N","N","N","N","N","N","C","C","C","C","N","C","N","N","C","C"]
master_rec_dt = ["N","N","N","N","C","N","N","D","D","D","D","N","C","C","C","C","D","C","N","N","C","C"] #BOC DATE? WHAT TODO IS IT THE SAME FORMAT?????
master_rec_names = ["layout_code","filing_num","status_id","corp_type_id","name","perpetual_flag","creation_date","expiration_date","inactive_date","formation_date","report_due_date","tax_id","dba_name","foreign_fein","foreign_state","foreign_country","foreign_formation_date","expiration_Type","nonprofit_subtype_id","boc_flag","boc_date","filler"]
#Record layout code 03 Master Address Record
address_rec_w = [0,2,10,50,50,64,4,9,6,64,301]
address_rec_dt = ["N","N","C","C","C","C","C","C","C","C"]
address_rec_names = ["layout_code","filing_num","address1","address2","city","state","zip_code","zip_extension","country","filler"]
#Record layout code 04 Reserved
reserved_rec_w = []
reserved_rec_dt = []
reserved_rec_names = []
#Record layout code 05 Registered Agent Record - Business Name
ra_business_rec_w = [0,2,10,50,50,64,4,9,6,64,8,150,143]
ra_business_rec_dt = ["N","N","C","C","C","C","C","C","C","D","C","C"]
ra_business_rec_names = ["layout_code","filing_num","address1","address2","city","state","zip_code","zip_extension","country","inactive_date","business_name","filler"]
#Record layout code 06 Registered Agent Record - Personal Name
ra_personal_rec_w = [0,2,10,50,50,64,4,9,6,64,8,50,50,50,6,137]
ra_personal_rec_dt = ["N","N","C","C","C","C","C","C","C","D","C","C","C","C","C"]
ra_personal_rec_names = ["layout_code","filing_num","address1","address2","city","state","zip_code","zip_extension","country","inactive_date","agent_last_name","agent_first_name","agent_middle_name","agent_suffix","filler"]
#Record layout code 07 Charter Officer - Business Name
co_business_rec_w = [0,2,10,50,50,64,4,9,6,64,6,32,150,113]
co_business_rec_dt = ["N","N","C","C","C","C","C","C","C","N","C","C","C"]
co_business_rec_names = ["layout_code","filing_num","address1","address2","city","state","zip_code","zip_extension","country","officer_id","officer_title","business_name","filler"]
#Record layout code 08 Charter Officer - Personal Name
co_personal_rec_w = [0,2,10,50,50,64,4,9,6,64,6,32,50,50,50,6,107]
co_personal_rec_dt = ["N","N","C","C","C","C","C","C","C","N","C","C","C","C","C","C"]
co_personal_rec_names = ["layout_code","filing_num","address1","address2","city","state","zip_code","zip_extension","country","officer_id","officer_title","last_name","first_name","middle_name","suffix","filler"]
#Record layout code 09 Charter Names Record 
charter_names_rec_w = [0,2,10,6,150,3,3,8,8,8,8,11,254,5,84]
charter_names_rec_dt = ["N","N","N","C","N","N","D","D","D","C","N","C","C","C"]
charter_names_rec_names = ["layout_code","filing_num","name_id","name","name_status_id","name_type_id","creation_date","inactive_date","expire_date","county_type","consent_filing_number","selected_county_array","reserved","filler"]
#Record layout code 10 Associated Entity Record 
associated_entity_rec_w = [0,2,10,6,150,12,8,64,4,8,4,292]
associated_entity_rec_dt = ["N","N","N","C","N","D","C","C","D","N","C"]
associated_entity_rec_names = ["layout_code","filing_num","associated_entity_id","associated_entity_name","entity_filing_number","entity_filing_date","jurisdiction_country","jurisdiction_state","inactive_date","capacity_id","filler"]
#Record layout code 11 Filing History Record 12>10 392>394
filing_hist_rec_w = [0,2,10,14,12,96,8,8,8,2,8,392]
filing_hist_rec_dt = ["N","N","N","N","C","D","D","D","N","D","C"]
filing_hist_rec_names = ["layout_code","filing_num","document_number","filing_type_id","filing_type","entry_date","filing_date","effective_date","effective_cond_flag","inactive_date","filler"]
#Record layout code 12 Corp Audit Log Record
audit_rec_w = [0,2,10,8,4,4,10,300,222]
audit_rec_dt = ["N","N","D","N","N","C","C","C"]
audit_rec_names = ["layout_code","filing_num","audit_date","table_id","field_id","action","current_value","audit_comment"]
#Record layout code 99 Totals Record
code99_rec_w = [0,2,10,8,12,12,12,12,12,12,12,12,12,12,12,12,12,384]
code99_rec_dt = ["N","N","D","N","N","N","N","N","N","N","N","N","N","N","N","N","N"]
code99_rec_names = ["layout_code","all_9s","date_of_run","count_01","count_02","count_03","count_04","count_05","count_06","count_07","count_08","count_09","count_10","count_11","count_12","count_13","filler"]

WIDTHS = [delete_rec_w,master_rec_w,address_rec_w,reserved_rec_w,ra_business_rec_w,ra_personal_rec_w,co_business_rec_w ,co_personal_rec_w ,charter_names_rec_w,associated_entity_rec_w,filing_hist_rec_w ,audit_rec_w,code99_rec_w]
DTYPES = [delete_rec_dt,master_rec_dt,address_rec_dt,reserved_rec_dt,ra_business_rec_dt,ra_personal_rec_dt,co_business_rec_dt ,co_personal_rec_dt ,charter_names_rec_dt,associated_entity_rec_dt,filing_hist_rec_dt ,audit_rec_dt,code99_rec_dt]
NAMES = [delete_rec_names,master_rec_names,address_rec_names,reserved_rec_names,ra_business_rec_names,ra_personal_rec_names,co_business_rec_names ,co_personal_rec_names ,charter_names_rec_names,associated_entity_rec_names,filing_hist_rec_names ,audit_rec_names,code99_rec_names]
TABLE_NAMES = ["delete_all_log","master","address","reserved","registered_agent_business","registered_agent_personal","charter_officer_business","charter_officer_personal","charter_names","associated_entity","filing_hist","audit_log","totals_log"]

##################TCAD DATA#######################
tcad_prop_w = [(12,17),(2608,2609),(2033,2058),(2731,2741),(2741,2751),(2751,2761),(1745,1795),(1695,1745),(1675,1685),(1659,1675),(1149,1404),(1915,1930),(1686,1695),(546,596),(0,12),(596, 608),(608,678),(4459,4474),(1039,1049),(1049,1099),(1099,1109),(1109,1139),(1139,1149),(4475,4479),(693,753),(753,813),(813,873),(873,923),(923,974),(978,983),(4135,4175)]
tcad_prop_names = ['ptype','hs','deed','code','code2','code3','lot','block','sub_div','acre','description','value','hood','geo_id','prop_id', 'py_owner_i','prop_owner','st_number','prefix','st_name','suffix','city','zip','unit_num','mail_add_1','mail_add_2','mail_add_3','mail_city','mail_state','mail_zip','DBA']
