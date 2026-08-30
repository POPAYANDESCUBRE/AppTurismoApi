-- Script SQL para insertar tipos de restaurantes de ejemplo
-- Ejecutar después de las migraciones

-- Insertar tipos de restaurantes
INSERT INTO restaurantes."TipoRestaurante" (nombre, fecha_creacion, fecha_actualizacion, estado, eliminado_en)
VALUES
    ('Heritage Dining', NOW(), NOW(), TRUE, NULL),
    ('Casual Dining', NOW(), NOW(), TRUE, NULL),
    ('Fine Dining', NOW(), NOW(), TRUE, NULL),
    ('Fast Food', NOW(), NOW(), TRUE, NULL),
    ('Cafetería', NOW(), NOW(), TRUE, NULL),
    ('Bistro', NOW(), NOW(), TRUE, NULL),
    ('Comida Rápida', NOW(), NOW(), TRUE, NULL),
    ('Parrilla', NOW(), NOW(), TRUE, NULL),
    ('Mariscos', NOW(), NOW(), TRUE, NULL),
    ('Vegetariano', NOW(), NOW(), TRUE, NULL);

-- Verificar inserción
SELECT * FROM restaurantes."TipoRestaurante";
