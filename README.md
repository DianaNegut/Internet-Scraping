# Internet-Scraping
Vreau sa implementez o aplicatie auxiliara site-ului eMAG care sa permita utilizatorilor sa monitorizeze preturile si sa primeasca alerte atunci cand pretuirle scad sub o anumita valoare prag setata de ei.
Aceasta aplicatie are rolul de a urmari evolutia preturilor.

## 18.06.2024
 -> am implementat functionalitatea care construieste URL-ul de cautare pe eMAG al unui produs 
 -> fac o cerere HTTP GET catre URL-ul produsului si parsez pentru a obtin pretul produsului
 -> fac verificare daca pretul este mai mic decat cel pe care l a ales utilizatorul sa primeasca o notificare