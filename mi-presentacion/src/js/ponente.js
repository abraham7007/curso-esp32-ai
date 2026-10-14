// Vista del ponente: recibe el estado de la lámina proyectada y le devuelve
// las órdenes de avance. Ver ponente.html.

const canal = new BroadcastChannel("esp32-ponente");
const $ = (id) => document.getElementById(id);

canal.addEventListener("message", ({ data }) => {
	if (data?.tipo !== "estado") return;
	$("pos").textContent = data.posicion || "—";
	$("titulo").textContent = data.titulo || "—";
	$("pasos").textContent = data.pasosTotal
		? `Paso ${data.pasosMostrados} de ${data.pasosTotal}`
		: "";
	$("notas").innerHTML =
		data.notas || "<p class='ponente__vacio'>Esta lámina no tiene notas.</p>";
	$("siguiente").textContent = data.siguiente || "Fin de la sesión";
});

// Al abrirse, pide a la lámina que vuelva a anunciarse.
canal.postMessage({ tipo: "pedir-estado" });

const ordenar = (orden) => canal.postMessage({ tipo: "orden", orden });
$("adelante").addEventListener("click", () => ordenar("avanzar"));
$("atras").addEventListener("click", () => ordenar("retroceder"));

document.addEventListener("keydown", (e) => {
	if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
		e.preventDefault();
		ordenar("avanzar");
	} else if (e.key === "ArrowLeft" || e.key === "PageUp") {
		e.preventDefault();
		ordenar("retroceder");
	}
});

// Cronómetro de la sesión.
let inicio = Date.now();
$("reiniciar").addEventListener("click", () => {
	inicio = Date.now();
});
setInterval(() => {
	const s = Math.floor((Date.now() - inicio) / 1000);
	const mm = String(Math.floor(s / 60)).padStart(2, "0");
	const ss = String(s % 60).padStart(2, "0");
	$("reloj").textContent = `${mm}:${ss}`;
}, 500);
