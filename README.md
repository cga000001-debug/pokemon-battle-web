# pokemon-battle-web

Aplicación web hecha con Flask donde un entrenador elige un Pokémon legendario y se enfrenta a un rival aleatorio.

## Estructura del proyecto

El código está organizado en capas. Cada capa solo habla con la siguiente:

```
rutas (routes)  →  servicio (services)  →  repositorio (repositories)  →  JSON
```

```
pokemon-battle-web/
├── app/
│   ├── main.py                    # Crea la app, configura la sesión y registra los blueprints
│   ├── models/
│   │   └── pokemon.py             # Dataclass Pokemon
│   ├── repositories/
│   │   └── pokemon_repo.py        # Lee el JSON y consulta los datos
│   ├── services/
│   │   └── pokemon_service.py     # Lógica de negocio (búsqueda y filtros)
│   ├── forms/
│   │   └── trainer_form.py        # Formulario del entrenador (Flask-WTF)
│   ├── routes/
│   │   ├── user_routes.py         # Inicio y logout
│   │   ├── pokemon_routes.py      # Listado y detalle
│   │   └── battle_routes.py       # Batalla
│   ├── util/
│   │   └── decorator_functions.py # Decorador login_requerido
│   ├── templates/                 # Plantillas Jinja2
│   └── static/css/styles.css
├── data/pokemons-legendary.json
├── requirements.txt
└── .gitignore                     # Incluye la carpeta de sesiones (.flask_session/)
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

**Cómo funciona:**
- `Pokemon` (`models/pokemon.py`) es una dataclass con los campos del Pokémon (id, nombre, tipos, estadísticas, movimientos, sprites...) y `media`, la media de sus estadísticas.
- `PokemonRepository` (`repositories/pokemon_repo.py`) lee `pokemons-legendary.json` **una sola vez** al crearse, convierte cada elemento en un objeto `Pokemon` y calcula su `media`. Ofrece las consultas: todos, por id, por nombre, por tipo y por rango de media.
- `PokemonService` (`services/pokemon_service.py`) es la capa que usan las rutas. Delega en el repositorio y añade `filter_pokemons`, que combina el filtro de tipo y el de media.
- Las plantillas reciben objetos `Pokemon` y acceden con `pokemon.name`, `pokemon.types`, etc.

### Fase II
##### Objetivos
- Emplear formularios para recoger la información introducida por el usuario.
- Pasar parámetros por URL.
- Validación de los datos en el servidor.

**Cómo funciona:**
- **Formulario del entrenador (`/`)**: usa Flask-WTF (`TrainerForm`). El nombre es obligatorio y debe tener entre 3 y 15 caracteres; los espacios sobrantes se eliminan antes de validar. Si falla, se vuelve a mostrar el formulario con el mensaje de error. Incluye un token CSRF.
- **Formulario de elegir Pokémon (`/pokemons/`, POST)**: se comprueba que el nombre no esté vacío y que exista. Si falla, el error se muestra bajo el campo.
- **Filtros del listado (`/pokemons/`, GET)**: filtran por tipo y por media de estadísticas (baja < 100, media 100-112, alta > 112). Se leen con `request.args.get` y se aplican con `service.filter_pokemons`. Los filtros viajan por la URL, por ejemplo `/pokemons/?tipo=fire&media=alta`.

### Fase III
##### Objetivos
- Comprender cómo mantener datos de usuario entre distintas peticiones HTTP.
- Utilizar sesiones en Flask para conservar información durante la navegación.
- Decidir qué datos de la aplicación tiene sentido guardar en la sesión.

#### 1. Preparación del entorno

Se usa **Flask-Session** con almacenamiento en el sistema de ficheros. Los datos de la sesión se guardan en el servidor, en la carpeta `.flask_session/` (incluida en `.gitignore`), y el navegador solo guarda una cookie con el identificador de la sesión.

```python
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)
```

La sesión es permanente (7 días), así que sobrevive al cierre del navegador. La clave secreta se lee de la variable de entorno `SECRET_KEY`; en un entorno real no se sube al repositorio.

Las dependencias (Flask, Flask-Session y Flask-WTF) están en `requirements.txt`.

#### 2. Mantenimiento del estado en sesión

**Entrenador y protección de pantallas**

Cuando el entrenador envía un nombre válido en `/`, se guarda en `session["trainer"]` y se redirige al listado. Ya no viaja por la URL. Si ya hay un entrenador en la sesión, la página principal redirige directamente al listado y no vuelve a pedir el nombre.

Las pantallas protegidas usan el decorador `@login_requerido` (`util/decorator_functions.py`), que se ejecuta antes de la vista: si no hay `trainer` en la sesión, redirige a la página principal.

```python
def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("user.index"))
        return func(*args, **kwargs)
    return wrapper
```

Está aplicado en el listado, el detalle y la batalla.

**Datos guardados en la sesión y por qué**

| Clave | Qué guarda | Por qué |
|---|---|---|
| `trainer` | Nombre del entrenador | Identifica al usuario y permite bloquear el acceso al resto de pantallas si no existe. Antes se pasaba por la URL. |
| `batalla` | `id` del Pokémon elegido, `id` del rival y lista de 4 índices de ataques | El rival y los ataques se sortean al azar. Si no se guardaran, al recargar `/battle` cambiarían y sería otra batalla distinta. Al guardarlos, la batalla se mantiene igual al recargar o al volver más tarde. |

**Por qué se guardan ids e índices y no los Pokémon completos:** los datos completos ya están en el repositorio. Guardar solo identificadores evita duplicar información y la sesión queda pequeña. En `/battle` se reconstruye todo buscando esos ids con `service.get_pokemon_by_id`.

**Qué no se guarda:** los filtros del listado (`tipo` y `media`) viajan por la URL con GET. Son una consulta, no un estado del usuario, y así se pueden recargar y compartir enlaces filtrados.

**Flujo de la batalla:**
1. En `/pokemons/` el usuario escribe un Pokémon y se valida.
2. Si es válido, se sortea el rival y los ataques, se guardan en `session["batalla"]` y se redirige a `/battle/`.
3. `/battle/` lee `session["batalla"]`, busca los Pokémon con el servicio y pinta la página. La URL queda limpia (sin parámetros).
4. Si alguien entra a `/battle/` sin haber elegido Pokémon, se le redirige al listado.

#### 3. Cerrar sesión

La ruta `/logout` (solo POST) borra toda la sesión y redirige a la página principal:

```python
@user_bp.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('user.index'))
```

Se usa POST porque cerrar sesión modifica el estado de la aplicación. El botón "Cerrar sesión" está en `base.html`, dentro de un `{% if session.trainer %}`, así que aparece en todas las páginas mientras haya un entrenador y desaparece cuando no lo hay.

### Fase IV
##### Objetivos
- Tener una estructura más limpia y modular en Flask, separando responsabilidades y preparando la base para proyectos más grandes.
- Reorganizar el código siguiendo una arquitectura en capas.
- Distinguir entre la lógica de presentación, negocio y datos.
- Entender cómo cada capa colabora con las demás.
- Integrar formularios con Flask-WTF para gestionar entradas de usuario de forma segura.

#### 1. Reorganización del proyecto

Todo el código vivía en un único `main.py`. Ahora está repartido en carpetas dentro de `app/`, una por responsabilidad:

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Presentación | `routes/`, `forms/`, `templates/` | Recibe las peticiones, valida los formularios y devuelve las vistas. No contiene lógica de negocio. |
| Negocio | `services/` | Decide qué hacer con los datos: buscar por nombre, combinar filtros de tipo y media... |
| Datos | `repositories/` | Es el único que conoce el JSON. Lo lee y ofrece consultas básicas. |
| Dominio | `models/` | Representa los datos de la aplicación (`Pokemon`). |
| Utilidades | `util/` | Código transversal, como el decorador `login_requerido`. |

Cada capa solo habla con la siguiente: una ruta nunca lee el JSON y el repositorio nunca sabe nada de Flask. Por ejemplo, al filtrar el listado:

1. `pokemon_routes.py` lee `tipo` y `media` de la URL.
2. Llama a `service.filter_pokemons(tipo, media)`.
3. El servicio pide los datos al repositorio y aplica los filtros.
4. La ruta recibe la lista de objetos `Pokemon` y la pasa a la plantilla.

Así, si mañana los datos vinieran de una base de datos, solo habría que cambiar el repositorio.

**Programación orientada a objetos:**
- **Modelo**: `Pokemon` es una `dataclass`, tal como exige el enunciado para los modelos del dominio.
- **Repositorio y servicio**: son clases (`PokemonRepository`, `PokemonService`). El servicio recibe el repositorio en su constructor, de modo que no depende de cómo se obtienen los datos.
- **Rutas y decorador**: se implementan con funciones, que es lo habitual en Flask.

#### 2. Blueprints

Las rutas están en `routes/` y divididas en tres blueprints, uno por área funcional:

| Blueprint | Fichero | Prefijo | Rutas | Por qué |
|---|---|---|---|---|
| `user` | `user_routes.py` | (ninguno) | `/`, `/logout` | Todo lo relacionado con el entrenador y su sesión: entrar y salir. |
| `pokemon` | `pokemon_routes.py` | `/pokemons` | `/`, `/<id>` | Consulta del catálogo: listado con filtros y detalle. |
| `battle` | `battle_routes.py` | `/battle` | `/` | La batalla tiene su propio estado (`session["batalla"]`) y puede crecer sin afectar al resto. |

Se ha elegido dividir por **funcionalidad**, no por tipo de petición, porque cada blueprint agrupa rutas que cambian por el mismo motivo. El blueprint `user` va sin prefijo para que la página principal siga siendo `/`.

Al usar blueprints, el nombre del endpoint lleva el prefijo del blueprint: `url_for('pokemon.listadoPokemon')`, `url_for('battle.battle')`, `url_for('user.index')`. Los tres se registran en `main.py`:

```python
app.register_blueprint(user_bp)
app.register_blueprint(pokemon_bp, url_prefix="/pokemons")
app.register_blueprint(battle_bp, url_prefix="/battle")
```

#### 3. Formularios con Flask-WTF

Los formularios viven en `forms/`. Se ha migrado el **formulario del entrenador** a `TrainerForm`:

```python
class TrainerForm(FlaskForm):
    trainer = StringField(
        "Trainer:",
        filters=[lambda valor: valor.strip() if valor else valor],
        validators=[
            DataRequired(message="El trainer es obligatorio."),
            Length(min=3, max=15, message="El trainer debe tener entre 3 y 15 caracteres."),
        ],
    )
```

Lo que aporta frente al formulario HTML anterior:
- **Validación declarativa**: las reglas están en la clase y desaparecen los `if` manuales de la ruta, que queda así: `if form.validate_on_submit(): ...`.
- **Protección CSRF**: la plantilla incluye `{{ form.hidden_tag() }}`, que añade un token que el servidor comprueba en cada POST.
- **Errores y valor conservado**: los mensajes se muestran con `form.trainer.errors` y el campo mantiene lo que escribió el usuario.

El formulario de elegir Pokémon y los filtros del listado siguen siendo HTML. Los filtros son consultas GET con botones que no modifican datos, y el formulario del Pokémon necesita buscar en el servicio, así que se ha priorizado migrar el del entrenador, que es el que gestiona la identidad del usuario.

## Rutas y vistas

Las rutas están divididas en tres blueprints. El nombre del endpoint lleva el prefijo del blueprint (por ejemplo `url_for('pokemon.listadoPokemon')`).

| Ruta | Endpoint | Métodos | Protegida | Descripción |
|---|---|---|---|---|
| `/` | `user.index` | GET, POST | No | Formulario del entrenador. Valida y guarda `trainer` en la sesión. |
| `/logout` | `user.logout` | POST | No | Borra la sesión y vuelve a `/`. |
| `/pokemons/` | `pokemon.listadoPokemon` | GET, POST | Sí | Listado con filtros y formulario para elegir Pokémon. |
| `/pokemons/<id>` | `pokemon.pokemon` | GET | Sí | Detalle de un Pokémon: datos, estadísticas, media y movimientos. |
| `/battle/` | `battle.battle` | GET | Sí | Batalla entre el Pokémon elegido y un rival, con 4 ataques. |

## Flujo de interacción

```
/  ──(nombre válido)──►  /pokemons/  ──(Pokémon válido)──►  /battle/
                            │  ▲
                            ▼  │
                       /pokemons/<id>

Cualquier pantalla ──(Cerrar sesión)──►  /logout  ──►  /
Sin entrenador en sesión, las rutas protegidas redirigen a /
Con entrenador en sesión, / redirige a /pokemons/
```

## Cómo ejecutarlo

Desde la **raíz del proyecto** (la carpeta que contiene `app/` y `data/`):

```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Definir la clave secreta (opcional en desarrollo)
set SECRET_KEY=una-clave-larga-y-aleatoria          # Windows (cmd)
export SECRET_KEY=una-clave-larga-y-aleatoria       # Linux / macOS

# 4. Arrancar la aplicación como módulo
python -m app.main
```

Hay que ejecutarlo como módulo (`python -m app.main`) y no con `python app/main.py`, porque los imports son de la forma `from app.routes...` y solo se resuelven desde la raíz del proyecto.

La aplicación queda disponible en `http://127.0.0.1:8080`.
