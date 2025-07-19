/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `db_sistema_reportes_mantenimientos` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci */;
USE `db_sistema_reportes_mantenimientos`;

CREATE TABLE IF NOT EXISTS `departamentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

INSERT INTO `departamentos` (`id`, `descripcion`) VALUES
	(1, 'Informática'),
	(2, 'Recursos Humanos'),
	(3, 'Infraestructura'),
	(4, 'Finanzas');

CREATE TABLE IF NOT EXISTS `equipos_informaticos` (
  `id_equipo` varchar(100) NOT NULL,
  `descripcion` varchar(400) DEFAULT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `tipo_equipo` varchar(50) DEFAULT NULL,
  `id_departamento` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_equipo`) USING BTREE,
  KEY `id_departamento` (`id_departamento`),
  CONSTRAINT `FK__departamentos` FOREIGN KEY (`id_departamento`) REFERENCES `departamentos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;


CREATE TABLE IF NOT EXISTS `incidencias_equipos` (
  `id_incidencia` int(11) NOT NULL AUTO_INCREMENT,
  `id_equipo_i` varchar(100) DEFAULT NULL,
  `ci_usuario` int(11) DEFAULT NULL,
  `fecha_reporte` date DEFAULT NULL,
  `estado_equipo` varchar(50) DEFAULT NULL,
  `desc_incidencia` varchar(700) DEFAULT NULL,
  PRIMARY KEY (`id_incidencia`),
  KEY `FK_incidencias_equipos_equipos_informaticos` (`id_equipo_i`),
  KEY `FK_incidencias_equipos_usuarios` (`ci_usuario`),
  CONSTRAINT `FK_incidencias_equipos_equipos_informaticos` FOREIGN KEY (`id_equipo_i`) REFERENCES `equipos_informaticos` (`id_equipo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_incidencias_equipos_usuarios` FOREIGN KEY (`ci_usuario`) REFERENCES `usuarios` (`cedula`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;


CREATE TABLE IF NOT EXISTS `mantenimientos_equipos` (
  `id_mantenimiento` int(11) NOT NULL AUTO_INCREMENT,
  `id_equipo_i` varchar(100) DEFAULT NULL,
  `ci_usuario` int(11) DEFAULT NULL,
  `fecha_programada` date DEFAULT NULL,
  `estado_mantenimiento` varchar(50) DEFAULT NULL,
  `descripcion` varchar(700) DEFAULT NULL,
  PRIMARY KEY (`id_mantenimiento`),
  KEY `FK_mantenimientos_equipos_equipos_informaticos` (`id_equipo_i`) USING BTREE,
  KEY `FK_mantenimientos_equipos_usuarios` (`ci_usuario`),
  CONSTRAINT `FK_mantenimientos_equipos_equipos_informaticos` FOREIGN KEY (`id_equipo_i`) REFERENCES `equipos_informaticos` (`id_equipo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_mantenimientos_equipos_usuarios` FOREIGN KEY (`ci_usuario`) REFERENCES `usuarios` (`cedula`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;


CREATE TABLE IF NOT EXISTS `usuarios` (
  `cedula` int(11) NOT NULL,
  `nombres` varchar(100) NOT NULL DEFAULT '',
  `nombre_usuario` varchar(100) NOT NULL DEFAULT '',
  `clave` varchar(100) NOT NULL DEFAULT '',
  `tipo_usuario` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

INSERT INTO `usuarios` (`cedula`, `nombres`, `nombre_usuario`, `clave`, `tipo_usuario`) VALUES
	(12345678, 'Admin', 'user_admin', 'admin123', 'Administrador');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
