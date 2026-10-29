# pokemon-battle-web

Aplicación web hecha con Flask donde un entrenador elige un Pokémon legendario y se enfrenta a un rival aleatorio.

## Estructura del proyecto

```
pokemon-battle-web/
├── app/
│   ├── main.py            # Aplicación Flask (rutas y lógica)
│   ├── templates/         # Plantillas Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── listado-pkm.html
│   │   ├── pokemon_card.html
│   │   ├── pokemon.html
│   │   └── battle.html
│   └── static/css/styles.css
└── data/pokemons-legendary.json
```

### FASE 0:
##### Objetivos
- Sentar las bases del proyecto
- Crear un repositorio (Github)
- Preparar el entorno de desarrollo.
- Arrancar una primera aplicación Flask muy simple que muestre un mensaje en el navegador.
- Renderizar plantillas empleando la sintaxis básica.

### Fase I
##### Objetivos
- Crear las primeras vistas HTML con Jinja2 y sentar las bases de la interfaz:
- Página de inicio.
- Página con un listado de Pokémon.
- Página de detalle de un Pokémon.
- Cargar datos desde un fichero .json en la aplicación.

**Cómo funciona:** al arrancar, `main.py` lee `pokemons-legendary.json` una sola vez y lo guarda en la variable `DATOS`. A cada Pokémon se le añade el campo `media` (media de sus estadísticas), que se usa para filtrar y para mostrar en el detalle.

### Fase II
##### Objetivos
- Emplear formularios para recoger la información introducida por el usuario.
- Pasar parámetros por URL.
- Validación de los datos en el servidor.

**Cómo funciona:**
- **Formulario del entrenador (`/`)**: el nombre debe tener entre 3 y 15 caracteres. Si no se cumple, se vuelve a mostrar el formulario con un mensaje de error.
- **Formulario de elegir Pokémon (`/pokemons`, POST)**: se comprueba que el nombre no esté vacío y que exista en `DATOS`. Si falla, el error se muestra bajo el campo.
- **Filtros del listado (`/pokemons`, GET)**: filtran por tipo y por media de estadísticas (baja < 100, media 100-112, alta > 112). Se leen con `request.args.get`.

### Fase III
##### Objetivos
- Comprender cómo mantener datos de usuario entre distintas peticiones HTTP.
- Utilizar sesiones en Flask para conservar información durante la navegación.
- Decidir qué datos de la aplicación tiene sentido guardar en la sesión.

#### 1. Preparación del entorno

Flask incluye sesiones de serie, así que no hace falta instalar nada. Solo hay que definir una clave secreta con la que Flask firma la cookie de sesión:

```python
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")
```

En un entorno real la clave se define como variable de entorno (`SECRET_KEY`) y no se sube al repositorio.

La sesión de Flask es una **cookie firmada**: el navegador puede leerla pero no modificarla sin invalidarla. Por eso no se guarda nada sensible en ella.

#### 2. Mantenimiento del estado en sesión

**Entrenador y protección de pantallas**

Cuando el entrenador envía un nombre válido en `/`, se guarda en `session["trainer"]` y se redirige al listado. Ya no viaja por la URL.

Las pantallas protegidas usan el decorador `@login_requerido`, que se ejecuta antes de la vista: si no hay `trainer` en la sesión, redirige a `/`.

```python
def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    return wrapper
```

Está aplicado en `/pokemons`, `/pokemon/<id>` y `/battle`.

**Datos guardados en la sesión y por qué**

| Clave | Qué guarda | Por qué |
|---|---|---|
| `trainer` | Nombre del entrenador | Identifica al usuario y permite bloquear el acceso al resto de pantallas si no existe. Antes se pasaba por la URL. |
| `batalla` | `id` del Pokémon elegido, `id` del rival y lista de 4 índices de ataques | El rival y los ataques se sortean al azar. Si no se guardaran, al recargar `/battle` cambiarían y sería otra batalla distinta. Al guardarlos, la batalla se mantiene igual al recargar o al volver más tarde. |

**Por qué se guardan ids e índices y no los Pokémon completos:** la cookie de sesión tiene un límite de unos 4 KB y los datos completos ya están en `DATOS`. Guardar solo identificadores mantiene la cookie pequeña y evita duplicar información. En `/battle` se reconstruye todo buscando esos ids en `DATOS`.

**Qué no se guarda:** los filtros del listado (`tipo` y `media`) siguen viajando por la URL con GET (`/pokemons?tipo=fire&media=alta`). Así se pueden recargar y compartir enlaces filtrados.

**Flujo de la batalla:**
1. En `/pokemons` el usuario escribe un Pokémon y se valida.
2. Si es válido, se sortea el rival y los ataques, se guardan en `session["batalla"]` y se redirige a `/battle`.
3. `/battle` lee `session["batalla"]`, busca los Pokémon en `DATOS` y pinta la página. La URL queda limpia (sin parámetros).
4. Si alguien entra a `/battle` sin haber elegido Pokémon, se le redirige al listado.

#### 3. Cerrar sesión

La ruta `/logout` (solo POST) borra toda la sesión y redirige a `/`:

```python
@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))
```

Se usa POST porque cerrar sesión modifica el estado de la aplicación. El botón "Cerrar sesión" está en `base.html`, dentro de un `{% if session.trainer %}`, así que aparece en todas las páginas mientras haya un entrenador y desaparece cuando no lo hay.

## Rutas y vistas

| Ruta | Métodos | Protegida | Descripción |
|---|---|---|---|
| `/` | GET, POST | No | Formulario del entrenador. Valida y guarda `trainer` en la sesión. |
| `/pokemons` | GET, POST | Sí | Listado con filtros y formulario para elegir Pokémon. |
| `/pokemon/<id>` | GET | Sí | Detalle de un Pokémon: datos, estadísticas, media y movimientos. |
| `/battle` | GET | Sí | Batalla entre el Pokémon elegido y un rival, con 4 ataques. |
| `/logout` | POST | No | Borra la sesión y vuelve a `/`. |

## Flujo de interacción

```
/  ──(nombre válido)──►  /pokemons  ──(Pokémon válido)──►  /battle
                           │  ▲
                           ▼  │
                       /pokemon/<id>

Cualquier pantalla ──(Cerrar sesión)──►  /logout  ──►  /
Sin entrenador en sesión, las rutas protegidas redirigen a /
```

## Cómo ejecutarlo

```bash
pip install flask
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")   # en Windows: set SECRET_KEY=...
python app/main.py
```

La aplicación queda disponible en `http://127.0.0.1:8080`.
