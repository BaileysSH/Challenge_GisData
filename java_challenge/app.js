function isPalindrome(str) {
  var len = Math.floor(str.length / 2);
  for (var i = 0; i < len; i++)
    if (str[i] !== str[str.length - i - 1])
      return false;
  return true;
}

// Mantenere questa dichiarazione di funzione
const process = () => {
  
  let test = words.filter(c => c.length >= 5).filter(c => isPalindrome(c));

  // Dopo aver analizzato tutte le parole, quelle che hanno superato
  // i criteri, vanno stampate nella pagina HTML, una per ogni riga
  document.getElementById("response").innerHTML = test.join("<br />");
};