/* Mide el espacio vertical que una lámina deja sin usar.
 *
 * `check-slides.mjs` detecta lo contrario: contenido que no cabe. Pero la
 * queja que llegó sobre la sesión 1 fue la opuesta —«hay espacios que no se
 * aprovechan bien»— y esa no la ve ningún verificador de desbordamiento.
 *
 * Por qué no basta con medir el hueco de abajo: cuando un bloque lleva
 * `is-stretch` el contenedor sí ocupa todo el alto, así que por abajo no
 * sobra nada, pero el vacío reaparece DENTRO del bloque —entre sus filas, o
 * entre su título y su tabla—. Medir solo el margen inferior daba mejoras
 * falsas: una lámina pasó de 282 a 297 px de vacío real mientras el hueco de
 * abajo bajaba a cero. Por eso se informa del mayor vacío contiguo esté donde
 * esté; la medición vive en tools/lib/medir-hueco.mjs.
 *
 * Uso:  node tools/check-huecos.mjs [clase-01] [--umbral 140]
 */
import { readdirSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import {
	medirHueco,
	prepararLamina,
	UMBRAL_POR_OMISION,
} from "./lib/medir-hueco.mjs";
import { asegurarServidor } from "./lib/servidor.mjs";

const RAIZ = path.resolve(import.meta.dirname, "..");
const BASE = "http://localhost:5173";
const SLIDES = path.join(RAIZ, "src", "slides");

const args = process.argv.slice(2);
const iUmbral = args.indexOf("--umbral");
const UMBRAL = iUmbral === -1 ? UMBRAL_POR_OMISION : Number(args[iUmbral + 1]);
const filtro = args.find((a) => !a.startsWith("--") && a !== String(UMBRAL));

const laminas = [];
for (const clase of readdirSync(SLIDES).sort()) {
	for (const archivo of readdirSync(path.join(SLIDES, clase)).sort()) {
		if (!archivo.endsWith(".html")) continue;
		const rel = `${clase}/${archivo}`;
		if (filtro && !rel.includes(filtro)) continue;
		laminas.push(rel);
	}
}

await asegurarServidor();

const navegador = await chromium.launch({ channel: "chrome" });
const pagina = await navegador.newPage({
	viewport: { width: 1440, height: 900 },
});

const medidas = [];
for (const rel of laminas) {
	/* Un recorrido de las 322 dura minutos, y en ese tiempo cualquier retoque
	   de CSS hace que Vite recargue la página en caliente justo mientras se
	   mide: la medición muere con «Execution context was destroyed» y se pierde
	   el recorrido entero. Se reintenta la lámina en vez de abortar. */
	let m = null;
	for (let intento = 0; intento < 3 && !m; intento++) {
		try {
			await pagina.goto(`${BASE}/src/slides/${rel}`, {
				waitUntil: "networkidle",
			});
			await prepararLamina(pagina);
			m = await medirHueco(pagina);
		} catch (e) {
			if (intento === 2) throw e;
			process.stdout.write("r");
		}
	}
	if (m) medidas.push({ rel, ...m });
	process.stdout.write(".");
}

await navegador.close();

const sospechosas = medidas
	.filter((m) => m.px >= UMBRAL)
	.sort((a, b) => b.px - a.px);

console.log(`\n\nMedidas ${medidas.length} láminas · umbral ${UMBRAL} px\n`);
if (!sospechosas.length) {
	console.log("Ninguna lámina deja un vacío por encima del umbral.");
} else {
	for (const s of sospechosas) {
		console.log(`  ${String(s.px).padStart(4)} px  ${s.rel}  (${s.donde})`);
	}
	console.log(`\n${sospechosas.length} láminas por encima del umbral.`);
}

/* Resumen por sesión: lo que interesa al comparar si una mejora hecha en una
   clase llegó a las demás. */
const porClase = new Map();
for (const m of medidas) {
	const c = m.rel.split("/")[0];
	if (!porClase.has(c)) porClase.set(c, []);
	porClase.get(c).push(m.px);
}
console.log("\nclase      láminas   mayor   mediana   sobre umbral");
for (const [c, px] of [...porClase].sort()) {
	const ord = [...px].sort((a, b) => a - b);
	const med = ord[Math.floor(ord.length / 2)];
	const n = px.filter((v) => v >= UMBRAL).length;
	console.log(
		`${c}   ${String(px.length).padStart(5)}   ${String(Math.max(...px)).padStart(5)}   ${String(med).padStart(7)}   ${String(n).padStart(12)}`,
	);
}
