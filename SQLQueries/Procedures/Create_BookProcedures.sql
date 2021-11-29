-- USE PerpuSQL
-- GO
-- SELECT * FROM BUKU
-- GO

CREATE PROCEDURE ADDBUKU
    (@JUDUL NVARCHAR(90),@ID_PENULIS INT,@ID_GENRE INT)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        DBCC CHECKIDENT('ID_BUKU',RESEED,0)
        PRINT 'DATA INSERT STARTED'
        INSERT INTO BUKU VALUES(@JUDUL,@ID_PENULIS,@ID_GENRE)
        PRINT 'DATA INSERT FINISHED'
        IF @@TRANCOUNT>0
        BEGIN
            PRINT 'NO ERROR OCCURRED, COMMITING'
            COMMIT TRAN
            PRINT 'DATA COMMITED'
        END
    END TRY
    BEGIN CATCH
        PRINT 'ERROR OCCURRED, ROLLING BACK'
        ROLLBACK TRAN
        PRINT 'DATA RESTORED'
    END CATCH
END
GO
CREATE PROCEDURE DELBUKU
    (@ID_BUKU INT,@JUDUL NVARCHAR(90),@ID_PENULIS INT, @ID_GENRE INT)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA DROP STARTED'
        DELETE FROM BUKU WHERE ID_BUKU=@ID_BUKU AND JUDUL=@JUDUL AND ID_PENULIS=@ID_PENULIS AND ID_GENRE=@ID_GENRE
        PRINT 'DATA DROP FINISHED'
        DBCC CHECKIDENT('ID_BUKU',RESEED,0)
        IF @@TRANCOUNT>0
        BEGIN
            PRINT 'NO ERROR OCCURRED, COMMITING'
            COMMIT TRAN
            PRINT 'DATA COMMITED'
        END
    END TRY
    BEGIN CATCH
        PRINT 'ERROR OCCURRED, ROLLING BACK'
        ROLLBACK TRAN
        PRINT 'DATA RESTORED'
    END CATCH
END
GO

CREATE PROCEDURE MODBUKU
    (@ID_BUKU INT, @JUDUL NVARCHAR(90),@ID_PENULIS INT, @ID_GENRE INT)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA DROP STARTED'
        UPDATE BUKU
        SET JUDUL=@JUDUL,ID_PENULIS=@ID_PENULIS,ID_GENRE=@ID_GENRE
        WHERE ID_BUKU=@ID_BUKU
        PRINT 'DATA DROP FINISHED'
        IF @@TRANCOUNT>0
        BEGIN
            PRINT 'NO ERROR OCCURRED, COMMITING'
            COMMIT TRAN
            PRINT 'DATA COMMITED'
        END
    END TRY
    BEGIN CATCH
        PRINT 'ERROR OCCURRED, ROLLING BACK'
        ROLLBACK TRAN
        PRINT 'DATA RESTORED'
    END CATCH
END
GO

CREATE PROCEDURE SHOWBUKU
AS
    SELECT * FROM BUKU
GO

CREATE PROCEDURE MASTERBUKU
    (@ID_BUKU INT, @JUDUL NVARCHAR(90),@ID_PENULIS INT, @ID_GENRE INT,@COMMAND VARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    IF @COMMAND='SELECT'
    BEGIN
        EXEC SHOWBUKU
    END
    ELSE IF @COMMAND='UPDATE'
    BEGIN
        EXEC MODBUKU @ID_BUKU,@JUDUL,@ID_PENULIS,@ID_GENRE
    END
    ELSE IF @COMMAND='ADD'
    BEGIN
        EXEC ADDBUKU @JUDUL,@ID_PENULIS,@ID_GENRE
    END
    ELSE IF @COMMAND='DELETE'
    BEGIN
        EXEC DELBUKU @ID_BUKU,@JUDUL,@ID_PENULIS,@ID_GENRE
    END
END
GO