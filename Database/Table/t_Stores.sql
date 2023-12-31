USE figure_tracker

CREATE TABLE Stores (
	[store_id] INT IDENTITY(1,1) PRIMARY KEY,
	[name] NVARCHAR(100) UNIQUE NOT NULL,
	[store_rating] DECIMAL(2,1) DEFAULT 0,
	[user_rating] DECIMAL(2,1) DEFAULT 0,
	[url] VARCHAR(512) DEFAULT '',
	[create_date] DATETIME DEFAULT GETDATE(),
	[update_date] DATETIME DEFAULT GETDATE()
)
GO

CREATE INDEX idx1_Stores ON Stores ([name])
GO

CREATE INDEX idx2_Stores ON Stores ([store_rating])
GO

CREATE INDEX idx3_Stores ON Stores ([user_rating])
GO

CREATE TRIGGER trg1_Stores ON Stores
AFTER UPDATE
AS
BEGIN
	UPDATE Stores
	SET [update_date] = GETDATE()
	WHERE [store_id] IN (SELECT DISTINCT [store_id] FROM inserted)
END
GO