Title: Обработка исключений для компонент Zeos
Date: 2008-12-09 14:27
Category: IT
Tags: delphi, zeos
Author: Swasher

Error Handling  
  
If any errors on the client or server side happens, ZDBC raises an
EZSQLException exception. This exception let you know not only the error
message but also the error code from the server.  

    try
        Statement.ExecuteUpdate(...);
    catch
    on E: EZSQLException do
        WriteLn(Format('SQL Error: %d with Code: %d',
        [E.Message, E.ErrorCode]));
    end;
