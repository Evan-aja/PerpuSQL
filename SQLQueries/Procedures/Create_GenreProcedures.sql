USE PerpuSQL
GO

DROP PROCEDURE ADDGENRE
DROP PROCEDURE DELGENRE
DROP PROCEDURE MODGENRE
DROP PROCEDURE SHOWGENRE
DROP PROCEDURE MASTERGENRE
GO

CREATE PROCEDURE ADDGENRE
    (@GENRE NVARCHAR(30))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA INSERT STARTED'
        INSERT INTO GENRE VALUES(@GENRE)
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
CREATE PROCEDURE DELGENRE
    (@ID_GENRE INT,@GENRE NVARCHAR(30))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA DROP STARTED'
        DELETE FROM GENRE WHERE ID_GENRE=@ID_GENRE AND GENRE=@GENRE
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

CREATE PROCEDURE MODGENRE
    (@ID_GENRE INT,@GENRE NVARCHAR(30))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    PRINT 'TRANSACTION HAS BEGUN'
    BEGIN TRAN
    BEGIN TRY
        PRINT 'DATA UPDATE STARTED'
        UPDATE GENRE
        SET GENRE=@GENRE
        WHERE ID_GENRE=@ID_GENRE
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

CREATE PROCEDURE SHOWGENRE
AS
    SELECT * FROM GENRE
GO

CREATE PROCEDURE MASTERGENRE
    (@ID_GENRE INT=NULL,@GENRE NVARCHAR(30)=NULL,@COMMAND VARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    IF @COMMAND='SELECT'
    BEGIN
        EXEC SHOWGENRE
    END
    ELSE IF @COMMAND='UPDATE'
    BEGIN
        EXEC MODGENRE @ID_GENRE,@GENRE
        EXEC SHOWGENRE
    END
    ELSE IF @COMMAND='ADD'
    BEGIN
        PRINT 'ADD'
        EXEC ADDGENRE @GENRE
        EXEC SHOWGENRE
    END
    ELSE IF @COMMAND='DELETE'
    BEGIN
        EXEC DELGENRE @ID_GENRE,@GENRE
        EXEC SHOWGENRE
    END
    ELSE
    BEGIN
        PRINT 'Available Command=ADD,DELETE,UPDATE,SELECT'
        PRINT 'ADD needs:@GENRE'
        PRINT 'DELETE needs:@ID_GENRE,@GENRE'
        PRINT 'UPDATE needs:@ID_GENRE,@GENRE'
        PRINT 'SELECT is just SELECT * FROM GENRE'
    END
END
GO