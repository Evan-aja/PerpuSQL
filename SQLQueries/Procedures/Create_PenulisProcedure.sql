USE PerpuSQL
GO

DROP PROCEDURE ADDPENULIS
DROP PROCEDURE DELPENULIS
DROP PROCEDURE MODPENULIS
DROP PROCEDURE SHOWPENULIS
DROP PROCEDURE MASTERPENULIS
GO

CREATE PROCEDURE ADDPENULIS
    (@NAMA_DEPAN NVARCHAR(50),@NAMA_BELAKANG NVARCHAR(70))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA INSERT STARTED'
        INSERT INTO PENULIS VALUES(@NAMA_DEPAN,@NAMA_BELAKANG)
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
CREATE PROCEDURE DELPENULIS
    (@ID_PENULIS INT,@NAMA_DEPAN NVARCHAR(50),@NAMA_BELAKANG NVARCHAR(70))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA DROP STARTED'
        DELETE FROM PENULIS WHERE ID_PENULIS=@ID_PENULIS AND NAMA_DEPAN=@NAMA_DEPAN AND NAMA_BELAKANG=@NAMA_BELAKANG
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

CREATE PROCEDURE MODPENULIS
    (@ID_PENULIS INT,@NAMA_DEPAN NVARCHAR(50),@NAMA_BELAKANG NVARCHAR(70))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA UPDATE STARTED'
        UPDATE PENULIS
        SET NAMA_DEPAN=@NAMA_DEPAN,NAMA_BELAKANG=@NAMA_BELAKANG
        WHERE ID_PENULIS=@ID_PENULIS
        PRINT 'DATA UPDATE FINISHED'
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

CREATE PROCEDURE SHOWPENULIS
AS
    SELECT * FROM PENULIS
    ORDER BY ID_PENULIS ASC
GO

CREATE PROCEDURE MASTERPENULIS
    (@ID_PENULIS INT=NULL,@NAMA_DEPAN NVARCHAR(50)=NULL,@NAMA_BELAKANG NVARCHAR(70)=NULL,@COMMAND VARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    IF @COMMAND='SELECT'
    BEGIN
        EXEC SHOWPENULIS
    END
    ELSE IF @COMMAND='UPDATE'
    BEGIN
        EXEC MODPENULIS @ID_PENULIS,@NAMA_DEPAN,@NAMA_BELAKANG
        EXEC SHOWPENULIS
    END
    ELSE IF @COMMAND='ADD'
    BEGIN
        PRINT 'ADD'
        EXEC ADDPENULIS @NAMA_DEPAN,@NAMA_BELAKANG
        EXEC SHOWPENULIS
    END
    ELSE IF @COMMAND='DELETE'
    BEGIN
        EXEC DELPENULIS @ID_PENULIS,@NAMA_DEPAN,@NAMA_BELAKANG
        EXEC SHOWPENULIS
    END
    ELSE
    BEGIN
        PRINT 'Available Command=ADD,DELETE,UPDATE,SELECT'
        PRINT 'ADD needs:@NAMA_DEPAN,@NAMA_BELAKANG'
        PRINT 'DELETE needs:@ID_PENULIS,@NAMA_DEPAN,@NAMA_BELAKANG'
        PRINT 'UPDATE needs:@ID_PENULIS,@NAMA_DEPAN,@NAMA_BELAKANG'
        PRINT 'SELECT is just SELECT * FROM PENULIS'
    END
END
GO