USE figure_tracker

CREATE TABLE Figure_Characters (
	[id] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13),
	[character_name] NVARCHAR(100) NOT NULL,
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE(),
	UNIQUE([jan_code], [character_name])
)
GO

CREATE INDEX idx1_Figure_Characters ON Figure_Characters ([jan_code])
GO

CREATE INDEX idx2_Figure_Characters ON Figure_Characters ([character_name])
GO
