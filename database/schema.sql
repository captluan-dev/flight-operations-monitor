USE flights;

CREATE TABLE voos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_voo VARCHAR(10),
    origem VARCHAR(30),
    destino VARCHAR(30),
    status VARCHAR(20),
    horario_coleta DATETIME
);