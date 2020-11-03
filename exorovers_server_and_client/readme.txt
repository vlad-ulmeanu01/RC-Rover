rover-ul transmite informatii prin hotspot catre laptop, care le pune pe un grafic, sau pe margine

grafic: umiditate (verde), ( 0 - 100% )
	temp (rosu), ( 0-100 grade C )
	pres (albastru), ( 950-1050 mB )
	vibratii(mov) (<0.2 m/s^2),
	inductie magnetica (galben) (0-100 T)
margine: date de pe arduino (senzori nh4, co2, proximitate)

graficul nu are legenda, spuneti voi parametrii

conectati laptopul la hotspot,deschideti cmd-ul si scrieti ipconfig. copiati adresa ipv4 ( ex:192.168.100.10 ) si inlocuiti-o la linia 33 in client_classic ( IN RPI )

porniti serverul(rulati din folder-ul server/hau2018.py cu python 3.6)

acum pe raspberry pi conectati-l la acelasi hotspot: daca este arduino-ul conectat si este modificata linia cu IP-ul, puteti sa rulati client_classic tot in python 3.6. 
In scurt timp o sa apara informatiile pe grafic o data pe sec

Daca vreti sa dati share screen, rulati VNC viewer si pe laptop si dupa aceea pe rover.
cautati vnc viewer in search-ul de la start


Clientul din folder pare sa fie client/arduino/ar