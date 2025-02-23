function [] = gato_pro ()
% Aqui hay que describir lo que realiza el programa
IA.caja = figure ('Unit','Pixels', ...
        'Position',    [500 300 350 350], ...
        'Menubar',     'None', ...
        'Numbertitle', 'Off', ...
        'Name',        'Juego del Gato', ...
        'Resize',      'Off');
IA.jg = uicontrol(IA.caja, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [140 5 70 40], ...
    'Fontsize', 15, ...
    'Tag',      'Jugar', ...
    'String',   {'Jugar'}, ...
    'Visible',  'Off', ...
    'Callback', {@jg_call, IA});
%=======================================================%

%==============> Grupo de botones 1 <===================%
IA.gb1 = uibuttongroup ('Unit', 'Pixels', ...
        'Position', [15 80 320 170], ...
        'Visible',  'On', ...
        'Tag',      'Grupo1');
 
IA.p1 = uicontrol(IA.gb1, ... 
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [65 130 200 30], ...
    'Fontsize', 15, ...
    'String',   'Un Solo Jugador', ...
    'Callback', {@p1_call, IA});
 
IA.p2 = uicontrol(IA.gb1, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [110 10 100 30], ...
    'Fontsize', 15, ...
    'String',   'Exit', ...
    'Callback', {@p2_call, IA});
%==================================================%
%==========> Grupo de botones 2 <==================%
IA.gb2 = uibuttongroup ('Unit', 'Pixels', ...
        'Position', [55 50 240 240], ...
        'Visible',  'Off', ...
        'Tag',      'Grupo2');
 
IA.pp(1) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [10 160 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp1', ...
    'Callback', {@pp1_call, IA});
 
IA.pp(2) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [85 160 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp2', ...
    'Callback', {@pp2_call, IA});
 
IA.pp(3) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [160 160 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp3', ...
    'Callback', {@pp3_call, IA});
 
IA.pp(4) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [10 85 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp4', ...
    'Callback', {@pp4_call, IA});
 
IA.pp(5) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [85 85 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp5', ...
    'Callback', {@pp5_call, IA});
 
IA.pp(6) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [160 85 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp6', ...
    'Callback', {@pp6_call, IA});
 
IA.pp(7) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [10 10 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp7', ...
    'Callback', {@pp7_call, IA});
 
IA.pp(8) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [85 10 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp8', ...
    'Callback', {@pp8_call, IA});
 
IA.pp(9) = uicontrol(IA.gb2, ...
    'Style',    'Push', ...
    'Unit',     'Pixels', ...
    'Position', [160 10 70 70], ...
    'Fontsize', 15, ...
    'Tag',      'pp9', ...
    'Callback', {@pp9_call, IA});
 
set(IA.pp(:), 'Callback', {@pp_call, IA});
%=====================================================%
IA.t2 = uicontrol('Style', 'Text', ...
    'Unit',     'Pixels', ...
    'Position', [80 295 190 50], ...
    'Fontname', 'Comic Sans MS', ...
    'Fontsize', 25, ...
    'Tag',      'Titulo', ...
    'String',   'GATO');
% %=====================================================%
% %==================  Funciones =============================%
% %===========================================================%
% function [] = p1_call (varargin)
% global Turno Tabla Sec
% %Turno es igual a la correspondencia en el tiro 2 para máquina 1 para humano
% %Tabla vector que contiene las 9 posiciones del gato
% %sec: secuencia de tiros
% set (findobj ('Tag','Grupo1'), 'Visible', 'Off');
% set (findobj ('Tag','Grupo2'), 'Visible', 'On');
% Turno = ceil( rand*2 );
% if (Turno == 1)
%     set(findobj('Tag','Titulo'), 'String', 'Turno Humano', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
% elseif (Turno == 2)
%     set(findobj('Tag','Titulo'), 'String', 'Turno Compu', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
% end
% 
% Tabla = zeros(1,9);
% Sec = {[5 1 3 7 9 2 4 6 8];
%        [5 7 1 9 3 4 8 2 6];
%        [5 3 1 9 7 2 6 4 8];
%        [5 9 3 7 1 6 8 4 2];};
% Sec=Sec{randi(4)};
% if (Turno == 2)
%     Decide();
% end
% %=====================================================================%
% function [] = p2_call (varargin)
% clc, clear,  close all;
% 
% %=====================================================================%
% function Decide()
% global Tabla Sec num %Num será aquello que irá adentro de la tabla
% pause(1);
% num = Sec(1,1);
% ClickTabla(num);
% %======================================================%
% function ClickTabla(num)
% global Turno Tabla Sec
% Sec(Sec == num) = [];
% Tabla(num) = Turno;
% if (Turno == 1)
%     set(findobj('Tag', strcat('pp',num2str(num))), 'Val', 1, 'String', 'X', 'Fontsize', 35);
%     Turno = 2;
%     set(findobj('Tag','Titulo'), 'String', 'Turno Compu', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
% elseif (Turno == 2)
%     set(findobj('Tag', strcat('pp',num2str(num))), 'Val', 1, 'String', 'O', 'Fontsize', 35);
%     Turno = 1;
%     set(findobj('Tag','Titulo'), 'String', 'Turno Humano', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
% end
% 
% [win] = RevisaTabla(Tabla);
% 
% if (win ~= 0)
%     set(findobj('Tag','Jugar'),  'Visible', 'On');
% 	if (win == 1)
%         set(findobj('Tag','Titulo'), 'String', 'Gana Humano');
%     elseif (win == 2)
%         set(findobj('Tag','Titulo'), 'String', 'Gana Compu');
%     end
% end
% 
% if (win == 0)
%     if isempty(Sec)
%         set(findobj('Tag','Jugar'),  'Visible', 'On')
%         set(findobj('Tag','Titulo'), 'String', 'Empate');
%         return
%     end
%     if (Turno == 2)
%         Decide();
%     end
% end
% %===================================================%
% function [win] = RevisaTabla(b)    
% win = 0;
% for i = 1:2
%     if b(1)==i && b(2)==i && b(3)==i
%         win = i;
%     elseif b(4)==i && b(5)==i && b(6)==i
%         win = i;
%     elseif b(7)==i && b(8)==i && b(9)==i
%         win = i;
%     elseif b(1)==i && b(4)==i && b(7)==i
%         win = i;
%     elseif b(2)==i && b(5)==i && b(8)==i
%         win = i;
%     elseif b(3)==i && b(6)==i && b(9)==i
%         win = i;
%     elseif b(1)==i && b(5)==i && b(9)==i
%         win = i;
%     elseif b(3)==i && b(5)==i && b(7)==i
%         win = i;
%     end
% end
% %=====================================================%
% function [] = pp_call(varargin)
% global num
% pos = get(gcbo, 'Position');
% col = ceil (pos(1)/75.0);
% fil = 4.0 - ceil(pos(2)/75.0);
% if (fil == 1)
%     num = col + 0;
% elseif (fil == 2)
%     num = col + 3;
% elseif (fil == 3)
%     num = col + 6;
% end
% ClickTabla(num)
% 
% function [] = jg_call(varargin)
% clc, clear, close all;
% gato_pro();

%==================  Funciones =============================%
%===========================================================%
function [] = p1_call (varargin)
global Turno Tabla Sec  
set (findobj ('Tag','Grupo1'), 'Visible', 'Off');
set (findobj ('Tag','Grupo2'), 'Visible', 'On');
Turno = ceil( rand*2 );
if (Turno == 1)
    set(findobj('Tag','Titulo'), 'String', 'Turno Humano', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
elseif (Turno == 2)
    set(findobj('Tag','Titulo'), 'String', 'Turno Compu', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
end

Tabla = zeros(1,9);
% Sec = [5 1 3 7 9 2 4 6 8];
% Sec = [5 9 1 3 7 6 4 2 8];
Sec = [1:9];
if (Turno == 2)
    Decide();
end
%=====================================================================%
function [] = p2_call (varargin)
clc, clear,  close all;

%=====================================================================%
function Decide()
global Tabla Sec num
num = 0;
i = 1;
j = 2;
pause(1);
% % % num = Sec(1,1);
while (num == 0)
    if i==1     
     s=[1 2 3];
    elseif i==2
     s=[4 5 6];
    elseif i==3
     s=[7 8 9];
    elseif i==4
     s=[1 4 7];
    elseif i==5
     s=[2 5 8];
    elseif i==6
     s=[3 6 9];
    elseif i==7
     s=[1 5 9];
    elseif i==8
     s=[3 5 7];
    elseif i==9 && j==2
        j=1;
        i=1;
    elseif i==9 && j==1
        num = Sec( ceil( rand*( length( Sec) ) ) );
    end
if (Tabla(s(1)) == j && Tabla(s(2)) == j && Tabla(s(3)) == 0)
        num = s(3);
elseif Tabla(s(1)) == j && Tabla(s(2)) == 0 && Tabla(s(3)) == j
        num = s(2);
elseif Tabla(s(1)) == 0 && Tabla(s(2)) == j && Tabla(s(3)) == j
        num = s(1);
end
    i=i+1;
end
ClickTabla(num);
%======================================================%
function ClickTabla(num)
global Turno Tabla Sec
Sec(Sec == num) = [];
Tabla(num) = Turno;
if (Turno == 1)
    set(findobj('Tag', strcat('pp',num2str(num))), 'Val', 1, 'String', 'X', 'Fontsize', 35);
    Turno = 2;
    set(findobj('Tag','Titulo'), 'String', 'Turno Compu', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
elseif (Turno == 2)
    set(findobj('Tag', strcat('pp',num2str(num))), 'Val', 1, 'String', 'O', 'Fontsize', 35);
    Turno = 1;
    set(findobj('Tag','Titulo'), 'String', 'Turno Humano', 'Fontsize', 15, 'Backg', [1 0.7 0.7]);
end

[win] = RevisaTabla(Tabla);

if (win ~= 0)
    set(findobj('Tag','Jugar'),  'Visible', 'On');
if (win == 1)
        set(findobj('Tag','Titulo'), 'String', 'Gana Humano');
    elseif (win == 2)
        set(findobj('Tag','Titulo'), 'String', 'Gana Compu');
    end
end

if (win == 0)
    if isempty(Sec)
        set(findobj('Tag','Jugar'),  'Visible', 'On')
        set(findobj('Tag','Titulo'), 'String', 'Empate');
        return
    end
    if (Turno == 2)
        Decide();
    end
end
%===================================================%
function [win] = RevisaTabla(b)    
win = 0;
for i = 1:2
    if b(1)==i && b(2)==i && b(3)==i
        win = i;
    elseif b(4)==i && b(5)==i && b(6)==i
        win = i;
    elseif b(7)==i && b(8)==i && b(9)==i
        win = i;
    elseif b(1)==i && b(4)==i && b(7)==i
        win = i;
    elseif b(2)==i && b(5)==i && b(8)==i
        win = i;
    elseif b(3)==i && b(6)==i && b(9)==i
        win = i;
    elseif b(1)==i && b(5)==i && b(9)==i
        win = i;
    elseif b(3)==i && b(5)==i && b(7)==i
        win = i;
    end
end
%=====================================================%
function [] = pp_call(varargin)
global num
pos = get(gcbo, 'Position');
col = ceil (pos(1)/75.0);
fil = 4.0 - ceil(pos(2)/75.0);
if (fil == 1)
    num = col + 0;
elseif (fil == 2)
    num = col + 3;
elseif (fil == 3)
    num = col + 6;
end
ClickTabla(num)

function [] = jg_call(varargin)
close all;
gato_pro();

% 10 veces con probabilístico
% 10 veces con el segundo
% ver cuantas veces gana el sujeto de prueba, la máquina o empate
%P1. Realizar cálculo formal para las 4 secuencias del probabilístico,
%analizar bloqueos del segundo programa, una vez analizada la lógica pasar
%programa a python con interfaz gráfica. El día martes se explicará un
%tercer gato, el cual tendrá aprendizaje, almacenar datos, jugar contra el
%probabilístico y el segundo contra el tercero, orientado a objetos