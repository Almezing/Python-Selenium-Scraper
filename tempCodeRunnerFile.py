table_sht2 = sht2.range(table_total_range).value
table_section_range1 = sht2[:, 0:4]
table_section_range2 = sht2[:, 5:9]

table_section_1 = sht2.range(table_section_range1).value
table_section_2 = sht2.range(table_section_range2).value


# write data
new_locaiton_range = sht1[:, 5:10]
insert_range = sht1[1:,4]
sht1.range('A1').value = table_section_1
sht1.range(insert_range).options(transpose=True).value = data
sht1.range(new_locaiton_range).value = tabl