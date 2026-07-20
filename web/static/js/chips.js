/**
 * chip-selector: combobox reutilizable con opcion "Otro" para escribir un
 * valor libre, botón "+ Agregar" y lista de chips removibles. El resultado
 * final se guarda en un <input type="hidden"> como texto separado por comas,
 * para mantener compatibilidad con el backend (parsear_lista en app.py).
 *
 * Uso (ver nuevo_puesto.html):
 *   <div class="chip-selector" id="chip-habilidades" data-hidden-name="habilidadesRequeridas">
 *     <div class="chip-lista"></div>
 *     <div class="chip-agregar">
 *       <select class="chip-select">...opciones... <option value="__otro__">Otro...</option></select>
 *       <input type="text" class="chip-otro" style="display:none">
 *       <button type="button" class="boton-secundario chip-add-btn">+ Agregar</button>
 *     </div>
 *   </div>
 *   <script>initChipSelector('chip-habilidades', ['Python', 'SQL']); </script>
 */
function initChipSelector(containerId, valoresIniciales) {
    valoresIniciales = valoresIniciales || [];

    const contenedor = document.getElementById(containerId);
    if (!contenedor) return;

    const listaChips = contenedor.querySelector(".chip-lista");
    const select = contenedor.querySelector(".chip-select");
    const otroInput = contenedor.querySelector(".chip-otro");
    const botonAgregar = contenedor.querySelector(".chip-add-btn");
    const hiddenName = contenedor.dataset.hiddenName;

    let hidden = contenedor.querySelector('input[type="hidden"]');
    if (!hidden) {
        hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.name = hiddenName;
        contenedor.appendChild(hidden);
    }

    let valores = valoresIniciales.slice();

    function renderizar() {
        listaChips.innerHTML = "";
        valores.forEach((valor, indice) => {
            const chip = document.createElement("span");
            chip.className = "chip";

            const texto = document.createElement("span");
            texto.textContent = valor;
            chip.appendChild(texto);

            const quitar = document.createElement("button");
            quitar.type = "button";
            quitar.className = "chip-quitar";
            quitar.setAttribute("aria-label", "Quitar " + valor);
            quitar.textContent = "×";
            quitar.addEventListener("click", () => {
                valores.splice(indice, 1);
                renderizar();
            });
            chip.appendChild(quitar);

            listaChips.appendChild(chip);
        });
        hidden.value = valores.join(", ");
    }

    function agregarValor(valorCrudo) {
        const valor = (valorCrudo || "").trim();
        if (!valor) return;
        const yaExiste = valores.some((v) => v.toLowerCase() === valor.toLowerCase());
        if (!yaExiste) {
            valores.push(valor);
            renderizar();
        }
        select.value = "";
        otroInput.value = "";
        otroInput.style.display = "none";
    }

    select.addEventListener("change", () => {
        if (select.value === "__otro__") {
            otroInput.style.display = "inline-block";
            otroInput.focus();
        } else if (select.value) {
            agregarValor(select.value);
        }
    });

    otroInput.addEventListener("keydown", (evento) => {
        if (evento.key === "Enter") {
            evento.preventDefault();
            agregarValor(otroInput.value);
        }
    });

    botonAgregar.addEventListener("click", () => {
        if (select.value === "__otro__") {
            agregarValor(otroInput.value);
        } else if (select.value) {
            agregarValor(select.value);
        }
    });

    renderizar();

    // Se expone por si el formulario necesita precargar valores (ej. desde un CV).
    contenedor._chipApi = { agregarValor, renderizar, obtenerValores: () => valores.slice() };
}
