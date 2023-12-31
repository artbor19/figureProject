USE figure_tracker

CREATE TABLE Figures (
	[jan_code] CHAR(13) PRIMARY KEY,
	[name] NVARCHAR(100) NOT NULL,
	[manufacturer] NVARCHAR(30)NOT NULL,
	[url] VARCHAR(512) DEFAULT '',
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE()
)
GO

CREATE INDEX idx1_Figures ON Figures ([manufacturer])
GO

CREATE INDEX idx2_Figures ON Figures ([name])
GO

CREATE TRIGGER trg1_Figures ON Figures
AFTER UPDATE
AS
BEGIN
	UPDATE Figures
	SET [update_date] = GETDATE()
	WHERE [jan_code] IN (SELECT DISTINCT [jan_code] FROM inserted)
END
GO