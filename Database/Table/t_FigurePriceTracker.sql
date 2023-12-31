USE figure_tracker

CREATE TABLE FigurePriceTracker (
	[uid] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13) FOREIGN KEY REFERENCES Figures ([jan_code]),
	[store_id] INT FOREIGN KEY REFERENCES Stores ([store_id]),
	[check_date] DATETIME DEFAULT GETDATE(),
	[currency_code] CHAR(3) NOT NULL,
	[price] DECIMAL(19,4) NOT NULL,
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE(),
	CONSTRAINT UNQ_FigurePriceTracker UNIQUE([jan_code], [store_id])
)
GO

CREATE INDEX idx1_FigurePriceTracker ON FigurePriceTracker ([currency_code], [price] ASC)
GO

CREATE INDEX idx2_FigurePriceTracker ON FigurePriceTracker ([jan_code])
GO

CREATE INDEX idx3_FigurePriceTracker ON FigurePriceTracker ([store_id])
GO

CREATE TRIGGER trg1_FigurePriceTracker ON FigurePriceTracker
AFTER UPDATE
AS
BEGIN
	UPDATE FigurePriceTracker
	SET [update_date] = GETDATE()
	WHERE [uid] IN (SELECT DISTINCT [uid] FROM inserted)
END
GO