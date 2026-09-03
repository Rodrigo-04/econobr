--verifica se o banco de dados já existe para então criar
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'econobr')
BEGIN
    CREATE DATABASE econobr;
END
GO

--usa o banco de dados
USE econobr;
GO

--cria as tabelas
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'selic')
BEGIN
    CREATE TABLE selic (
        id INT IDENTITY(1,1) PRIMARY KEY,
        data DATE NOT NULL,
        valor DECIMAL(10,4) NOT NULL,
        criado_em DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_selic_data UNIQUE (data)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ipca')
BEGIN
    CREATE TABLE ipca (
        id INT IDENTITY(1,1) PRIMARY KEY,
        data DATE NOT NULL,
        valor DECIMAL(10,4) NOT NULL,
        criado_em DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_ipca_data UNIQUE (data)
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'cambio')
BEGIN
    CREATE TABLE cambio (
        id INT IDENTITY(1,1) PRIMARY KEY,
        data DATE NOT NULL,
        valor DECIMAL(10,4) NOT NULL,
        criado_em DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_cambio_data UNIQUE (data)
    );
END
GO