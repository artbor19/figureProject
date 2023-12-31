USE figure_tracker

CREATE TABLE PreownedListings (
	[entry_id] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13) FOREIGN KEY REFERENCES Figures ([jan_code]),
	[store_id] INT FOREIGN KEY REFERENCES Stores ([store_id]),
	[currency_code] CHAR(3) NOT NULL,
	[price] DECIMAL(19,4) NOT NULL,
	[is_available] BIT DEFAULT 0,
	[is_limited_edition] BIT DEFAULT 0,
	[condition] VARCHAR(100),
	[recent_check_date] DATETIME DEFAULT GETDATE(),
	[url] VARCHAR(512) DEFAULT '',
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE()
)
GO

CREATE INDEX idx1_PreownedListings ON PreownedListings ([jan_code])
GO

CREATE INDEX idx2_PreownedListings ON PreownedListings ([store_id])
GO

CREATE INDEX idx3_PreownedListings ON PreownedListings ([currency_code], [price] ASC)
GO

CREATE INDEX idx4_PreownedListings ON PreownedListings ([is_available])
GO

CREATE TRIGGER trg1_PreownedListings ON PreownedListings
AFTER UPDATE
AS
BEGIN
	UPDATE PreownedListings
	SET [update_date] = GETDATE()
	WHERE [entry_id] IN (SELECT DISTINCT [entry_id] FROM inserted)
END
GO
