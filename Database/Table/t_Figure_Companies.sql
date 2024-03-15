USE figure_tracker

CREATE TABLE Figure_Companies (
	[id] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13),
	[company_name] NVARCHAR(100) NOT NULL,
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE(),
	UNIQUE([jan_code], [company_name])
)
GO

CREATE INDEX idx1_Figure_Companies ON Figure_Companies ([jan_code])
GO

CREATE INDEX idx2_Figure_Companies ON Figure_Companies ([company_name])
GO