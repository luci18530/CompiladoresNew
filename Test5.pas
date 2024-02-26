program Test5;
var
   A, B, R, I : integer;
begin
   for I := 1 to 5 do
   begin
      A := A * A;
      B := B * A;
      R := A + B
   end
end.

{utilizar mais de um for - encadeado}
{cuidado com o ";" entenda o que a gramática está pedindo}