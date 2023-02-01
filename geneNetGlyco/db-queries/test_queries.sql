select count(*) from TF_Master
select distinct(cell_type_id) from TF_Master

with dataset as (
select tf, target, confidence from TF_Master where cell_type_id in ( 
	select cell_type_id from TF_Tags where tag in
		('brain', 'adult') group by 
		cell_type_id having count(cell_type_id) = 2
	)
)
select * from dataset where 
confidence >= (select percentile_disc(0.99) WITHIN GROUP (ORDER BY confidence) from dataset)

truncate TF_Master
drop table TF_Master