USE figure_tracker

CREATE TABLE NewListings (
	[entry_id] INT IDENTITY(1,1) PRIMARY KEY,
	[jan_code] CHAR(13) FOREIGN KEY REFERENCES Figures ([jan_code]),
	[store_id] INT FOREIGN KEY REFERENCES Stores ([store_id]),
	[currency_code] CHAR(3) NOT NULL,
	[price] DECIMAL(19,4) NOT NULL,
	[is_available] BIT DEFAULT 0,
	[is_limited_edition] BIT DEFAULT 0,
	[recent_check_date] DATETIME DEFAULT GETDATE(),
	[url] VARCHAR(512) DEFAULT '',
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE(),
	CONSTRAINT UNQ_NewListings UNIQUE([jan_code], [store_id], [is_limited_edition])
)
GO

CREATE INDEX idx1_NewListings ON NewListings ([jan_code])
GO

CREATE INDEX idx2_NewListings ON NewListings ([store_id])
GO

CREATE INDEX idx3_NewListings ON NewListings ([currency_code], [price] ASC)
GO

CREATE INDEX idx4_NewListings ON NewListings ([is_available])
GO

CREATE TRIGGER trg1_NewListings ON NewListings
AFTER UPDATE
AS
BEGIN
	UPDATE NewListings
	SET [update_date] = GETDATE()
	WHERE [entry_id] IN (SELECT DISTINCT [entry_id] FROM inserted)
END
GO