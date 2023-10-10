use copiadoDeImagenesCD;
CREATE SCHEMA IF NOT EXISTS copiadoDeImagenesCD DEFAULT CHARACTER SET utf8mb4;

ALTER TABLE nombresArchivos DROP INDEX indxAliasArchivos;
ALTER TABLE nombresArchivos ADD UNIQUE idCorridaConNombresArchivos (idCorrida, alias);

SHOW CREATE TABLE nombresArchivos;

UPDATE nombresCarpetas SET renombrada = 0 WHERE idReg = 12873;
UPDATE nombresArchivos SET renombrado = 0 WHERE idCorrida = 12 AND idregPadre = 12875 AND original = 'año2022.javax';
update carpetasRaiz SET pathRaiz = "63" where idCorrida = 63;

DELETE FROM nombresArchivos WHERE idCorrida = 12;
DELETE FROM carpetasRaiz WHERE idCorrida > 2; /* on delete cascade y no restrict por fa ger */
delete from carpetasRaiz where idCorrida = 61;

DELETE FROM nombresCarpetas where idCorrida = 82;
DELETE FROM nombresArchivos where idCorrida = 82;
