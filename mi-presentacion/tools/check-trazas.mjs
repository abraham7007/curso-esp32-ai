/* Detecta trazas del monitor serie recortadas por la derecha.
 *
 * El recuadro .term tiene el desbordamiento oculto: una línea más ancha que
 * la columna desaparece sin que nada lo acuse — ni el navegador, ni el
 * comprobador de geometría, que solo mide altura. Se descubrió al convertir
 * las láminas de práctica y afectaba a nueve de ellas.
 *
 * Uso:  node tools/check-trazas.mjs [clase-NN ...]     (sin argumentos, todas)
 */
import { readdirSync } from "node:fs";
import { chromium } from "playwright";
import { asegurarServidor } from "./lib/servidor.mjs";

const RAIZ = "src/slides";
const clases =
	process.argv.length > 2
		? process.argv.slice(2)
		: readdirSync(RAIZ)
				.filter((d) => d.startsWith("clase-"))
				.sort();

await asegurarServidor();

const navegador = await chromium.launch({ channel: "chrome" });
const pagina = await navegador.newPage({
	viewport: { width: 1440, height: 900 },
});

let recortadas = 0;
for (const clase of clases) {
	for (const lamina of readdirSync(`${RAIZ}/${clase}`)
		.filter((f) => f.endsWith(".html"))
		.sort()) {
		await pagina.goto(`http://localhost:5173/${RAIZ}/${clase}/${lamina}`, {
			waitUntil: "networkidle",
		});
		await pagina.waitForTimeout(250);
		const exceso = await pagina.evaluate(() => {
			let peor = 0;
			for (const t of document.querySelectorAll(".term")) {
				peor = Math.max(peor, t.scrollWidth - t.clientWidth);
			}
			return Math.round(peor);
		});
		if (exceso > 2) {
			console.log(`${String(exceso).padStart(4)}px  ${clase}/${lamina}`);
			recortadas++;
		}
	}
}

await navegador.close();
console.log(
	recortadas
		? `\n${recortadas} traza(s) recortada(s).`
		: "Ninguna traza recortada.",
);
