# Noul website RMI

Acesta este, în primul rând, un exemplu al temei [RMS
Theme](https://github.com/CNITV/rms-theme).

Site-ul este generat static folosind [Hugo](https://gohugo.io/). El se
instalează foarte ușor, este doar un singur fișier executabil. Se folosește la
linia de comandă.

Făcătorii acestui site sunt [Tudor Roman](https://github.com/tudurom) și
[Ciprian Ionescu](https://github.com/cirip). Faimă și recunoștință eternă pentru
ei!

## Testing and deploying

Folosește comanda `hugo serve -D` pentru a testa site-ul în dezvoltarea
lui. Flag-ul `-D` înseamnă că Hugo va lua în considerare și paginile
marcate ca draft. Testează apoi cu `hugo serve` ca să vezi cum va arăta de
fapt.

Pentru a genera site-ul, șterge folder-ul `public` și execută `hugo`.
Doar atât, fără alt parametru.

Pentru a face modificările live, pune conținutul folder-ului `public` pe
server.

## Instrucțiuni de operare pentru site

Vine o nouă ediție a RMI / RMM, ce faci?

### Modifici fișierul `config.toml`

Acest fișier ține informații precum titlul site-ului, numărul ediției și
perioada în care se desfășoară. În general, trebuie să modifici anul și data.

### Modifici pagina principala în `content/_index.md`

Ca și în cazul fișierului de configurare, aici ar trebui să modifici anul și
data.

### Resetează paginile

Resetarea unei pagini constă în ștergerea conținutului (nu șterge fișierul!) și
înlocuirea lui cu un mesaj ("There are no news currently." ar fi un exemplu
pentru pagina de noutăți). După ce ai înlocuit conținutul, setează pagina ca
draft.

Fiecare pagină are un antet de forma:

```yaml
---
title: "News"
date: 2019-10-02T15:00:00+03:00
menu:
  main:
    parent: "root"
    weight: 1
---
```

Ca să marchezi pagina ca un draft, pui o linie nouă, fără indentare: `draft:
true`:

```yaml
---
title: "News"
date: 2019-10-02T15:00:00+03:00
menu:
  main:
    parent: "root"
    weight: 1
draft: true
---
```

Pagini care trebuiesc resetate sunt paginile cu noutăți, poze, programul concursului, regulament,
rezultate și subiecte. Paginile de noutăți, poze și programul concursului _nu_ trebuie marcate ca draft
totuși.

### Schimbă logo-ul

Logo-ul trebuie să fie un fișier `.png` în `static/assets/logo.png`. Dacă ai și
un roll-up, cum am avut la ediția din 2019, pune-l în
`static/assets/rollup.png`.

### Actualizează sponsorii

Logo-urile sponsorilor sunt în `static/assets/sponsors`. Ele vor fi afișate în
ordinea alfabetică a filename-urilor.

### Actualizează pagina cu comisiile (`csv/*_committee.csv`)

Fiecare fișier `.csv` are 4 coloane, fără antet. Fiecare rând are următoarea
formă:

```csv
Titulatură,Prenume,Nume,Funcție
```

Titulatura este de obicei "Prof." sau nimic. Funcția este "PRESIDENT", "VICE
PRESIDENT" sau nimic.

Mai este și fișierul cu voluntari, în `csv/guides.csv`. El are altă
structură:

```csv
Prenume,Nume,Clasa
```

Nici fișierul cu voluntari nu are antet.

### Actualizează paginile cu documente

Acestea sunt: `content/organisation/programme.md`,
`content/organisation/rules.md` și `content/contest/results.md`.

Fiecare din aceste fișiere are conținut de forma:

```html
{{< section title="Competition Rules" link="/rules.pdf" >}}
{{% pdf file="/rules.pdf" %}}
```

Cred că se înțelege ce valori trebuie să modifci pentru fiecare caz.
S-ar putea ca aceste linii să fie cuprinse într-un comentariu, de forma:

```html
<!--
{{< section title="Programme" link="/program.pdf" >}}
{{% pdf file="/programme.pdf" %}}
-->
```

Când vine momentul, scoți liniile cu `<!--` și `-->`, evident.

Fișierele aferente se pun in `static/`. De exemplu, fișierul din exemplul de mai
sus cu calea `/programme.pdf` trebuie pus in `static/programme.pdf`.

Pagina cu rezultate s-ar putea să aibă mai multe astfel de documente
afișate, pentru diferite tipuri de clasamente.

### Actualizează pagina cu concursul online

Acesta ar trebui să fie actualizat cu perioada în care se va ține, link către
CMS, și document `pdf` cu rezultatele la final.

### Nu uita să publici draft-urile!

După ce lucrezi la pagini marcate ca draft, nu uita să setezi `draft: false`
ca să apară.

### Actualizează noutățile și pozele

Pe măsură ce actualizezi aceste două pagini, nu uita să schimbi și data!
