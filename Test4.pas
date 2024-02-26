program Test4;
var
   A, B, R, I : integer;

procedure teste (A:integer, B:real);
var
   S,X: real;
begin
   S := A + B * X
end  {verifique se é necessário um ";" no fechamento de um procedimento}

begin
   while (I <= 5) do
   begin
      A := A+1;
      B := B-1;
      R := A + B;
      I := I + 1
   end
end.

{retirar algumas palavras reservadas para gerar erros sintáticos}