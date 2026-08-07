/* Exporta una sesión completa a un solo PDF, una lámina por página.
 *
 * Por qué no basta con «imprimir» desde el navegador: cada lámina es un
 * documento HTML independiente, así que la impresión manual produciría 33
 * archivos. Aquí se recorre la cadena de navegación igual que la recorre
 * quien proyecta, se imprime cada lámina a su propio PDF y se unen al final.
 *
 * El tamaño de página es el mismo 1440 × 900 con el que se verifica el mazo,
 * expresado en pulgadas a 96 ppp: cualquier otro tamaño reflowaría el texto y
 * el PDF dejaría de representar lo que se ve al proyectar.
 *
 * Al unir, cada página trae incrustadas sus propias fuentes: treinta y tres
 * copias del mismo juego tipográfico. Por eso el archivo sale desproporcionado
 * y por eso se pasa al final por Ghostscript, que las unifica y recomprime los
 * flujos. Sobre la sesión 1 eso baja de 9,4 MB a 2,0 MB sin pérdida visible;
 * si Ghostscript no está instalado, se conserva el PDF unido sin comprimir.
 *
 * Uso:  node tools/exportar-pdf.mjs clase-01 [destino.pdf]
 */
import { execFileSync } from "node:child_process";
import { mkdirSync, readdirSync, renameSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import { asegurarServidor } from "./lib/servidor.mjs";

const RAIZ = path.resolve(import.meta.dirname, "..");
const BASE = "http://localhost:5173";
const ANCHO_PX = 1440;
const ALTO_PX = 900;
const PPP = 96;

const clase = process.argv[2] ?? "clase-01";
const destino = path.resolve(
	process.argv[3] ?? path.join(RAIZ, "export", `${clase}.pdf`),
);
const temporal = path.join(RAIZ, "export", ".paginas");

const laminas = readdirSync(path.join(RAIZ, "src", "slides", clase))
	.filter((f) => f.endsWith(".html"))
	.sort();

mkdirSync(temporal, { recursive: true });

await asegurarServidor();

const navegador = await chromium.launch({ channel: "chrome" });
const pagina = await navegador.newPage({
	viewport: { width: ANCHO_PX, height: ALTO_PX },
});

const sueltos = [];
for (const [i, lamina] of laminas.entries()) {
	await pagina.goto(`${BASE}/src/slides/${clase}/${lamina}`, {
		waitUntil: "networkidle",
	});

	/* Las láminas entran con una animación escalonada y algunas figuras se
	   insertan en línea tras una petición. Imprimir antes de que ambas cosas
	   terminen produce páginas con huecos donde luego hay contenido. */
	await pagina.waitForTimeout(900);
	await pagina.evaluate(() => {
		for (const el of document.querySelectorAll("*")) {
			el.style.animation = "none";
			el.style.transition = "none";
		}
		for (const el of document.querySelectorAll("[data-animate]")) {
			el.classList.add("is-visible");
			el.style.opacity = "1";
			el.style.transform = "none";
		}
	});
	await pagina.waitForTimeout(200);

	const salida = path.join(temporal, `${String(i).padStart(3, "0")}.pdf`);
	await pagina.pdf({
		path: salida,
		width: `${ANCHO_PX / PPP}in`,
		height: `${ALTO_PX / PPP}in`,
		printBackground: true,
		pageRanges: "1",
	});
	sueltos.push(salida);
	process.stdout.write(`  ${lamina}\n`);
}

await navegador.close();

mkdirSync(path.dirname(destino), { recursive: true });
const unido = path.join(temporal, "unido.pdf");
execFileSync("pdfunite", [...sueltos, unido]);
const antes = statSync(unido).size;

/* Ghostscript unifica las fuentes repetidas y recomprime los flujos. El perfil
   `printer` conserva la resolución de imagen que necesita una proyección; con
   `ebook` el archivo pesa lo mismo y remuestrea de más, y con `prepress` sube
   un 50 % sin ganancia visible. */
let comprimido = false;
try {
	execFileSync("gs", [
		"-sDEVICE=pdfwrite",
		"-dCompatibilityLevel=1.7",
		"-dPDFSETTINGS=/printer",
		"-dDetectDuplicateImages=true",
		"-dNOPAUSE",
		"-dQUIET",
		"-dBATCH",
		`-sOutputFile=${destino}`,
		unido,
	]);
	comprimido = true;
} catch {
	renameSync(unido, destino);
	console.log("  aviso: Ghostscript no disponible, PDF sin comprimir");
}

const despues = statSync(destino).size;
rmSync(temporal, { recursive: true, force: true });

const mb = (n) => `${(n / 1024 / 1024).toFixed(1)} MB`;
console.log(
	`\n${laminas.length} láminas → ${path.relative(RAIZ, destino)}  ` +
		(comprimido
			? `${mb(antes)} → ${mb(despues)} (−${Math.round((1 - despues / antes) * 100)} %)`
			: mb(despues)),
);
