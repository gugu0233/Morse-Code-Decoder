DECODIFICARE MORSE:

   Pornesc spre dreapta din starea initiala q0, din care trec in stari intermediare (precum 'q.', 'q-') pana intalnesc pe banda simbolul '*'. La fiecare trecere intr-o stare intermediara, sterg caracterul respectiv si ma mut spre dreapta. In momentul in care am ajuns la '*', inseamna ca am decodificat o litera, deci voi trece intr-o stare corespunzatoare fiecarei litere, cu care merg spre dreapta pana la o casuta libera si scriu litera respectiva. Dupa, trec in starea 'qback', cu care merg spre stanga pana la o casuta libera, apoi trec in starea initiala, pentru a relua procesul de decodificare. Asemanator fac si pentru simbolul '/', pe care il tratez ca pe o litera, intrucat trebuie scris pe banda.

IDENTIFICARE CUVINTE CHEIE:

   Pornesc spre dreapta din starea initiala q0, din care trec in stari intermediare (precum 'qH1', 'qS1') daca intalnesc una din literele din cuvintele cheie, altfel raman in starea initiala, pana intalnesc pe banda simbolul '/' sau casuta libera. Pentru cazul in care am gasit casuta libera si starea este 'qHELP' sau 'qSOS', masina accepta inputul, altfel il refuza. Pentru cazul in care am intalnit simbolul '/', daca starea este 'qHELP' sau 'qSOS', masina accepta inputul, altfel trece mai departe. Am folosit o stare auxiliara 'q'' pentru a nu sterge simbolul '/' de pe banda, dupa decodificare.

