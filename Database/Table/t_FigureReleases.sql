USE figure_tracker

CREATE TABLE FigureReleases (
	[release_id] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13) FOREIGN KEY REFERENCES Figures ([jan_code]),
	[release_date] DATE NOT NULL,
	[currency_code] CHAR(3) NOT NULL,
	[price] DECIMAL(19,4) NOT NULL,
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE()
)
GO

CREATE INDEX idx1_FigureReleases ON FigureReleases ([currency_code], [price] ASC)
GO

CREATE INDEX idx2_FigureReleases ON FigureReleases ([jan_code])
GO

CREATE TRIGGER trg1_FigureReleases ON FigureReleases
AFTER UPDATE
AS
BEGIN
	UPDATE FigureReleases
	SET [update_date] = GETDATE()
	WHERE [release_id] IN (SELECT DISTINCT [release_id] FROM inserted)
END
GO