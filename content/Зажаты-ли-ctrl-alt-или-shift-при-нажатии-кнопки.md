Title: Зажаты ли Ctrl, Alt или Shift при нажатии кнопки
Date: 2008-12-10 11:10
Category: IT
Tags: delphi
Author: Swasher
Slug: pressed-ctrl-alt-shift

Функция CtrlDown

    ::pascal
    function CtrlDown : Boolean;
    var
    State : TKeyboardState;
    begin
    GetKeyboardState(State);
    Result := ((State[vk\_Control] And 128) \<\> 0);
    end;

Функция ShiftDown

    ::pascal
    function ShiftDown : Boolean;
    var
    State : TKeyboardState;
    begin
    GetKeyboardState(State);
    Result := ((State[vk\_Shift] and 128) \<\> 0);
    end;

Функция AltDown

    ::pascal
    function AltDown : Boolean;
    var
    State : TKeyboardState;
    begin
    GetKeyboardState(State);
    Result := ((State[vk\_Menu] and 128) \<\> 0);
    end;

Обработчик кнопки

    ::pascal
    procedure TForm1.Button1Click(Sender: TObject);
    begin
    if ShiftDown then
    Form1.Caption := 'Shift'
    else
    Form1.Caption := '';
    end;
