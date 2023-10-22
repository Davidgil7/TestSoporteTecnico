fetch("http://127.0.0.1:5000/vistallamadas")
    .then(response => response.json())
    .then(data => {
        var tabla = document.getElementById("vista-usuarios");
        tabla.innerHTML = "";
        var claves = Object.keys(data[0]);
        var tr = document.createElement("tr");

        for (var i = 0; i < claves.length; i++) {
            var th = document.createElement("th");
            th.textContent = claves[i];
            tr.appendChild(th);
        }
        tabla.appendChild(tr);

        for (var i = 0; i < data.length; i++) {

            var tr = document.createElement("tr");
            for (var propiedad in data[i]) {
                var td = document.createElement("td");
                td.textContent = data[i][propiedad];
                tr.appendChild(td);
            }

            tabla.appendChild(tr);
        }

        for (var i = 0; i < tabla.rows.length; i++) {
            for (var j = 0; j < tabla.rows[i].cells.length; j++) {
                var valor = tabla.rows[i].cells[j].textContent;
                var numero = parseInt(valor);
                if (numero > 600 && j == 3) {
                    tabla.rows[i].cells[j].style.backgroundColor = "red";
                }
            }
        }
    });

let select = document.getElementById("tipoConsulta");
select.addEventListener("change", function () {
    let tipo = select.value;

    obtenerDatos(tipo);
});

function obtenerDatos(tipo) {
    fetch("http://127.0.0.1:5000/numero-llamadas-usuario/" + tipo)
        .then(response => response.json())
        .then(data => {

            var tabla = document.getElementById("tabla");
            tabla.innerHTML = "";
            var claves = Object.keys(data[0]);
            var tr = document.createElement("tr");
            for (var i = 0; i < claves.length; i++) {
                var th = document.createElement("th");
                th.textContent = claves[i];
                tr.appendChild(th);
            }

            tabla.appendChild(tr);
            for (var i = 0; i < data.length; i++) {
                var tr = document.createElement("tr");
                for (var propiedad in data[i]) {
                    var td = document.createElement("td");
                    td.textContent = data[i][propiedad];
                    tr.appendChild(td);
                }
                tabla.appendChild(tr);
            }
        });
}


function resumenLlamada() {
    // Obtener el valor del cuadro de texto
    var valor = document.getElementById("extension").value;
    
    fetch("http://127.0.0.1:5000/resumen-llamadas/"+ valor)
        .then(response => response.json())
        .then(data => {
            var tabla = document.getElementById("resumen-llamadas");
            tabla.innerHTML = "";
            var claves = Object.keys(data[0]);
            var tr = document.createElement("tr");

            for (var i = 0; i < claves.length; i++) {
                var th = document.createElement("th");
                th.textContent = claves[i];
                tr.appendChild(th);
            }
            tabla.appendChild(tr);

            for (var i = 0; i < data.length; i++) {

                var tr = document.createElement("tr");
                for (var propiedad in data[i]) {
                    var td = document.createElement("td");
                    td.textContent = data[i][propiedad];
                    tr.appendChild(td);
                }

                tabla.appendChild(tr);
            }


        });
}