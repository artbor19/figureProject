USE figure_tracker

CREATE TABLE FigurePriceTracker (
	[uid] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13) FOREIGN KEY REFERENCES Figures ([jan_code]),
	[store_id] INT FOREIGN KEY REFERENCES Stores ([store_id]),
	[check_date] DATETIME DEFAULT GETDATE(),
	[currency_code] CHAR(3) NOT NULL,
	[price] DECIMAL(19,4) NOT NULL,
	[is_limited_edition] BIT DEFAULT 0,
	[is_preowned] BIT DEFAULT 0,
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE()
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

CREATE TRIGGER trg2_FigurePriceTracker ON NewListings
AFTER INSERT
AS
BEGIN
	INSERT INTO FigurePriceTracker ([jan_code], [store_id], [is_limited_edition], [check_date], [currency_code], [price])
		SELECT [jan_code], [store_id], [is_limited_edition], [recent_check_date], [currency_code], [price] FROM inserted
END
GO

CREATE TRIGGER trg3_FigurePriceTracker ON NewListings
AFTER UPDATE
AS
BEGIN
	INSERT INTO FigurePriceTracker ([jan_code], [store_id], [is_limited_edition], [check_date], [currency_code], [price])
		SELECT [jan_code], [store_id], [is_limited_edition], [recent_check_date], [currency_code], [price] FROM inserted
END
GO

CREATE TRIGGER trg4_FigurePriceTracker ON PreownedListings
AFTER INSERT
AS
BEGIN
	INSERT INTO FigurePriceTracker ([jan_code], [store_id], [is_limited_edition], [is_preowned], [check_date], [currency_code], [price])
		SELECT [jan_code], [store_id], [is_limited_edition], 0, [recent_check_date], [currency_code], [price] FROM inserted
END
GO

CREATE TRIGGER trg5_FigurePriceTracker ON PreownedListings
AFTER UPDATE
AS
BEGIN
	INSERT INTO FigurePriceTracker ([jan_code], [store_id], [is_limited_edition], [is_preowned], [check_date], [currency_code], [price])
		SELECT [jan_code], [store_id], [is_limited_edition], 0, [recent_check_date], [currency_code], [price] FROM inserted
END
GO