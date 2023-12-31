USE master

IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'figure_tracker')
BEGIN
	CREATE DATABASE figure_tracker
END

USE figure_tracker

------ Drop Tables -----------------------------------------------------------------------------
IF EXISTS (SELECT * FROM sysobjects WHERE name = 'FigureReleases' AND xtype = 'U')
BEGIN
	DROP TABLE FigureReleases
END

IF EXISTS (SELECT * FROM sysobjects WHERE name = 'NewListings' AND xtype = 'U')
BEGIN
	DROP TABLE NewListings
END

IF EXISTS (SELECT * FROM sysobjects WHERE name = 'PreownedListings' AND xtype = 'U')
BEGIN
	DROP TABLE PreownedListings
END

IF EXISTS (SELECT * FROM sysobjects WHERE name = 'FigurePriceTracker' AND xtype = 'U')
BEGIN
	DROP TABLE FigurePriceTracker
END

IF EXISTS (SELECT * FROM sysobjects WHERE name = 'Figures' AND xtype = 'U')
BEGIN
	DROP TABLE Figures
END

IF EXISTS (SELECT * FROM sysobjects WHERE name = 'Stores' AND xtype = 'U')
BEGIN
	DROP TABLE Stores
END
------------------------------------------------------------------------------------------------


------ Figures Table ---------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------


---- FigureReleases Table ----------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------


---- Stores Table --------------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------


---- NewListings Table -----------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------


----- PreownedListings Table --------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------


----- FigurePriceTracker Table -----------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------
