# Internet-Scraping
Vreau sa implementez o aplicatie auxiliara site-ului eMAG care sa permita utilizatorilor sa monitorizeze preturile si sa primeasca alerte atunci cand pretuirle scad sub o anumita valoare prag setata de ei.
Aceasta aplicatie are rolul de a urmari evolutia preturilor.

## 18.06.2024
 - am implementat functionalitatea care construieste URL-ul de cautare pe eMAG al unui produs 
 - fac o cerere HTTP GET catre URL-ul produsului si parsez pentru a obtin pretul produsului
 - fac verificare daca pretul este mai mic decat cel pe care l a ales utilizatorul sa primeasca o notificare

 ## 19.06.2024 
- am implementat o parte din  interfata grafica pentru aplicatie
- m-am documentat si am gasit o modalitate de a trimite email folosindu-ma de bibliotecile puse la dispozitie de python
- am facut configurarile necesare din contul de gmail creat special pentru trimiterea emailurilor 


## 20.06.2024
- am facut o prima pagina care sa afiseze un mesaj de "Bun venit!" 
- ofer posibilitatea userului sa aleaga intre modurile in care vrea sa lucreze (Local -> adica sa primeasca notificari doar in aplicatie si prin Email -> sa fie anuntat printr-un email daca pretul produsului selectat de el a scazut sub o anumita valoare)
- exista 2 pagini diferite pentru fiecare optiune selectata
- pentru meniul de Email avem o sectiune unde userul trebuie sa isi introduca emailul intr-un text box
- urmeaza pagina de selectare produs care este comuna atat pentru optiunea de Email cat si pentru cea de Local 
- userul poate sa primeasca o notificare in aplicatie si/ sau email in functie de modul in care se afla
- trebuie sa implementez si un buton de back pentru a ma putea intoarce din meniul de optiune cu email in cel de Local

# 21.06.2024
- am reusit sa fac scarping pe si pe site-ul Altex
- rezultatul paginii vine intr-un xhr si a trebuit sa gestionez acest rezultat
- am inceput sa implementez interfata grafica a aplicatiei


## 25.06.2024
- am facut functionalitatea de copy link care creeaza linkul (in cazul site-ului Altex) sau il ia din pagina site-ului (Emag) dupa care o copiaza in clipboard-ul userului
- am lucrat in continuare la interfata grafica a aplicatiei
