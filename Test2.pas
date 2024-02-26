program Test2;
var
   X, A, B : integer;
begin
   A := 5;
   B := 10;
   if (A > B) then
   begin
      X := A;
      A := B;
      B := X   {veja que o último comando de um bloco não possui o ;}
   end         {alguns alunos preferem implementar com ;}
end.	       

{gere erros sintáticos}