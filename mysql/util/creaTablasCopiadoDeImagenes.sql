USE db;

/* tabla para diferenciar las corridas del script que renombra,
  de manera que podamos en un futuro ejecutar el inverso del
  renombramiento sin revolver carpetas y archivos de una
  misma corrida */
CREATE TABLE IF NOT EXISTS db.corridaYcarpetaRaiz (
    idCorrida INT NOT NULL AUTO_INCREMENT,
    pathRaiz VARCHAR(700) NOT NULL,
    pathDestino VARCHAR(700) NOT NULL,
    PRIMARY KEY (idCorrida),
    UNIQUE indxPathRaiz (pathRaiz)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS db.nombresCarpetas (
    idCorrida INT NOT NULL,
    idreg INT UNSIGNED NOT NULL AUTO_INCREMENT,
    original VARCHAR(4096) NOT NULL, 
    numeroDeArchivos INT NOT NULL,
    FOREIGN KEY (idCorrida) REFERENCES corridaYcarpetaRaiz(idCorrida) ON DELETE RESTRICT,
    PRIMARY KEY (idreg)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS db.nombresArchivos (
    idCorrida INT NOT NULL,
    original VARCHAR(700) NOT NULL,
    alias VARCHAR(700) NOT NULL, 
    idregPadre INT UNSIGNED NOT NULL, 
    /* nombresArchivos.copiado por omisión toma valor 1 declarando que el programa
       pudo copiar el archivo, se actualiza a 0 cuando el programa detecta
       que no fue posible copiar el archivo */
    copiado BIT(1) DEFAULT 1,
    FOREIGN KEY (idCorrida) REFERENCES corridaYcarpetaRaiz(idCorrida) ON DELETE RESTRICT,
    FOREIGN KEY (idregPadre) REFERENCES nombresCarpetas(idreg) ON DELETE RESTRICT,
    /* como los archivos estarán en un solo directorio, nos apoyamos en un
    indice que garantice unicidad de todos los nombres de imágenes */
    UNIQUE idCorridaConNombresArchivos (idCorrida, alias)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;