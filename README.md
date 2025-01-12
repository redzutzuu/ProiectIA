# ProiectIA
Proiect Inteligență Artificială

Studenți: Spătaru Alexandru     1405B
Verșanu George-David     1405B

Tema proiectului: Algoritmul minimax cu retezarea alfa-beta aplicat jocului Nim

Descrierea problemei considerate
Jocul Nim este un joc strategic în care doi jucători iau pe rând bețe din mai multe grămezi, având libertatea de a alege câte bețe să ia dintr-o singură grămadă, într-un interval definit. Scopul este de a evita să iei ultimul băț, care semnifică pierderea jocului. Implementarea de față permite jucătorului să concureze împotriva unui bot inteligent care utilizează algoritmul Minimax cu retezarea alfa-beta pentru a lua decizii optime. De asemenea, jocul oferă o interfață grafică pentru o experiență mai plăcută utilizatorului.

Aspecte teoretice privind algoritmul
Algoritmul Minimax este o metodă folosită pentru a determina cea mai bună strategie într-un joc cu sumă zero și perfectă informație. Acesta simulează toate posibilele mutări și contrapărți, evaluând fiecare rezultat. Prin retezarea alfa-beta, spațiul de căutare este redus, eliminând ramurile care nu pot influența decizia finală, ceea ce îmbunătățește performanța.

Modalitatea de rezolvare
Am aplicat algoritmul Minimax cu retezarea alfa-beta pentru a evalua și selecta cele mai bune mutări ale botului. Soluția este implementată astfel:
Funcția minimax evaluează toate opțiunile posibile la o adâncime limitată și decide mutarea optimă, fie pentru bot (maximizare), fie pentru jucător (minimizare).
Funcția bot_decide determină grămada și numărul de bețe de luat pentru a maximiza șansele de câștig.
Interfața grafică, creată cu tkinter, facilitează interacțiunea jucătorului cu jocul, afișând grămezile și gestionând mutările.




Părți semnificative

Funcția pentru calculul Minimax cu retezarea alfa-beta: 


Aceasta evaluează posibilitățile de joc și aplică optimizări alfa-beta pentru a elimina ramurile irelevante.

Funcția pentru determinarea mutării botului: 


Aceasta analizează fiecare grămadă și determină mutarea optimă folosind rezultatele funcției minimax
