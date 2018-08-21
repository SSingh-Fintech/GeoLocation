DELIMITER //
CREATE DEFINER=`webuser`@`%` PROCEDURE `SP_IIS_XFF`()
BEGIN	
	Insert into XFF_Info (`ip`)
	select distinct X_Forwarded from IISLog where X_Forwarded REGEXP '^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$' and X_Forwarded not in (select ip from XFF_Info) and id > (select id from IISLast_Updated_ID);
	update IISLast_Updated_ID set `id` = (select max(id) from IISLog);
END//
DELIMITER ;