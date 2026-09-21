INSERT INTO employees VALUES
('QNA-1001','Maya','Chen','AI Platform','Software Engineer','Regular Full-Time','California','2023-04-17','QNA-1008','Active'),
('QNA-1002','Jordan','Lee','Product Operations','Program Coordinator','Temporary','California','2026-06-01','QNA-1010','Active'),
('QNA-1008','Priya','Nair','AI Platform','Engineering Manager','Regular Full-Time','California','2021-02-08',NULL,'Active'),
('QNA-1010','Evan','Brooks','Product Operations','Director, Product Operations','Regular Full-Time','California','2020-09-14',NULL,'Active')
ON CONFLICT (employee_id) DO UPDATE SET employment_status=EXCLUDED.employment_status;

INSERT INTO pto_balances VALUES
('QNA-1001','Vacation',96,8,'2026-09-20'),
('QNA-1002','Vacation',0,0,'2026-09-20')
ON CONFLICT (employee_id) DO UPDATE SET available_hours=EXCLUDED.available_hours, as_of_date=EXCLUDED.as_of_date;

INSERT INTO benefits VALUES
('QNA-1001','QuantNova Standard PPO','QuantNova Dental Plus','QuantNova Vision',TRUE,'Active','2026-09-20'),
('QNA-1002',NULL,NULL,NULL,FALSE,'Not Eligible - Temporary Classification','2026-09-20')
ON CONFLICT (employee_id) DO UPDATE SET status=EXCLUDED.status, as_of_date=EXCLUDED.as_of_date;
