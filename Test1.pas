program Test1;
   var
      Area, Comprimento, Raio : real; 
   begin   
      Raio := 4;
      Area := 3.14 * Raio * Raio;
      Comprimento := 2 * 3.14 * Raio;
end.

{testar multiplos espacos também}
{gere erros sintáticos, como retirar uma atribuição}
{veja o que a especificação diz em relação ao uso de ";" no último comando. Eh necessário?}