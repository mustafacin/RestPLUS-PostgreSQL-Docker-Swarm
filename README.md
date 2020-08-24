# RestPLUS-PostgreSQL-Docker-Swarm
Uygulama Python RestPLUS ile geliştirilmiş Api scriptidir. GET, POST, DELETE ve PUT methodlarını destekler. PostgreSQL veritabanıyla entegre olarak çalışmaktadır. 
Docker Swarm üzerinde çalıştırabilmek için ilk olarak web dizinin imajı alınmalı ve docker-compose.yml dosyasına eklenmelidir. Docker imajları içerisinde kurulu indirilmiş
postgresql ve nginx olmalıdır.
<br>
<h2> Docker Compose İle Çalıştırma</h2>
docker-compose.yml dosyasında /web katergorisindeki image kısımı silinip build: ./web şeklinde yazmak yeterli olacakatır.<br>
<h3>docker-compose build</h3> => imajını alır.<br>
<h3>docker-compose up</h3>  => Uygulamayı çalıştırır. <br>
